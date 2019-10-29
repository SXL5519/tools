"""
NumPy 学习
"""
from numpy import *


print(eye(4))


import numpy as np
# dt = np.dtype([('age',np.int8)])
# a = np.array([(10,),(20,),(30,)], dtype = dt)
# print(a['age'])
# """
# 声明一个3列的数据类型，第一列列名为name,数据类型为字符串；第二列列名为age，数据类型为int8(整数);第三列列名为marks.数据类型为浮点型
# """
# student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')])
# b = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype = student)
# print(b)###打印整个数组
# print(b['name'])##打印数组的name列
# print(b['age'])
# print(type(b['age']))
# print(type(b))


# c = np.arange(24)###产生0到23的一维数组，range的数组版
# print(c)
# print (c.ndim)
# print (c.shape)
# # c 现只有一个维度
# # 现在调整其大小
# cc = c.reshape(2,4,3)###将C修改为2个4行3列
# print(cc)# b 现在拥有三个维度
# print (cc.ndim)###打印数组的维数
# print (cc.shape)##打印数组的大小
#
# #创建一个数组，2行3列
# d = np.array([[1,2,3],[4,5,6]])
# print(d)
# ##修改数组d的大小，3行2列；方法两种：reshape，shape
# d.shape =  (3,2)
# print (d)



"""
数组创建
"""
##  1、
"""
numpy.empty 方法用来创建一个指定形状（shape）、数据类型（dtype）且未初始化的数组
数组元素为随机值，因为它们未初始化
"""
e = np.empty([3,2], dtype = int)
print (e)

###  2、
"""
数组元素默认值是0.（默认浮点型） 注意:zeros_linke函数只是根据传入的ndarray数组的shape来创建所有元素为0的数组，并不是拷贝源数组中的数据
"""
f = np.zeros((5), dtype = np.int)
print(f)
ndarray4 = np.zeros(10)
ndarray5 = np.zeros((3, 3))
ndarray6 = np.zeros_like(f)  # 按照 ndarray5 的形状创建数组
print(ndarray4)
print(ndarray5)
print(ndarray6)

###   3、

"""
用于创建所有元素都为1的数组.ones_like用法同zeros_like用法
"""
print('3333333333333333')
# 默认为浮点数
g = np.ones(5)
print(g)

# 自定义类型
x = np.ones([2, 2], dtype=int)
print(x)
print(g[0])
g[0] = 999###修改数组的值
print(g)
h = np.ones_like(g)  # 按照 ndarray5 的shape创建数组
print(h)

###  4、
"""
arange函数是python内置函数range函数的数组版本
"""
print('44444444444444444')
ndarray13 = np.arange(10)                  #产生0-9共10个元素
ndarray14 = np.arange(10, 20)              #产生从10-19共10个元素
ndarray15 = np.arange(10, 20, 2)           #产生10 12 14 16 18, 2为step 间隔为2
print(ndarray13)
print(ndarray14)
print(ndarray15)
print('ndarray14的形状:', ndarray14.shape)  #ndarray14的长度
z=ndarray14.reshape((2, 5))
ndarray14.shape=(2,5)
print(z)
print(ndarray14)
print(ndarray14.shape)


###   5、
"""
eys创建对角矩阵数组
该函数用于创建一个N*N的矩阵，对角线为1，其余为0
"""
print('5555555555555')
ndarray16 = np.eye(5)
print(ndarray16)


#### 6、
"""
创建数组最简单的方法就是使用array函数。它接收一切序列型的对象（包括其他数组），然后产生一个新的含有传入数据的Numpy数组。
"""
"""
# 声明一个3列的数据类型，第一列列名为name,数据类型为字符串；第二列列名为age，数据类型为int8(整数);第三列列名为marks.数据类型为浮点型
"""
student = np.dtype([('name','S20'), ('age', 'i1'), ('marks', 'f4')])
w = np.array([('abc', 21, 50),('xyz', 18, 75)], dtype = student)
print(w)###打印整个数组
print(w['name'])##打印数组的name列
print(w['age'])
print(w.ndim)
w.reshape(2,1)
print(w)


#### 7、
"""
在10到20之间生成步长为2的浮点数
"""
r = np.arange(10,20,2,dtype=float)
print (r)

#
# if __name__ == '__main__':
#     test_1()