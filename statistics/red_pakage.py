from db_file import DB

class redpacket():
    """红包池运营后台促销统计"""

    def  total_amount(self):
        """
        普奖奖池总额
        :return:
        """
        self.total_money=0  ###所有规则总额
        self.del_total_money=0  ###删除规则剩余金额
        sum=[{'$group':{'_id':'金额总额','total':{'$sum':"$money"}}}]
        del_sum=[{'$match':{"isDelete" :True}},{'$group':{'_id':'删除规则总额','total':{'$sum':"$remainMoney"}}}]

        database = DB()
        ol=database.connect_mongodb_all('tb_redpond', 2,sum)
        self.total_money=float(database.get_data(ol,'total')[0])
        del_ol=database.connect_mongodb_all('tb_redpond', 2,del_sum)
        self.del_total_money=float(database.get_data(del_ol,'total')[0])
        total=self.total_money-self.del_total_money
        print('普奖奖池总额：%.2f'%total)

    def receive(self):
        """
        普奖奖池已被领取金额
        :return:
        """
        self.total_money = 0  ###所有规则总额
        self.surplus_money=0 ###所有规则剩余金额
        sum = [{'$group': {'_id': '金额总额', 'total': {'$sum': "$money"}}}]
        surplus_sum=[{'$group': {'_id': '剩余金额总额', 'total': {'$sum': "$remainMoney"}}}]
        database = DB()
        ol = database.connect_mongodb_all('tb_redpond', 2, sum)
        self.total_money = float(database.get_data(ol, 'total')[0])
        del_ol = database.connect_mongodb_all('tb_redpond', 2, surplus_sum)
        self.surplus_money = float(database.get_data(del_ol, 'total')[0])
        total = self.total_money - self.surplus_money
        print('已发放总额：%.2f' % total)

    def su_money(self):
        """
        奖池剩余金额
        :return:
        """
        self.total_money = 0  ###所有规则总额
        sum = [{'$match':{"isDelete" :False}},{'$group':{'_id':'剩余规则总额','total':{'$sum':"$remainMoney"}}}]
        database = DB()
        ol = database.connect_mongodb_all('tb_redpond', 2, sum)
        self.total_money = float(database.get_data(ol, 'total')[0])
        print('已发放总额：%.2f' % self.total_money)


if __name__ == "__main__":

    a=redpacket()
    a.total_amount()
    a.receive()
    a.su_money()