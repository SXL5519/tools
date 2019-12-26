"""
判断输入的字符串是否是IP

re.match与re.search的区别：re.match只匹配字符串的开始，如果字符串开始不符合正则表达式，则匹配失败，函数返回None；而re.search匹配整个字符串，直到找到一个匹配
"""
import re


def q_ip(n):
    #正则
    compile_ip = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if compile_ip.match(n):
        print('is ip')
    else:
        print('not ip')

def is_ip(n):
    if '.' in n and n.count('.')==3: # 判断是否包含小数点，且小数点个数为3
        flag = True
        one_list = n.split('.')#以小数点分割字符串
        for one in one_list:
            try:
                one_num = int(one)
                if one_num >= 0 and one_num <= 255:
                    pass
                else:
                    flag = False
                    break
            except:
                flag = False
        if flag==True:
            print('is ip')
        else:
            print('is not ip')
    else:
        print('is not ip')















if __name__ == '__main__':
    n='132.18.1.21'
    # q_ip(n)
    is_ip(n)