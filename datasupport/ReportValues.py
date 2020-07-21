import csv, re, numpy, time, string

class ReadExcel(object):
    def _ReadCsv(self, csv_file):
        self.csv_file = csv_file
        with open(self.csv_file) as f:
            csv_list = [i for i in csv.reader(f)]
        return csv_list


class ReportPass(ReadExcel):
    def __init__(self, **src_f):
        self.srcd = src_f['srcd']
        self.srcd_table = super()._ReadCsv(self.srcd)
        
        if len(src_f) == 2:
            self.srcc = src_f['srcc']
            self.srcc_table = super()._ReadCsv(self.srcc)

        # 定义 月/周 字典
        self.mon_data_dict = {}
        self.week_data_dict = {}
        # 定义 自建 字典
        self.CreateList_dict = {}
        # 生成字典
        self._CreateList()
        
    # 除法 求%
    def _Division(self, mol, den):
        if den == 0 and mol > 0:
            return -1
        elif den == 0:
            return 0
        else:
            return (mol / den * 100)

    # 获取 表单月份
    def _GetFormMon(self):
        self.GFM = re.search(r'(\d+)-(\d+)-(\d+)', self.srcd_table[2][0]).group()
        return time.strftime('%m', time.strptime(self.GFM, '%Y-%m-%d'))

    # 计算 日期差
    def _TimeDiff(self, a_j, b_j):
        # a_j - b_j
        early = time.mktime(time.strptime(b_j, '%Y-%m-%d'))
        late = time.mktime(time.strptime(a_j, '%Y-%m-%d'))
        return int((late - early) / (24 * 60 * 60))
    
    # 检查月份是否一致
    def _TimeCheck(self, get_date):
        if time.strftime('%m', time.strptime(get_date, '%Y-%m-%d')) == self._GetFormMon():
            return True
        else:
            return False

    # 获取 阶段数据
    def _GetStageData(self, num, column_name):
        column_num = self._GetSN(column_name)
        stage_value = self.srcc_table[num - 1][column_num]
        days_find = re.search(r'\d+天', stage_value)
        hours_find = re.search(r'\d+小时', stage_value)
        if days_find:
            trans_days = int(re.search(r'\d+', days_find.group(0)).group(0)) * 24
        else:
            trans_days = 0
        if hours_find:
            trans_hours = int(re.search(r'\d+', hours_find.group(0)).group(0))
        else:
            trans_hours = 0
        return trans_days + trans_hours

    # 获取 各列序号
    def _GetSN(self, Keyword):
        count = 1
        for i in string.ascii_uppercase:
            if i == Keyword:
                return count - 1
            else:
                count += 1

    # 获取 各列数据
    def _CouF(self, Keyword):
        cou_list = []
        for i in self.srcd_table[5:]:
            if i[self._GetSN(Keyword)].isdigit():
                value = int(i[self._GetSN(Keyword)])
            else:
                value = i[self._GetSN(Keyword)]
            cou_list.append(value)
        return cou_list

    # 生成 各列列表 字典
    def _CreateList(self):
        for i in 'CDQRSUAMJKLHGT':
            self.CreateList_dict[i] = self._CouF(i)
            
    # 求百分比(除法)
    def _Percentage(self, mol, den, digits=None):
        if den == 0 and mol > 0:
            return -1
        elif den == 0:
            return 0
        else:
            res = mol / den * 100
            if digits == 2:
                return '%.2f%%' %(res)
            else:
                return '%.f%%' %(res)

    # 求岗位成功关闭率
    def _GWCGGBL(self):
        cou_list = []
        for num in range(len(self.CreateList_dict['C'])):
            c_line = self.CreateList_dict['C'][num]
            d_line = self.CreateList_dict['D'][num]
            if c_line != '-' and d_line != '-' and self._TimeCheck(c_line) and self._TimeCheck(d_line):
                cou_list.append((c_line, d_line))
        return cou_list
        
    # 月汇报 字典
    def GetMonData(self):
        self.mon_data_dict['初试数'] = int(numpy.sum(self.CreateList_dict['Q']))
        self.mon_data_dict['复试数'] = int(numpy.sum(self.CreateList_dict['R']))
        self.mon_data_dict['创建offer数'] = int(numpy.sum(self.CreateList_dict['S']))
        self.mon_data_dict['入职人数'] = int(numpy.sum(self.CreateList_dict['U']))
        self.mon_data_dict['职位数'] = int(len(self.CreateList_dict['A']))
        self.mon_data_dict['合格简历倍数'] = self._Percentage(numpy.sum(self.CreateList_dict['M']), self.mon_data_dict['职位数'])
        self.mon_data_dict['简历等级A'] = int(numpy.sum(self.CreateList_dict['J']))
        self.mon_data_dict['简历等级A+'] = int(numpy.sum(self.CreateList_dict['K']))
        self.mon_data_dict['简历等级S'] = int(numpy.sum(self.CreateList_dict['L']))
        self.mon_data_dict['岗位成功关闭率'] = int(len(self._GWCGGBL()))
        self.mon_data_dict['初筛通过率'] = self._Percentage(numpy.sum(self.CreateList_dict['H']), numpy.sum(self.CreateList_dict['G']), digits=2)
        self.mon_data_dict['用人部门筛选通过率'] = self._Percentage(numpy.sum(self.CreateList_dict['M']), numpy.sum(self.CreateList_dict['H']), digits=2)
        self.mon_data_dict['初试通过率'] = self._Percentage(numpy.sum(self.CreateList_dict['R']), numpy.sum(self.CreateList_dict['Q']), digits=2)
        self.mon_data_dict['复试通过率'] = self._Percentage(numpy.sum(self.CreateList_dict['S']), numpy.sum(self.CreateList_dict['R']), digits=2)
        self.mon_data_dict['外部招聘OFFER接受率'] = self._Percentage(numpy.sum(self.CreateList_dict['T']), numpy.sum(self.CreateList_dict['S']), digits=2)
        self.mon_data_dict['入职率'] = self._Percentage(numpy.sum(self.CreateList_dict['U']), numpy.sum(self.CreateList_dict['T']), digits=2)
        self.mon_data_dict['初筛周期'] = self._GetStageData(5, 'D')
        self.mon_data_dict['用人部门筛选周期'] = self._GetStageData(6, 'D')
        self.mon_data_dict['面试周期'] = self._GetStageData(7, 'D')
        self.mon_data_dict['offer发放周期'] = self._GetStageData(8, 'D')
        self.mon_data_dict['待入职周期'] = self._GetStageData(9, 'D')
        return self.mon_data_dict
    
    # 周汇报 字典
    def GetWeekData(self):
        self.week_data_dict['简历数'] = int(numpy.sum(self.CreateList_dict['G']))
        self.week_data_dict['推荐简历数'] = int(numpy.sum(self.CreateList_dict['H']))
        self.week_data_dict['推荐简历通过数'] = int(numpy.sum(self.CreateList_dict['M']))
        self.week_data_dict['专业面试数'] = int(numpy.sum(self.CreateList_dict['Q']))
        self.week_data_dict['综合面试数'] = int(numpy.sum(self.CreateList_dict['R']))
        self.week_data_dict['创建offer数'] = int(numpy.sum(self.CreateList_dict['S']))
        self.week_data_dict['入职人数'] = int(numpy.sum(self.CreateList_dict['U']))
        return self.week_data_dict
