#!/usr/bin/python3
# 文件名：client.py
# 导入 socket、sys 模块
import socket
import sys
import time
import jpype
# 创建 socket 对象
socket.setdefaulttimeout(20)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 获取服务器主机名（此处获取的是本地主机名）
host = '192.168.1.23'
# 设置待连接的服务器端口号
port = 9226

# s.setdefaulttimeout(20)
# 连接服务，指定主机和端口
s.connect((host, port))
# 接收小于 1024 字节的数据
# ss=bytes('5dd750c14aa4234c502636d40',encoding='utf-8')
# print(s.send(ss))
# print(s)
# msg = s.recv(10240)
# print (msg.decode('utf-8'))、
time.sleep(10)
s.sendall('0'.encode('utf-8'))
for i in (1,10):
    time.sleep(2)
    msg = s.recv(20480)
    print(msg)
s.close()



