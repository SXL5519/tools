import pprint
from datetime import date, datetime

import pymongo
import pymysql
import readConfig as readConfig
from pymongo import MongoClient


localReadConfig = readConfig.ReadConfig()

class DB:


    def __init__(self):
        # self.log = Log.get_log()
        # self.logger = self.log.get_logger()
        global host, username, password, port, database, mysql_config
        host = localReadConfig.get_db("host")
        username = localReadConfig.get_db("username")
        password = localReadConfig.get_db("password")
        port = int(localReadConfig.get_db("port"))
        database = localReadConfig.get_db("database")
        mysql_config = {
            'host': str(host),
            'user': username,
            'passwd': password,
            'port': int(port),
            'db': database
        }

        # self.db = None
        # self.cursor = None

    def connect_mongodb_all(self,table,type,n=None):
        """
        查询mongoDB数据
        :param table: 表名
        :param n: 查询条件
        :return:
        """
        value=''
        client = MongoClient(host=host, port=port)  ##无密码
        # client = MongoClient(host=host,port=port,username=username,password=password)
        db = client[database]
        # print(db)
        collection = db[table]
        # print('sql：'+str(n))
        if type == 1:
            value = collection.find_one(n)
        elif type == 2:
            value = collection.aggregate(n)
        elif type == 3:
            value = collection.find(n).count()
        # print(value)
        client.close()
        return value

    def update_mongodb_data(self,table,sql,document):
        """
        更新mongodb数据
        :return:
        """
        client = MongoClient(host=host, port=port)  ##无密码
        # client = MongoClient(host=host,port=port,username=username,password=password)
        db = client[database]
        # print(db)
        collection = db[table]
        print(sql)
        print(document)
        collection.update(sql,document)


    def connect_mysql_all(self,sql,params):
        """
        查询sql全部数据
        :param sql:
        :param params:
        :return:
        """
        db = pymysql.connect(**mysql_config)
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        db.commit()
        value = cursor.fetchall()
        self.cursor.close()
        self.db.close()
        print("Database closed!")
        return value

    def connect_mysql_one(self,sql,params):
        """
        查询sql一条数据
        :param sql:
        :param params:
        :return:
        """
        db = pymysql.connect(**mysql_config)
        cursor = self.db.cursor()
        cursor.execute(sql, params)
        db.commit()
        value = cursor.fetchone()
        self.cursor.close()
        self.db.close()
        print("Database closed!")
        return value


    def connectDB(self):
        """
        链接数据库
        :return:
        """
        try:
            # connect to DB
            self.db = pymysql.connect(**mysql_config)
            # create cursor  创建游标
            self.cursor = self.db.cursor()
            print("Connect DB successfully!")
        except ConnectionError as ex:
            raise
            # self.logger.error(str(ex))

    def executeSQL(self, sql, params):
        """
        执行sql语句
        :param sql:
        :param params: sql语句的参数
        :return:
        """
        self.connectDB()
        # executing sql
        self.cursor.execute(sql, params)
        # executing by committing to DB
        self.db.commit()
        return self.cursor

    def get_all(self, cursor):
        """
        获取查询的全部数据
        :param cursor:
        :return:
        """
        value = cursor.fetchall()
        return value

    def get_one(self, cursor):
        """
        获取查询出的一条数据
        :param cursor:
        :return:
        """
        value = cursor.fetchone()
        return value

    def closeDB(self):
        """
        关闭数据库
        :return:
        """
        self.cursor.close()
        self.db.close()
        print("Database closed!")

    def get_data(self,data,key):
        """
        执行SQL后获取数据
        :param data: 执行SQL后的数据
        :param key: 需要取值的KEY值
        :return: 返回字符串类型数据
        """
        value=[]
        for i in data:
            if type(key)== list:
                for j in key:
                    va = str(i.get(j))
                    value.append(va)
            else:
                value.append(str(i.get(key)))
        return value

    def assert_data(self,data,n):
        """
        判断 get_data 返回数据是否为空（null）
        :param list: 默认值
        :param assert_value: 判断的数据
        :param data: sql返回数据
        :return: data，或者 list(列表)
        """
        if len(data)!=0:
            value=[n for n in data]
        else:
            value=[0 for i in range(n)]
        # value=[n for n in data if len(data)!=0 else list1]
        return value


# if __name__ == "__main__":
#     a=DB()
#     ba=a.connect_mongodb_all('tb_order',[{'$match': {'$and': [{'payTime': {'$gte': datetime.strptime('2019-01-16 00:00:00','%Y-%m-%d %H:%M:%S')}},
#                             {'payTime': {'$lte': datetime.strptime('2019-01-16 23:59:59','%Y-%m-%d %H:%M:%S')}}]}},
#                             {'$group': {'_id': '销售总额', 'total': {'$sum': '$totalPrice'}}}])
#     c=0
#     for i in ba:
#         c=float(str(i.get('total')))##销售总额
#     bb=a.connect_mongodb_all('tb_return_apply',[{'$match':{'$and':[{"statusList.status":"FINISHED"},
#                             {"statusList.time":{'$gte':datetime.strptime('2019-01-16 00:00:00','%Y-%m-%d %H:%M:%S')}},
#                             {"statusList.time":{'$lte':datetime.strptime('2019-01-16 23:59:59','%Y-%m-%d %H:%M:%S')}}]}},
#                             {'$group':{'_id':'退款总金额','total':{'$sum':'$confirmMoney'}}}])
#     cc=0
#     for j in bb:
#         cc = float(str(j.get('total')))  ##退款总金额
#     print('销售金额%.2f'%(c-cc))
##################################################################################################################################
    # bc = a.connect_mongodb_all('tb_return_apply', [{'$match': {'$and': [{"statusList.status": "FINISHED"},
    #                                                                     {"statusList.time": {'$gte': datetime.strptime(
    #                                                                         '2019-01-16 00:00:00',
    #                                                                         '%Y-%m-%d %H:%M:%S')}},
    #                                                                     {"statusList.time": {'$lte': datetime.strptime(
    #                                                                         '2019-01-16 23:59:59',
    #                                                                         '%Y-%m-%d %H:%M:%S')}}]}},
    #                                                {'$group': {'_id': '退款总金额', 'total': {'$sum': '$confirmMoney'}}}])
