# -*- encoding: utf-8 -*-
'''
功能：提取出label为1的问答对\n
作者：姜才武\n
时间：2021/01/19\n
用法：python get1.py filename\n
'''
import os
import sys
 
def get1(filename): #filename 表示一个要提取label为1问答对的txt文本
    if os.path.exists(filename):
        print('提取出label为1的问答对...')
        f1 = open(filename, 'r', encoding='utf-8')   #打开txt文本进行读取
        f2 = open('test_1.txt', 'a+',encoding="utf-8")
        while True:  #循环，读取question文本里面的所有内容
            line = f1.readline() #一行一行读取
            if not line:  #如果没有内容，则退出循环
                break
            if line.split('\t')[2] == '1\n':
                f2.write(str(line))
        f1.close()
        f2.close()
        return ('test_1.txt')
    else:
        print('get1输入文件名错误')
 
if __name__ == "__main__":
    filename = sys.argv[1]
    get1(filename)
    print('get1转换完成')