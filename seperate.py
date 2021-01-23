# -*- encoding: utf-8 -*-
'''
功能：提取、合成问题-答案-摘要对应数据，用nltk分句，用'##SENT##'作为每句间的分隔符合成answer\n
作者：姜才武\n
时间：2021/01/20\n
用法：python seperate.py filename1 filename2 
'''
import os
import sys
import codecs
import nltk
import nltk.tokenize as tk

nltk.data.path.append("/home/amax/JCW/nltk_data") #解决nltk手动下载包的路径访问问题

def seperate(filename1, filename2): #filename1 表示question的txt文本 filename2表示answer和summary的txt文本
    if os.path.exists(filename1) and os.path.exists(filename2):
        print('NLTK分句...')
        f1 = codecs.open(filename1, 'r', encoding='utf-8') #打开txt文本进行读取
        f2 = codecs.open(filename2, 'r', encoding='utf-8')
        f3 = open('answer_1.txt', 'a+',encoding="utf-8")
        f4 = open('summary_1.txt', 'a+',encoding="utf-8")
        f5 = open('combination.txt', 'a+',encoding="utf-8")
        f5.write("question\tanswer\tsummary\tindex\n")
        f2.seek(0)  #光标归0，很关键否则再次readline()什么都读不出来
        list2 = []
        list4 = []
        for line in f1:
            list1 = []
            for i in line.split('\t'):
                list1.append(i)
            list2.append(list1)
        print('list2生成')
        for line in f2:
            list3 = []
            for i in line.split('\t'):
                list3.append(i)
            list4.append(list3)
        print('list4生成')
        for i in list2: #将answer、summary和综合起来的内容写入三个文件中
            idx = int(i[1])
            ques = i[0]
            index = i[1]
            print(idx,"\n")
            answer = list4[idx][1]
            summary = list4[idx][2]

            tokens_answer = tk.sent_tokenize(answer)  #NLTK分句
            tokens_summary = tk.sent_tokenize(summary)

            tokens_a_rp = "##SENT##".join(i for i in tokens_answer)  #以##SENT##为间隔符将分开的句子连接起来用于后续处理
            tokens_s_rp = "##SENT##".join(i for i in tokens_summary)

            f3.write(tokens_a_rp +'\n')  #将对应answer写入
            f4.write(tokens_s_rp + '\n')  #将对应summary写入
            f5.write(ques + '\t' + answer + '\t' + summary.strip('\r\n') + '\t' + index + '\n') #全部写入combination里面
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        f5.close()
        return (['answer_1.txt', 'summary_1.txt', 'combination.txt'])
    else:
        print('seperate输入文件名错误')


if __name__ == "__main__":
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    seperate(filename1, filename2)
    print('分句完成')
