import ast
import csv
import json
import random
import re
import smtplib, os, time
import traceback
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
import io
import logging

import requests
import sys

import xlrd


def logfile():
    # fp = io.StringIO()
    # traceback.print_stack(file=fp)
    # message = fp.getvalue()

    tim = time.strftime("%Y%m%d%H%M%S")
    logging.basicConfig(level=logging.DEBUG,            # 定义输出到文件的log级别，大于此级别的都被输出
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',# 定义输出log的格式
                        datefmt='%a, %d %b %Y %H:%M:%S',         # 时间
                        filename='../Logfile/'+tim+'.log',       # log文件名
                        filemode='w')                        # 写入模式“w”或“a”

    logging.debug('debug message')
    logging.info('info message')
    logging.warning('warning message')
    logging.error('error message')
    logging.critical('critical message')



def send_mail(n,report):
    """用于将测试报告发送到邮箱
      n== 1 时 添加附件
    :param
    smtp_dict = {
        "smtp_server": "发送邮件的smtp ex:smtp.126.com",
        "send_user": "发送邮件的邮箱 ex:am1122@126.com",
        "send_pwd": "发送邮件的邮箱密码 ex:mima",
        "sender": "发件人邮箱用于显示收到邮件中的发件人 ex:am1122@126.com",
        "receiver": "收件人邮箱 ex:zhangmin@hidtest.cn",多个收件人可以写成list
        "subject": "邮件主题 ex:自动化测试报告"
    }
    """
    smtp_dict = {
        "smtp_server": "smtp.163.com",  # 发送邮件服务器
        "send_user": "shaoxinlin5519@163.com",  # 发送邮件的邮箱账号
        "send_pwd": "159369sxl",  # 发送邮件的账号密码
        "sender": "shaoxinlin5519@163.com",
        "receiver": ['1260510655@qq.com','shaoxinlin@ajgs.cn'], # 收件邮箱地址
        "subject": "接口自动化测试报告\n"  # 邮件主题
    }

    # 获取测试报告的内容
    file = open(report, "rb")
    mail_body = file.read()
    print(mail_body)
    file.close()
    # 组装邮件内容
    msg=MIMEMultipart()
    # msg = MIMEText(mail_body, 'html', 'utf-8')
    msg['Subject'] = Header(smtp_dict["subject"], 'utf-8')
    msg['From'] = smtp_dict["send_user"]
    msg['to']=";".join(smtp_dict["receiver"])
    print(msg['to'])
    if n==1:
    #添加附件
        part = MIMEText(mail_body,'html',"utf-8")
        part.add_header('Content-Disposition', 'attachment', filename="接口自动化测试报告.html")
        msg.attach(part)
        msg.attach(MIMEText(mail_body, 'html', 'utf-8'))  ###将数据放到正文
    else:
        msg.attach(MIMEText(mail_body, 'html', 'utf-8'))###将数据放到正文
    # 发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(smtp_dict["smtp_server"])
        smtp.login(smtp_dict["send_user"], smtp_dict["send_pwd"])
        smtp.sendmail(msg['From'],msg['to'], msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as se:
        print("邮件发送失败！！")
        print(se)
        raise se

def screen_shot(driver):
    """用于测试用例执行过程中的截图
    :param
    第一个当然是driver对象，
    第二个是保存的图片文件名，不用输.png"""

    top_dir = "../report/image/"
    times = time.strftime("%Y%m%d%H%M%S")
    image_file = top_dir + times + ".png"
    driver.get_screenshot_as_file(image_file)



def set_data(data):
    """
    将data转换成字典
    :param data:
    :return:
    """
    d = {}
    if data!='null':
        for param in data.split('&'):
            k, v = param.split('=')
            d[k]=v
        return d
    else:
        return d


def find_update_data_01(r,data,*n):
    """
        以json格式匹配
        例：匹配 "token":"8b63876034ab4a22bbbd4c28a1d74399"
        :param r:需要匹配的json格式key值（元组）
        :param data: 匹配的数据
        :param n:n=1时返回匹配全部数据
        :return:
    """
    list_1=[]
    data=json.loads(data)
    data_1=data
    for a in r:
        if isinstance(data_1,list):
            for s in range(len(data_1)):
                list_1+=set_list(data_1[s][a])
            data_1=list_1
            list_1=[]
        elif isinstance(data_1,dict):
            data_1=data_1[a]
    if n[0]==1:
        k=random.randint(0,len(data_1) - 1)
        data_1 = data_1[k]
    return data_1


def req(method,url,header,data):
    if method=='post':
        # r=requests.post(url=url,headers=header,data=data,timeout=timeout,verify=False)
        r = requests.post(url=url, headers=header, data=data,verify=False)
    elif method=='get':
        # r=requests.get(url=url,headers=header,data=data,timeout=timeout)
        r = requests.get(url=url, headers=header, data=data,verify=False)
    return r

def set_list(data):
    """
    将参数转变为list
    :return:
    """
    a=[]
    if type(data)==str:
        a.append(data)
        return a
    elif isinstance(data,dict):
        a.append(data)
        return a
    else:
        return data

def write_csv(data,*name,filename,n):
    """
    将爬取的数据写入CSV文件
    :param data:写入的数据
    :param name:csv文件列名
    :param filename:csv文件名
    :return:
    """
    list1=[]
    if n==1:
        if os.path.exists('./data_file/'+filename+'.csv'):
            os.remove('./data_file/'+filename+'.csv')
    with open('./data_file/'+filename+'.csv', 'a+',newline='') as f:
        csv_write = csv.writer(f)
        if n==1:
            csv_write.writerow(name)
        for i in data:
            print(i)
            list1.append(str(i[0]))
            for j in i[1].split(','):
                list1.append(j)
            list1.append(str(i[2]))
            csv_write.writerow(list1)
            list1=[]

def re_data(i,data):
    """

    :param i: 正则表达式
    :param data: 匹配的数据
    :return: 匹配成功的数据
    """
    re_str = re.compile(i)
    re_data=re_str.findall(data)
    # print(re_data)
    return re_data

def get_all_data(filepath):
    """
    获取所有数据
    返回excel所有shell的数据
    :return:
    """

    cases = dict()
    sheet_data = []
    path = os.path.split(sys.path[0])[0]
    excel = xlrd.open_workbook(path+filepath)
    # excel = xlrd.open_workbook(path+"/datafile/data_file.xls")###更换文件

    # excel = xlrd.open_workbook(path + "/datafile/data_file_01.xls")###本地运行
    for sheet in excel.sheets():
        for n in range(2, sheet.nrows):
            sheet_data.append(dict(zip(sheet.row_values(1), sheet.row_values(n))))
        cases[sheet.name] = sheet_data
    return cases


def altel_data(data):
    """
    组装data ，需要改变变量类型
    :param data:
    :return:
    """
    data =ast.literal_eval(data)
    return data