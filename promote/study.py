"""
筛选2个列表重复的数据
"""


import datetime
from _pydecimal import Decimal
from time import sleep

from bson import Decimal128


def run_time(func):
    """
    装饰器：计算方法执行时间
    :param func:
    :return:
    """
    def wrapper(*args,**kwargs):
        start_time = datetime.datetime.now()
        print(start_time)
        r=func(*args,**kwargs)
        end_time = datetime.datetime.now()
        print(end_time)
        print(end_time-start_time)
        return r
    return wrapper

@run_time
def find_same_element(l1, l2):
    """
    筛选2个list中重复的元素
    dict 是一个哈希表，时间复杂度为 O(1)；空间复杂度看数据大小
    :param l1:
    :param l2:
    :return:
    """

    dist = {}
    lists=[]
    for i in l1:
        dist[i] = 1
    for j in l2:
        if dist.get(j) == 1:
            lists.append(j)
    return lists

@run_time
def find_same_element1(l1, l2):
    """传统的比较2个列表是否有相同的元素"""
    sleep(1)
    for i in l1:
        for j in l2:
            if i==j:
                print(i)


def update_data():
    """
    更新mongodb数据
    :return:
    """
    from db_file import DB
    from function import read_txt
    data=read_txt("../datafile/222.txt")
    for n in data:
        sql={"_id" : n}
        document={"$set":{"money":Decimal128("100.00")}}
        multi={'multi': True}
        database = DB()
        database.update_mongodb_data('tb_user',sql,document)
        print("更新成功%s"%n)



if __name__ == '__main__':
    # l1 = [1, 2, 3, 4, 5, 6,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    # l2 = [4, 5, 6, 7, 8, 9,111,112,113,114,115,116,117,118,119,120,121,122,123,124,125,126,127,128,129,130]
    # print(find_same_element(l1, l2))
    # find_same_element1(l1,l2)

    update_data()