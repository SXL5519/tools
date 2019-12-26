"""
OA 系统统计
"""
import re
from datetime import datetime,date,timedelta

from bson import ObjectId

from db_file import DB
from statistics.yunying_tongji import test_tongji

from statistics.shop_tongji import test_shop_tongji


class test_OA():
    machert_list = ['5e04628eb563574a3b28fab7']

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
        m_detail= str(machert_name.get('detail'))##地址

        return m_n,m_time,m_contracts,m_phone,m_detail


    def machert_nu(self):
        """
        测试统计当前账号签约超市数量
        :return:
        """
        # re_str=re.compile("ObjectId('(.*?)')")

        sql = {"salesManager": "800688744572"}
        database = DB()
        mac_nn=database.connect_mongodb_all('tb_merchant',3,sql)
        print('当前账号签约数量为：%d'%mac_nn)
        if mac_nn > 0:
            mac_id=database.connect_mongodb_all('tb_merchant',4,sql)
            print(mac_id)
            for n in mac_id:
                machert_id=str(n.get('_id'))
                # id_s=re_str.findall(machert_id)
                self.machert_list.append(machert_id)
        print(self.machert_list)

    def count_sales_amount(self):
        """
        统计当前账号流水（所有无订单）
        :return:
        """

        database = DB()
        count_amount=0
        if len(self.machert_list)>0:
            for id in self.machert_list:
                self.count=0
                sql = [{'$match': {'$and': [{"supplier": ObjectId(id)},{"orderType" : "NO_ORDER_PAY"},
                                            {"payTime": {'$ne': None}}]}},
                       {'$group': {'_id': '销售总额', 'total': {'$sum': '$totalPrice'}, 'transPrice': {'$sum': '$transPrice'}}}]

                all=database.connect_mongodb_all('tb_order',2,sql)
                for i in all:
                    self.total = float(str(i.get('total')))  ##订单总额
                    self.transPrice = float(str(i.get('transPrice')))  ###运费总额
                    self.count=self.total + self.transPrice
                m_n=self.machert_name(id)[0]
                print('%s流水为：%.2f'%(m_n,self.count))
                count_amount = self.count + count_amount
            print('######################当前账号流水为%.2f'%count_amount)
        else:
            print('######################当前账号流水为：0')

    def resultful_count_sales_amount(self):
        """
        统计当前账号有效流水（有粮票生成无订单）
        :return:
        """
        database = DB()
        count_amount = 0
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                self.count = 0
                sql = [{'$lookup':{'from':'tb_order_detail','localField':'orderDetail','foreignField':'_id','as':'orderDetail'}},{'$unwind': '$orderDetail'},
                            {'$lookup':{'from':'tb_order','localField':'orderDetail.order','foreignField':'_id','as':'order'}},{'$unwind': '$order'},
                            {'$match': {'$and': [{"order.supplier": ObjectId(id)},{"orderType" : "NO_ORDER_PAY"}]}},
                            {'$group': {'_id': '销售总额', 'total': {'$sum': '$order.totalPrice'}, 'transPrice': {'$sum': '$order.transPrice'}}}]

                all = database.connect_mongodb_all('tb_red_packet', 2, sql)
                for i in all:
                    self.total = float(str(i.get('total')))  ##订单总额
                    self.transPrice = float(str(i.get('transPrice')))  ###运费总额
                    self.count = self.total + self.transPrice
                m_n = self.machert_name(id)[0]
                print('%s有效流水为：%.2f' % (m_n, self.count))
                count_amount = self.count + count_amount
            print('######################当前账号有效流水为%.2f' % count_amount)
        else:
            print('######################当前账号有效流水为：0')

    def machert_details_1(self):
        """
        商家详情---基本信息
        :return:
        """
        database = DB()

        if len(self.machert_list) > 0:
            for id in self.machert_list:
                print('############ 基本信息')
                machert_ID = {"merchant": ObjectId(id)}

                m_name=self.machert_name(id)[0]
                m_time=self.machert_name(id)[1]
                m_contracts=self.machert_name(id)[2]
                m_phone=self.machert_name(id)[3]
                m_detail=self.machert_name(id)[4]
                print('#######################  %s  #############'%m_name)
                print('#####%s 入驻时间：%s'%(id,m_time))
                print('#####%s 联系人：%s'%(id,m_contracts))
                print('#####%s 联系方式：%s' % (id,m_phone))
                print('#####%s 地址：%s' % (id,m_detail))
                machertID=database.connect_mongodb_all('tb_manage_user',1,machert_ID)
                if machertID!=None:
                    m_id=str(machertID.get('username'))
                    print('#####%s 商家账号：%s' % (id,m_id))
                    m_type = str(machertID.get('isEnable'))
                    if m_type == 'True':
                        print('#####%s 账号状态为：已开通'%id)
                    elif m_type == 'False':
                        print('#####%s 账号状态为：已禁用'%id)
                else:
                    print('#####%s 商家账号：无'%id)
                    print('#####%s 账号状态为：无'%id)
        else:
            print('暂无商家')

    def machert_details_2(self):
        """
        商家详情---店铺信息
        :return:
        """
        database = DB()

        if len(self.machert_list) > 0:
            for id in self.machert_list:
                print('############ 店铺信息')
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
                    if machertID['isOpenNoOrderPay'] ==True:
                        print('#####%s 无订单支付：已开启'%id)
                    else:
                        print('#####%s 无订单支付：未开启'%id)
                    if machertID['isOpenBalanceDeduction']==True:
                        print('#####%s 余额抵扣：已开启'%id)
                    else:
                        print('#####%s 余额抵扣：未开启'%id)

                else:
                    print('暂无商家')
                    print('暂无商家')
        else:
            print('暂无商家')

    def machert_details_3(self):
        """
        商家详情---结算信息
        :return:
        """
        database = DB()
        wait_money=0
        set_in=0
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                print('############ 结算信息')
                ##银行卡信息
                bank = [{'$lookup':{'from':'tb_company_blank','localField':'company','foreignField':'company','as':'company_blank'}},{'$unwind': '$company_blank'},
                           {'$match': {"_id": ObjectId(id)}}]
                ##冻结中
                no_order_set=[{'$match': {'$and':[{"orderType" : "NO_ORDER_PAY"},{"orderStatus" : "ORDER_FINISH"},{"supplier" : ObjectId(id)}]}}]
                ##可结算
                wait_set=[{'$match': {'$and':[{"settlementType" : "NO_ORDER_PAY"},{"settlementStatus" : "STAY_SETTLEMENT"},{"merchant" : ObjectId(id)}]}},
                            {'$group': {'_id': '待结算总额', 'total': {'$sum': '$shouldMoney'}}}]
                ##结算中
                set_ing=[{'$match': {'$and':[{"settlementType" : "NO_ORDER_PAY"},{"settlementStatus" : "MIDDLE_SETTLEMENT"},{"merchant" : ObjectId(id)}]}},
                            {'$group': {'_id': '结算中总额', 'total': {'$sum': '$shouldMoney'}}}]
                c_bank=database.connect_mongodb_all('tb_merchant',2,bank)
                for bank_n in c_bank:
                    try:
                        bankNo=bank_n['company_blank']['blankNo']
                        print('#####%s 结算银行卡：%s'%(id,bankNo))
                    except KeyError as e:
                        print('#####%s 结算银行卡：无(%s)' % (id,e))
                    try:
                        weChatNO=bank_n['weChatNO']
                        print('#####%s 结算微信昵称：%s'%(id,weChatNO))
                    except KeyError as e:
                        print('#####%s 结算微信昵称：无(%s)'%(id,e))
                c_no_order_set = database.connect_mongodb_all('tb_order', 2, no_order_set)
                now=datetime.now() ##当前时间
                set=0##结算中
                for no in c_no_order_set:
                    # paytime=datetime.strptime(str(no['payTime']),'%Y-%m-%d %H:%M:%S')
                    paytime=no['payTime']
                    noOrderPaySettlementDelay=no['noOrderPaySettlementDelay'] * 3600
                    if now < paytime+ timedelta(seconds=noOrderPaySettlementDelay):
                        set=set+no['totalPrice']
                print('#####%s 冻结中：%.2f'%(id,set))
                wait_set_money=database.connect_mongodb_all('tb_settlement', 2, wait_set)
                for i in wait_set_money:
                    wait_money=i['total']
                print('#####%s 可结算：%.2f'% (id,wait_money))
                seting_money = database.connect_mongodb_all('tb_settlement', 2, set_ing)
                for i in seting_money:
                    set_in=i['total']
                print('#####%s 结算中：%.2f' % (id,set_in))

        else:
            print('暂无商家')

    def count_sales_amount_no(self):
        database = DB()
        GoodsPay=0
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                print('############ 销售数据')
                sql1=[{'$match': {'$and': [{"payTime": {'$ne': None}},{"orderType" : "NO_ORDER_PAY"},{"supplier" : ObjectId(id)}]}},
                 {'$group': {'_id': '', 'sumGoodsPay': {'$sum': "$totalPrice"},
                             'sumTransPay': {'$sum': "$transPrice"}}}]

                total = database.connect_mongodb_all('tb_order', 2, sql1)
                for i in total:
                    GoodsPay=float(str(i['sumGoodsPay']))+float(str(i['sumTransPay']))
                print('#####%s 累计销售额%.2f'%(id,GoodsPay))

    def count_sales_n(self,n,nu):
        database = DB()
        tongji = test_tongji()
        Pay=0
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                sql = [{'$match': {'$and': [{"orderTime": {'$gte': tongji.get_time(n, nu)[0]}},
                                            {"orderTime": {'$lte': tongji.get_time(n, nu)[1]}},
                                            {"payTime": {'$ne': None}}, {"orderType": "NO_ORDER_PAY"},{"supplier" : ObjectId(id)}]}},
                       {'$group': {'_id': '', 'sumGoodsPay': {'$sum': "$totalPrice"},
                                   'sumTransPay': {'$sum': "$transPrice"}}}]
                total = database.connect_mongodb_all('tb_order', 2, sql)
                for i in total:
                    Pay = float(str(i['sumGoodsPay']))+float(str(i['sumTransPay']))
                print('#####%s 近%d销售额%.2f' % (id,nu,Pay))


    def count_user(self,n,nu):
        database = DB()
        tongji = test_tongji()
        new_shop_user=0
        more_shop_users=0
        pay_shop_users=0
        ####新门客
        if len(self.machert_list) > 0:
            for id in self.machert_list:
                print('############ 用户数据')
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
                print('%s  %d天新用户数：%d' % (id,nu, new_shop_user))
                #####收藏店铺数
                collects_shop = {'$and': [{"collection_id": ObjectId(id)}, {"type": "MERCHANT"}]}
                collect_shop = database.connect_mongodb_all('tb_collection', 3,collects_shop)
                print('%s 店铺关注总数：%d' % (id,collect_shop))
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
                print('%s 商家复购用户数：%d' % (id,more_shop_users))
                pay_user = [{'$match': {'$and': [{'$or': [{"orderStatus": "ORDER_FINISH"},
                                                           {"orderStatus": "ORDER_WAIT_DELIVER"},
                                                           {"orderStatus": "ORDER_WAIT_RECEIVE"}]},
                                                  {"supplier": ObjectId(id)}]}},
                             {'$group': {"_id": '$customer', 'number': {'$sum': 1}}},{'$count': 'countNum'}]
                shop_users = database.connect_mongodb_all('tb_order', 2, pay_user)
                for i in shop_users:
                    pay_shop_users = int(str(i.get('countNum')))
                print('%s 商家下单用户数：%d' % (id,pay_shop_users))

if __name__ == "__main__":
    obj=test_OA()
    obj.machert_nu()
    obj.count_sales_amount()
    obj.resultful_count_sales_amount()
    obj.machert_details_1()
    obj.machert_details_2()
    obj.machert_details_3()
    obj.count_sales_amount_no()
    obj.count_sales_n(0,1)
    obj.count_sales_n(1, 7)
    obj.count_sales_n(1, 30)
    obj.count_user(0,1)

