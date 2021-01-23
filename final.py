# -*- encoding: utf-8 -*-
'''
功能：转换为最终格式\n
作者：姜才武\n
时间：2021/01/20\n
用法：python final.py filename1 filename2 
'''
import os
import sys
import codecs
import nltk.tokenize as tk

def final(filename1, filename2): #filename1 表示all的txt文本 filename2表示oracle的txt文本
    if os.path.exists(filename1) and os.path.exists(filename2):
        print('转换为最终格式...')
        f1 = codecs.open(filename1, 'r', encoding='utf-8')   #打开txt文本进行读取
        f2 = codecs.open(filename2, 'r', encoding='utf-8')
        f3 = open('final.txt', 'a+',encoding="utf-8")
        f3.write("question\tanswer\tlabel\tindex\n")
        list2 = []
        f1.readline()
        for (line1, line2) in zip(f1, f2):
            ques = line1.split('\t')[0]
            answer = line1.split('\t')[1]
            index = line1.split('\t')[3]
            a = line2.split('\t')[0].strip('(').strip(')')  #去除首尾括号
            b = a.split(',')  #将str以'，'为间隔转换为list
            tokens_answer = tk.sent_tokenize(answer)
            length = len(tokens_answer)
            for i in range(length):  #判断序号是否为选中的内容来记录label值
                if str(i) in b or (' ' + str(i)) in b:
                    f3.write(ques + '\t' + tokens_answer[i] + '\t' + '1\t' + index.strip('\r\n') + '\n')
                else:
                    f3.write(ques + '\t' + tokens_answer[i] + '\t' + '0\t' + index.strip('\r\n') + '\n')
            if str(i) in b or (' ' + str(i)) in b:
                f3.write(ques + '\t' + tokens_answer[i] + '\t' + '1\t' + index.strip('\r\n') + '\n')
            else:
                f3.write(ques + '\t' + tokens_answer[i] + '\t' + '0\t' + index.strip('\r\n') + '\n')
        f3.close()
        return 1
    else:
        print('final输入文件名错误')
        return 0


if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    final(filename1, filename2)
    print('合成完成')