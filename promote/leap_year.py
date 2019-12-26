"""
判断是否是闰年
1、是4的倍数且不是100的倍数，是闰年
2、是400的倍数，是闰年

"""

def is_year(year):
    if year % 4==0 and year % 100 != 0 or year % 400 ==0:
        print('是闰年')
    else:
        print('不是闰年')

import calendar

def isleap_year(year):
    check_year=calendar.isleap(year)
    if check_year == True:
        print ("闰年")
    else:
        print ("平年")







if __name__=='__main__':
    year=int(input('输入年份:'))
    is_year(year)
    isleap_year(year)