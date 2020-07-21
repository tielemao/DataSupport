import csv, re, numpy, time

class ReadExcel(object):
    def _ReadCsv(self, csv_file):
        self.csv_file = csv_file
        with open(self.csv_file) as f:
            csv_list = [i for i in csv.reader(f)]
        return csv_list

class StagePass(ReadExcel):
    def __init__(self, **src_f):
        self.srcd = src_f['srcd']
        self.srcc = src_f['srcc']

        self.srcd_table = super()._ReadCsv(self.srcd)
        self.srcc_table = super()._ReadCsv(self.srcc)

        self.data_dict = {}

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
    #  end_j - start_j
    def _TimeDiff(self, start_j, end_j):
        ss = time.mktime(time.strptime(start_j, '%Y-%m-%d'))
        es = time.mktime(time.strptime(end_j, '%Y-%m-%d'))
        return int((es - ss) / (24 * 60 * 60))
    
    # 获取 阶段数据
    def _GetStageData(self, data_key):
        for i in self.srcc_table[4:]:
            if i[0] == data_key:
                if i[3] != '-':
                    return i[3]
                else:
                    return 0
    
    # 招聘违规率
    def CouRecViolationPercent(self):
        cou_list = [int(i[18]) for i in self.srcd_table[5:] if int(i[18]) > 0]
        self.CRVP = int(numpy.sum(cou_list))
        self.data_dict['招聘违规率'] = self.CRVP,

    # 职位数
    def CouPositions(self):
        cou_list = [i[0] for i in self.srcd_table[5:] if i[0]]
        self.CP = len(cou_list)
        self.data_dict['职位数'] = self.CP,

    # 初筛数
    def CouPreScreen(self):
        cou_list = [int(i[6]) for i in self.srcd_table[5:]]
        self.CPS = int(numpy.sum(cou_list))
        self.data_dict['初筛数'] = self.CPS,
        
    # 初筛平均处理周期
    def CouPreScreenAverCyc(self):
        offer_value = self._GetStageData('初筛')
        self.data_dict['初筛平均处理周期'] = offer_value,

    # 推荐简历数
    def CouRecomRes(self):
        cou_list = [int(i[7]) for i in self.srcd_table[5:] if int(i[7]) > 0]
        self.CRR = int(numpy.sum(cou_list))
        self.data_dict['推荐简历数'] = self.CRR,

    # 初筛通过率
    def CouPrePassPercent(self):
        self.data_dict['初筛通过率'] = self.CRR, self.CPS, '%.2f%%' %(self._Division(self.CRR, self.CPS))

    # 推荐简历等级比例
    def CouLevel(self):
        cou_a_list = []
        cou_a1_list = []
        cou_s_list = []
        for i in self.srcd_table[5:]:
            cou_a_list.append(int(i[9]))
            cou_a1_list.append(int(i[10]))
            cou_s_list.append(int(i[11]))
        self.ca = int(numpy.sum(cou_a_list))
        self.ca1 = int(numpy.sum(cou_a1_list))
        self.cs = int(numpy.sum(cou_s_list))
        self.data_dict['推荐简历等级比例'] = '%s : %s : %s' %(self.ca, self.ca1, self.cs),

    # 简历推荐通过数
    def CouRecomResPass(self):
        cou_list = [int(i[12]) for i in self.srcd_table[5:] if int(i[12]) > 0]
        self.CRRP = int(numpy.sum(cou_list))
        self.data_dict['简历推荐通过数'] = self.CRRP,

    # 简历推荐通过率
    def CouRecomPassPercent(self):
        self.data_dict['简历推荐通过率'] = self.CRRP, self.CRR, '%.2f%%' %self._Division(self.CRRP, self.CRR)
        
    # 用人部门筛选简历平均处理周期
    def CouFilterResAverCyc(self):
        offer_value = self._GetStageData('用人部门筛选')
        self.data_dict['用人部门筛选简历平均处理周期'] = offer_value,

    # 合格简历倍数
    def CouMeetResMulti(self):
        self.data_dict['合格简历倍数'] = self.CRRP, self.CP, '%.f%%' %(self._Division(self.CRRP, self.CP))

    # 安排面试数
    def CouCreateInter(self):
        cou_list = [int(i[13]) for i in self.srcd_table[5:] if int(i[13]) > 0]
        self.CCI = int(numpy.sum(cou_list))
        self.data_dict['安排面试数'] = self.CCI,

    # 邀约成功率
    def CouInvitePercent(self):
        cou_list = [int(i[14]) for i in self.srcd_table[5:] if int(i[14]) > 0]
        self.ArrInter = int(numpy.sum(cou_list))
        self.data_dict['邀约成功率'] = self.ArrInter, self.CRRP, '%.2f%%' %(self._Division(self.ArrInter, self.CRRP))
    
    # 面试通过率
    def CouInterPassPercent(self):
        cou_list = [int(i[15]) for i in self.srcd_table[5:] if int(i[15]) > 0]
        self.data_dict['面试通过率'] = int(numpy.sum(cou_list)),
        
    # 面试平均处理周期
    def CouAverageInterProcess(self):
        offer_value = self._GetStageData('面试')
        self.data_dict['面试平均处理周期'] = offer_value,

    # 沟通offer平均处理周期
    def CouOfferAverage(self):
        offer_value = self._GetStageData('沟通offer')
        self.data_dict['沟通offer平均处理周期'] = offer_value,

    # 人均创建offer的申请数
    def CouAvgCreateOffer(self):
        self.CACO = self.CRVP
        self.data_dict['人均创建offer的申请数'] = self.CACO,

    # 外部招聘OFFER接受率
    def CouOutOfferPercent(self):
        create_offer_accept_list = []
        for i in self.srcd_table[5:]:
            if int(i[19]) > 0:
                create_offer_accept_list.append(int(i[19]))
        self.COA = int(numpy.sum(create_offer_accept_list))
        self.data_dict['外部招聘OFFER接受率'] = self.COA, self.CACO, '%.2f%%' %(self._Division(self.COA, self.CACO))

    # 外部招聘平均到岗时间
    def CouAverageArrival(self):
        time_d_list = [self._TimeDiff(i[1], i[3]) for i in self.srcd_table[5:] if i[3] != '-']
        self.CAA = int(numpy.sum(time_d_list))
        self.data_dict['外部招聘平均到岗时间'] = self.CAA, len(time_d_list), '%.2f' %(self.CAA / len(time_d_list))

    # 岗位成功关闭率
    def CouClosePercent(self):
        #cou_end_list = [i[3] for i in self.srcd_table[5:] if i[3] != '-' and time.strftime('%m', time.strptime(i[3], '%Y-%m-%d')) == self._GetFormMon()]
        cou_end_list = []
        for i in self.srcd_table[5:]:
            if i[3] != '-' and i[2] != '-' and time.strftime('%m', time.strptime(i[3], '%Y-%m-%d')) == self._GetFormMon():
                if self._TimeDiff(i[3], i[2]) > 0:
                    cou_end_list.append(i)

                
        cou_complete_list = [i for i in self.srcd_table[5:] if i[2] != '-' and time.strftime('%m', time.strptime(i[2], '%Y-%m-%d')) == self._GetFormMon()]
        #for i in cou_end_list:
        #    print(i)
        #print(cou_complete_list)
        self.data_dict['岗位成功关闭率'] = len(cou_end_list), len(cou_complete_list), '%.2f%%' %(len(cou_end_list) / len(cou_complete_list) * 100)

    # 创建offer申请数
    def CouCreateOffer(self):
        self.CCO = self.CRVP
        self.data_dict['创建offer数'] = self.CRVP,


    def GetDict(self):
        self.CouRecViolationPercent()
        self.CouPositions()
        self.CouPreScreen()
        self.CouPreScreenAverCyc()
        self.CouRecomRes()
        self.CouPrePassPercent()
        self.CouLevel()
        self.CouRecomResPass()
        self.CouRecomPassPercent()
        self.CouFilterResAverCyc()
        self.CouMeetResMulti()
        self.CouCreateInter()
        self.CouInvitePercent()
        self.CouInterPassPercent()
        self.CouAverageInterProcess()
        self.CouOfferAverage()
        self.CouAvgCreateOffer()
        self.CouOutOfferPercent()
        self.CouAverageArrival()
        self.CouClosePercent()
        self.CouCreateOffer()
        return self.data_dict
