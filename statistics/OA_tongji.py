"""
OA 系统统计
"""
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

import ast
import json
import re
from datetime import datetime,date,timedelta

from bson import ObjectId

from db_file import DB
from statistics.yunying_tongji import test_tongji

from configHttp import ConfigHttp

import urllib3
urllib3.disable_warnings()
class test_OA():
    machert_list = []
    list_name = []

    def machert_name(self,id):
        """
        查询商家名称
        :return:
        """
        database = DB()
        sql_1 = {"_id": ObjectId(id)}
        machert_name = database.connect_mongodb_all('tb_merchant', 1, sql_1)
        m_n = machert_name.get('storeName')##店铺名称
        m_time=str(machert_name.get('firstDate'))###入驻时间
        m_contracts = str(machert_name.get('contracts'))#联系人
        m_phone = str(machert_name.get('phone'))  # 联系方式
        m_detail= str(machert_name.get('addressDetail')['country'])+str(machert_name.get('addressDetail')['province'])+str(machert_name.get('addressDetail')['city'])+str(machert_name.get('addressDetail')['area'])+str(machert_name.get('addressDetail')['detail'])##地址

        return m_n,m_time,m_contracts,m_phone,m_detail

    def oa_id(self,name,n):
        """
        查找当前账号的所有子账号
        :param name: 当前账号
        :param n: 1：为管理员，2为非管理员
        :return:
        """
        list_id=[]
        id=''
        database = DB()
        nu=0
        if n==1:####平台账号，区域账号
            sql_name = {"accountNumber": name, "isDelete": False}

            id = database.connect_mongodb_all('tb_oa_user', 1, sql_name)
            idlist = id['authPermissionList']
            for id in idlist:
                sql={"name" : "平台"}
                areoa = database.connect_mongodb_all('tb_oa_area', 1, sql)
                if str(id) != str(areoa['_id']):##过滤平台ID
                    sql2 = {"areaOAId": ObjectId(id),"isDelete" : False}
                    areoa_id2 = database.connect_mongodb_all('tb_oa_area', 4, sql2)  ##分区ID
                    for id_1 in areoa_id2:
                        id = id_1['_id']
                        list_id.append(id)
            print('分区ID：%s'%list_id)
            for id in list_id:
                sql3={"areaOA" : ObjectId(id),"isDelete" : False}
                print(sql3)
                areoa_id3 = database.connect_mongodb_all('tb_oa_user', 4, sql3)
                for name in areoa_id3:
                    n_id=name['accountNumber']
                    self.list_name.append(n_id)
            print(self.list_name)
            nu=len(self.list_name)
        else:
            self.list_name.append(name)
            sql_name={"accountNumber" : name,"isDelete" : False}

            id=database.connect_mongodb_all('tb_oa_user', 1, sql_name)
            id = id['areaOA']
            sql_areaOA = {"areaOA": ObjectId(id),"isDelete" : False}
            nu=database.connect_mongodb_all('tb_oa_user', 3, sql_areaOA)

        print('团队人数%d'%(nu))

    def machert_nu(self):
        """
        测试统计当前账号签约超市数量
        :return:
        """
        # re_str=re.compile("ObjectId('(.*?)')")
        mac_nn=0
        for name in self.list_name:
            sql = [{'$lookup':{'from':'tb_manage_user','localField':'salesManager','foreignField':'_id','as':'manage_user'}},{'$unwind': '$manage_user'},
                             {'$lookup':{'from':'tb_oa_user','localField':'manage_user._id','foreignField':'manageUser','as':'manage'}},{'$unwind': '$manage'},
                             {'$match':{'$and':[{"manage.accountNumber" : name},{"isdelete" : False}]}},{'$group': {"_id": '$customer', 'number': {'$sum': 1}}}]

            sql_1 = [{'$lookup': {'from': 'tb_manage_user', 'localField': 'salesManager', 'foreignField': '_id',
                                'as': 'manage_user'}}, {'$unwind': '$manage_user'},
                   {'$lookup': {'from': 'tb_oa_user', 'localField': 'manage_user._id', 'foreignField': 'manageUser',
                                'as': 'manage'}}, {'$unwind': '$manage'},
                   {'$match': {'$and':[{"manage.accountNumber": name},{"isdelete" : False}]}}]
            database = DB()
            machert=database.connect_mongodb_all('tb_merchant',2,sql)

            for mac in machert:
                # print(int(mac['number']))
                mac_nn=mac_nn+int(mac['number'])


            if mac_nn > 0:
                mac_id=database.connect_mongodb_all('tb_merchant',2,sql_1)
                # print(mac_id)
                for n in mac_id:
                    machert_id=str(n.get('_id'))
                    # id_s=re_str.findall(machert_id)
                    self.machert_list.append(machert_id)
        print('当前账号签约数量为：%d' % mac_nn)
        # print(self.machert_list)
        # print(len(self.machert_list))

    def count_sales_amount(self):
        """
        统计当前账号流水（所有）
        :return:
        """

        database = DB()
        count_amount=0
        if len(self.machert_list)>0:
            print(self.machert_list)
            for id in self.machert_list:
                self.count=0
                sql = [{'$match': {'$and': [{"supplier": ObjectId(id)},
                                            {"payTime": {'$ne': None}}]}},
                       {'$group': {'_id': '销售总额', 'total': {'$sum': '$totalPrice'}, 'transPrice': {'$sum': '$transPrice'}}}]

                all=database.connect_mongodb_all('tb_order',2,sql)
                for i in all:
                    self.total = float(str(i.get('total')))  ##订单总额
                    self.transPrice = float(str(i.get('transPrice')))  ###运费总额
                    self.count=self.total + self.transPrice
                    # print(self.count)
                m_n=self.machert_name(id)[0]
                print('%s流水为：%.2f'%(m_n,self.count))
                count_amount = self.count + count_amount
            print('######################################当前账号流水为%.2f ###################'%count_amount)
        else:
            print('######################################当前账号流水为：0 ###################')

    def resultful_count_sales_amount(self):
        """
        统计当前账号有效流水（有粮票生成订单）
        :return:
        """
        database = DB()
        count_amount = 0
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                self.count = 0
                sql = [{'$match': {'$and': [{"supplier": ObjectId(id)},{"payTime": {'$ne':None}}]}},
                       {'$lookup':{'from':'tb_order_detail','localField':'_id','foreignField':'order','as':'orderDetail'}},
                       {'$lookup':{'from':'tb_red_packet','localField':'orderDetail._id','foreignField':'orderDetail','as':'red_packet'}},{'$unwind': '$red_packet'},
                       {'$match': {'$and': [{"red_packet.money":{'$gt':0}}]}},
                       {'$group': {'_id': '$_id', "supplier":{'$first':"$supplier"},'totalPrice': {'$first': '$totalPrice'}, 'transPrice': {'$first': '$transPrice'}}},
                       {'$group': {'_id': '$supplier', 'total': {'$sum': '$totalPrice'}, 'transPrice': {'$sum': '$transPrice'}}}]
                all = database.connect_mongodb_all('tb_order', 2, sql)
                for i in all:
                    self.total = float(str(i.get('total')))  ##订单总额
                    self.transPrice = float(str(i.get('transPrice')))  ###运费总额
                    self.count = self.total + self.transPrice
                m_n = self.machert_name(id)[0]
                print('%s有效流水为：%.2f' % (m_n, self.count))
                count_amount = self.count + count_amount
            print('######################################当前账号有效流水为%.2f ###################' % count_amount)
        else:
            print('######################################当前账号有效流水为：0 ###################')

    def all_data(self):
        database = DB()

        if len(self.machert_list) > 0:
            for id in self.machert_list:
                self.machert_details_1(database,id)
                self.machert_details_2(database, id)
                self.machert_details_3(database, id)
                # self.machert_details_4(database, id)
                self.count_sales_amount_no(database, id)
                self.count_sales_n(0,1,database, id)
                self.count_sales_n(1, 7,database, id)
                self.count_sales_n(1, 30,database, id)
                self.count_user(0,1,database, id)
        else:
            print('暂无商家')

    def machert_details_1(self,database,id):
        """
        商家详情---基本信息
        :return:
        """
        # database = DB()
        #
        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:

        machert_ID = [{'$match': {'$and':[{"merchant" : ObjectId(id)},
                                          {'merchantUserType':{'$ne':'SUB_ACCOUNT'}}]}}]

        m_name=self.machert_name(id)[0]
        m_time=self.machert_name(id)[1]
        m_contracts=self.machert_name(id)[2]
        m_phone=self.machert_name(id)[3]
        m_detail=self.machert_name(id)[4]
        print('#####################################################  %s（%s）  #######################################'%(id,m_name))
        print('############################## 基本信息 #############################')
        print('##### 入驻时间：%s'%(m_time))
        print('##### 联系人：%s'%(m_contracts))
        print('##### 联系方式：%s' % (m_phone))
        print('##### 地址：%s' % (m_detail))
        machertID=database.connect_mongodb_all('tb_manage_user',2,machert_ID)
        if machertID.__dict__['_CommandCursor__data']!=None:
            for us in machertID.__dict__['_CommandCursor__data']:
                m_id=str(us.get('username'))
                print('##### 商家账号：%s' % (m_id))
                m_type = str(us.get('isEnable'))
                if m_type == 'True':
                    print('##### 账号状态为：已开通')
                elif m_type == 'False':
                    print('##### 账号状态为：已禁用')
        else:
            print('##### 商家账号：无')
            print('##### 账号状态为：无')
        # else:
        #     print('暂无商家')

    def machert_details_2(self,database,id):
        """
        商家详情---店铺信息
        :return:
        """
        # database = DB()

        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:
        print('############################## 店铺信息 ##############################')
        machert_ID = {"_id": ObjectId(id)}
        m_name=self.machert_name(id)[0]
        print('#####店铺名称：%s'%m_name)
        machertID=database.connect_mongodb_all('tb_merchant',1,machert_ID)
        if machertID!=None:
            if machertID['isdelete']==False:
                if machertID.get('valid')==True:
                    print('#####店铺状态：已启用')
                else:
                    print('#####店铺状态：已禁用')
            else:
                print('#####%s 店铺状态：已删除'%id)
            try:
                if machertID['isOpenNoOrderPay'] ==True:
                    print('##### 无订单支付：已开启')
                else:
                    print('##### 无订单支付：未开启')
            except:
                print('##### 无订单支付：未开启')
            try :
                if machertID['isOpenBalanceDeduction']==True:
                    print('##### 余额抵扣：已开启')
                else:
                    print('##### 余额抵扣：未开启')
            except:
                print('##### 余额抵扣：未开启')

        else:
            print('暂无商家')
            print('暂无商家')
        # else:
        #     print('暂无商家')

    def machert_details_3(self,database,id):
        """
        商家详情---结算信息
        :return:
        """
        # database = DB()
        # wait=0
        set_in=0
        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:
        print('############################## 结算信息 ##############################')
        ##银行卡信息
        bank = [{'$lookup':{'from':'tb_company_blank','localField':'company','foreignField':'company','as':'company_blank'}},{'$unwind': '$company_blank'},
                   {'$match': {"_id": ObjectId(id)}}]
        ##冻结中
        no_order_set=[{'$match': {'$and':[{"orderType" : "NO_ORDER_PAY"},{"orderStatus" : "ORDER_FINISH"},{"supplier" : ObjectId(id)}]}}]
        ##可结算
        wait_set=[{'$match': {'$and': [{"orderType": "NO_ORDER_PAY"}, {"settlementStatus": "STAY_SETTLEMENT"},
                                         {"payTime": {'$ne': None}}, {"supplier": ObjectId(id)}]}}]
        ##结算中
        set_ing=[{'$match': {'$and':[{"settlementType" : "NO_ORDER_PAY"},{'$or':[{"settlementStatus" : "STAY_SETTLEMENT"},{"settlementStatus" : 'MIDDLE_SETTLEMENT'}]},{"merchant" : ObjectId(id)}]}},
                    {'$group': {'_id': '结算中总额', 'total': {'$sum': '$shouldMoney'}}}]
        c_bank=database.connect_mongodb_all('tb_merchant',2,bank)
        for bank_n in c_bank:
            try:
                bankNo=bank_n['company_blank']['blankNo'] + ':'+bank_n['company_blank']['blankName']

                print('##### 结算银行卡：%s'%(bankNo))
            except KeyError as e:
                print('##### 结算银行卡：无(%s)' % (e))
            try:
                weChatNO=bank_n['weChatNO']
                print('##### 结算微信昵称：%s'%(weChatNO))
            except KeyError as e:
                print('##### 结算微信昵称：无(%s)'%(e))
        c_no_order_set = database.connect_mongodb_all('tb_order', 2, no_order_set)
        set=0##结算中
        wait=0
        for no in c_no_order_set.__dict__['_CommandCursor__data']:
            # print(no['_id'])
            now = datetime.now()  ##当前时间
            # paytime=datetime.strptime(str(no['payTime']),'%Y-%m-%d %H:%M:%S')
            paytime=no['payTime']
            try:
                noOrderPaySettlementDelay=no['noOrderPaySettlementDelay'] * 3600
            except:
                noOrderPaySettlementDelay=0
            if now < paytime+ timedelta(seconds=noOrderPaySettlementDelay):
                set=set+float(str(no['totalPrice']))
                print(str(no['totalPrice']))
        print('##### 冻结中：%.2f'%(set))
        try:
            wait_set_money = database.connect_mongodb_all('tb_order', 2, wait_set)
            for no in wait_set_money.__dict__['_CommandCursor__data']:
                # print(no['_id'])
                now1 = datetime.now()  ##当前时间
                # paytime=datetime.strptime(str(no['payTime']),'%Y-%m-%d %H:%M:%S')
                paytime = no['payTime']
                try:
                    noOrderPaySettlementDelay = no['noOrderPaySettlementDelay'] * 3600
                except:
                    noOrderPaySettlementDelay = 0
                if now1 >= paytime + timedelta(seconds=noOrderPaySettlementDelay):
                    wait = wait + float(str(no['totalPrice']))
            print('##### 可结算：%.2f' % (wait))
        except :
            print('##### 可结算--报错：%.2f' % (wait))

        seting_money = database.connect_mongodb_all('tb_settlement', 2, set_ing)
        for i in seting_money:
            set_in=float(str(i['total']))
        print('##### 结算中：%.2f' % (set_in))

        # else:
        #     print('暂无商家')

    # def machert_details_4(self,database,id):
    #     """
    #     商家详情---结算信息
    #     :return:
    #     """
    #     # database = DB()
    #     wait=0
    #     # set_in=0
    #     # if len(self.machert_list) > 0:
    #     #     for id in self.machert_list:
    #     print('############ 结算信息')
    #     ##可结算
    #     wait_set = [{'$match': {'$and': [{"orderType": "NO_ORDER_PAY"}, {"settlementStatus": "STAY_SETTLEMENT"},
    #                                      {"payTime": {'$ne': None}}, {"supplier": ObjectId(id)}]}}]
    #     wait_set_money = database.connect_mongodb_all('tb_order', 2, wait_set)
    #     for no in wait_set_money.__dict__['_CommandCursor__data']:
    #         # print(no['_id'])
    #         now1 = datetime.now()  ##当前时间
    #         # paytime=datetime.strptime(str(no['payTime']),'%Y-%m-%d %H:%M:%S')
    #         paytime = no['payTime']
    #         try:
    #             noOrderPaySettlementDelay = no['noOrderPaySettlementDelay'] * 3600
    #         except:
    #             noOrderPaySettlementDelay = 0
    #         if now1 >= paytime + timedelta(seconds=noOrderPaySettlementDelay):
    #             wait = wait + float(str(no['totalPrice']))
    #     print('#####%s 可结算：%.2f' % (id, wait

    def count_sales_amount_no(self,database,id):
        # database = DB()
        GoodsPay=0
        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:
        print('############################## 销售数据 ##############################')
        sql1=[{'$match': {'$and': [{"payTime": {'$ne': None}},{"supplier" : ObjectId(id)}]}},
         {'$group': {'_id': '', 'sumGoodsPay': {'$sum': "$totalPrice"},
                     'sumTransPay': {'$sum': "$transPrice"}}}]

        total = database.connect_mongodb_all('tb_order', 2, sql1)
        for i in total:
            GoodsPay=float(str(i['sumGoodsPay']))+float(str(i['sumTransPay']))
        print('##### 累计销售额%.2f'%(GoodsPay))

    def count_sales_n(self,n,nu,database,id):
        # database = DB()
        tongji = test_tongji()
        Pay=0
        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:
        sql = [{'$match': {'$and': [{"orderTime": {'$gte': tongji.get_time(n, nu)[0]}},
                                    {"orderTime": {'$lte': tongji.get_time(n, nu)[1]}},
                                    {"payTime": {'$ne': None}}, {"supplier" : ObjectId(id)}]}},
               {'$group': {'_id': '', 'sumGoodsPay': {'$sum': "$totalPrice"},
                           'sumTransPay': {'$sum': "$transPrice"}}}]
        total = database.connect_mongodb_all('tb_order', 2, sql)
        for i in total:
            Pay = float(str(i['sumGoodsPay']))+float(str(i['sumTransPay']))
        print('##### 近%d销售额%.2f' % (nu,Pay))


    def count_user(self,n,nu,database,id):
        # database = DB()
        tongji = test_tongji()
        new_shop_user=0
        more_shop_users=0
        pay_shop_users=0
        ####新门客
        # if len(self.machert_list) > 0:
        #     for id in self.machert_list:
        print('############################## 用户数据 ##############################')
        shop_new_user = [{'$match': {'$and': [{'$or': [{"orderStatus": "ORDER_FINISH"},
                                                       {"orderStatus": "ORDER_WAIT_DELIVER"},
                                                       {"orderStatus": "ORDER_WAIT_RECEIVE"}]},
                                              {"supplier": ObjectId(id)}, {"orderTime": {'$gte': tongji.get_time(n, nu)[0]}},
                                              {"orderTime": {'$lte': tongji.get_time(n, nu)[1]}}]}},
                         {'$group': {"_id": '$customer', 'number': {'$sum': 1}}}, {'$match': {'number': {'$lte': 1}}},
                         {'$count': 'countNum'}]
        new_shop_users = database.connect_mongodb_all('tb_order', 2,shop_new_user)
        for i in new_shop_users:
            new_shop_user = int(str(i.get('countNum')))
        print(' %d天新用户数：%d' % (nu, new_shop_user))
        #####收藏店铺数
        collects_shop = {'$and': [{"collection_id": ObjectId(id)}, {"type": "MERCHANT"}]}
        collect_shop = database.connect_mongodb_all('tb_collection', 3,collects_shop)
        print('店铺关注总数：%d' % (collect_shop))
        #####复购用户数
        more_user = [{'$match': {'$and': [{'$or': [{"orderStatus": "ORDER_FINISH"},
                                                   {"orderStatus": "ORDER_WAIT_DELIVER"},
                                                   {"orderStatus": "ORDER_WAIT_RECEIVE"}]},
                                          {"supplier": ObjectId(id)}]}},
                     {'$group': {"_id": '$customer', 'number': {'$sum': 1}}},
                     {'$match': {'number': {'$gt': 1}}}, {'$count': 'countNum'}]
        shop_users = database.connect_mongodb_all('tb_order', 2,more_user)
        for i in shop_users:
            more_shop_users = int(str(i.get('countNum')))
        print('商家复购用户数：%d' % (more_shop_users))
        pay_user = [{'$match': {'$and': [{'$or': [{"orderStatus": "ORDER_FINISH"},
                                                   {"orderStatus": "ORDER_WAIT_DELIVER"},
                                                   {"orderStatus": "ORDER_WAIT_RECEIVE"}]},
                                          {"supplier": ObjectId(id)}]}},
                     {'$group': {"_id": '$customer', 'number': {'$sum': 1}}},{'$count': 'countNum'}]
        shop_users = database.connect_mongodb_all('tb_order', 2, pay_user)
        for i in shop_users:
            pay_shop_users = int(str(i.get('countNum')))
        print('商家下单用户数：%d' % (pay_shop_users))

    def order_goods(self,name):
        """
        风控比
        :return:
        """
        print('############################## 风控比 ##############################')
        configHttp=ConfigHttp()
        host='https://oaapiha.godteam.net/'
        url=host+'loginOA/manageLogin?'+'username='+name+'&passWord=123456'
        data=configHttp.set_data('username=sxl123&passWord=123456')

        header=''

        loginCode=configHttp.req('get',url,header,data)
        # print(loginCode.text)
        loginCode=loginCode.json()['data']['loginCode']
        # print(loginCode)
        # +'username=sxl123&passWord=123456'
        url1='indexOA/getMerchantsData'
        data1=configHttp.set_data('sortType=riskControlValue&sortMode=[{"riskControlValue":1,"moneyRecords":1,"goodMoneyRecords":1,"placeGoods":1,"incomeTime":1}]&' \
                                         'adFee=3')
        header1={}
        header1['loginCode']=loginCode
        header1['Referer']='https://oa.godteam.net/home/main'

        url2=host+url1
        # header1=ast.literal_eval({'loginCode':123456})
        resp=configHttp.req('get',url2,header1,data1)
        # print(resp.headers)
        # print(resp.json())
        for i in range(0,len(resp.json()['data']['merchantDatas'])-1):
            placeGood=resp.json()['data']['merchantDatas'][i]['placeGoodsMoney']
            placeGood =float(placeGood) if float(placeGood)>0 else 1
            settingRisk=resp.json()['data']['merchantDatas'][i]['settingRiskValue']
            n=float(settingRisk)/float(placeGood)
            merchantId=resp.json()['data']['merchantDatas'][i]['merchantId']
            print("#################################")
            print('%s 订货金额%.2f'%(merchantId,placeGood))
            print('%s 该商家的风控比%.2f'%(merchantId,n))
            print('%s 该商家设置的风控值%.2f'%(merchantId,float(settingRisk)))


if __name__ == "__main__":
    obj=test_OA()
    obj.oa_id('zzzzz', 1)
    obj.machert_nu()
    obj.count_sales_amount()
    obj.resultful_count_sales_amount()
    obj.all_data()
    # obj.machert_details_1()
    # obj.machert_details_2()
    # obj.machert_details_3()
    # obj.count_sales_amount_no()
    # obj.count_sales_n(0,1)
    # obj.count_sales_n(1, 7)
    # obj.count_sales_n(1, 30)
    # obj.count_user(0,1)
    obj.order_goods('qqqqq')

