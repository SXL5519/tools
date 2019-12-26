"""
判断json是否相等
"""
import json


def eq_json(json1,json2):
    dcit1=json.load(json1)###转换为字典
    dcit2=json.load(json2)
    for key1,key2 in dcit1,dcit2:
        if key1 in dcit2 and key2 in dcit1:
            if dict[key1]==dict[key2]:
                pass
            else:
                print('不相等')
                break
        else:
            print('不相等')
            break


if __name__=='__main__':

    json1=json.dumps([{'1':1,'2':2}])
    json2=json.dumps([{'1':1,'2':3}])
    eq_json(json1,json2)