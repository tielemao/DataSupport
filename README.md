# DataSupport

## Explain

- 利用Python Flask Web框架搭建web站点
- 主要用于数据支持和采集，填入Google Sheets中
- 使用flask框架，python去读取邮箱中的附件，并填入相应的googlesheet表格文件中

## Version

- 目前版本为v1.0


## ENV

| Project | version | Description |
|---|---|---|
| python | 3.7 | None |
| Flask | 1.0.2 | web框架 |
| Flask-wtf | 0.14.2 | form表单插件 |
| Flask-Bootstrap | 3.3.7.1 | 优化html |
| Flask-Login | 0.4.1 | 登录插件 |
| Flask-SQLAIchemy | 2.3.2 | 数据库插件 |
| SQLAIchemy | 1.3.2 | 采取SQLite数据库 |
| supervisor | 4.0.2 | 监听相关进程，挂掉则重启 |
| Jinja2 | 2.1.0 | 模板引擎 |
| pygsheets | 2.0.2 | googlesheets API |
| pandas | 0.25.3 | 用于表格做科学计算 |
| xlsx2csv | 0.7.6 | 用于将表格转换成csv |
| xlrd | 1.2.0 | 处理表格 |
| numpy | 1.17.3 | 配合pandas做科学计算 |
| pypinyin | 0.36.0 | 文件名中文转拼音 |

## Route

| Route | Function | Methods | Description |
| --- | --- | --- | --- |
| '/' and '/index' | index | GET | 首页 |
| /login | login | GET,POST | 登录 |
| /logout | logout | GET | 注销 |
| /googlesheets | googlesheets | GET,POST | 采集数据导入GoogleSheets中 |
| /googlesheets2 | googlesheets2 | GET,POST | 导入数据到DataSource |


## Run
进入项目下，输入以下命令
`flask run -h 主机ip -P 端口`

* 例：
```python
(venv) flask run -h 127.0.0.1 -p 5000
 * Serving Flask app "data_support.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
127.0.0.1 - - [12/Apr/2019 16:30:11] "GET / HTTP/1.1" 302 -
127.0.0.1 - - [12/Apr/2019 16:30:11] "GET /login?next=%2F HTTP/1.1" 200 -
127.0.0.1 - - [12/Apr/2019 16:30:12] "GET /favicon.ico HTTP/1.1" 404 -
```

## Update Daily

### 2020-07-21

* 将敏感数据删除，上github展示代码用。



### 2019-11-05  tag v0.3 Demo

* 初步实现选择execl文件（数据源），填入GoogleSheets的表格文件名，填入sheets name（后两项可优化为不填则按默认的执行）。点击执行后则采集和处理数据后生成数据到相应的Google Sheets表格中。

### 2019-11-08
* 表格文件中文名转拼音
* 默认输入框为 "IT数据支持系统" 和 "0"
* 邮件附件获取

### 2019-11-15

* 定时获取邮件附件到uploads
* 扫描uploads目录发现符合条件（名字符合，日期天数相差为0）的则触发导入googlesheets
* 增加数据库保存每次处理完的json结果

### 2019-11-18  tag v0.5 Demo2

* 修复分析数据的bug
* 测试数据库添加正常，测试定时任务拉取邮件正常
* 添加和优化展示，现有两个页面控制，及返回json提示

### 2019-11-20

* hr添加周报和日报
* datasource和之前的统计表不再需要采集
* 周报只传一张统计表，月报需要两张表

##  ToDo

* [ ] 智能匹配相关的数据，以防表格有变后填入错误。
* [x] 邮件订阅服务，自动读取邮件附件后触发填入数据。
* [ ] 自动按日期或按季在Google Sheets上建表，建sheet。



