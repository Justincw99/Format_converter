# -*- encoding: utf-8 -*-
'''
功能：生成最终格式\n
作者：姜才武\n
时间：2021/01/22\n
用法：python main.py filename1 filename2
'''
import os
import sys
import find_oracle_para as fop
import get1
import seperate
import final

if __name__ == "__main__":
    filename1 = sys.argv[1]  #filename1为question文件
    filename2 = sys.argv[2]  #filename2为summary文件
    if os.path.exists(filename1) and os.path.exists(filename2):
        question = get1.get1(filename1)  #提取出label为1的问答对
        answer, summary, combination = seperate.seperate(question, filename2)  #生成answer、summary文件和总文件
        ground_truth = fop.main(answer, summary, 'oracle.txt')  #生成oracle文件
        check = final.final(combination, ground_truth)  #生成最终形式，check用来检验是否转换成功
        if check:
            print('数据格式转换完成,并存储于final.txt文件中')
        else:
            print('数据格式转换失败，若想重新转换请删除中间文件')
    else:
        print('main输入文件名错误')

    # os.remove('combination.txt')  #删除中间文件
    # os.remove('answer_1.txt')
    # os.remove('oracle.txt')
    # os.remove('summary_1.txt')
    # os.remove('test_1.txt')
