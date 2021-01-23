# Format_converter
**用于特定数据格式的转换**
## 需要安装以下python包
+ `NLTK`用于分句
```
pip install NLTK
```
要注意离线下载路径问题

## 数据格式
+ **输入**:

**test.txt**:
| question | index | label |
| :--------: | :-----: | :----: |

**summary.txt**:
| index | answer_all | summary |  
| :-----: | :------: | :-------: |
+ **输出**:

**test_f.txt**:
| question | answer_split | label | index |
| :--------: | :------: | :-----: | :-----: |

其中`answer_all`和`answer_split`分别是是`question`的对应整段答案和对应单句答案  

## 具体步骤	
**1 提取出`label`为1的问答对**  
```python
#提取并写入文本
while True:
    line = f1.readline()
    if not line:
        break
    if line.split('\t')[2] == '1\n':
        f2.write(str(line))
```
**2 提取、合成`question-answer-summary-index`对应数据**
```python
# 将question和answer，summary文本内容读入列表中
for line in f1:
    list1 = []
    for i in line.split('\t'):
        list1.append(i)
    list2.append(list1)
for line in f2:
    list3 = []
    for i in line.split('\t'):
        list3.append(i)
    list4.append(list3)
# 遍历question列表并用NLTK对对应答案进行分句，合成，生成三个文本
for i in list2: 
    idx = int(i[1])
    ques = i[0]
    index = i[1]
    print(idx,"\n")
    answer = list4[idx][1]
    summary = list4[idx][2]

    tokens_answer = tk.sent_tokenize(answer)
    tokens_summary = tk.sent_tokenize(summary)

    tokens_a_rp = "##SENT##".join(i for i in tokens_answer)
    tokens_s_rp = "##SENT##".join(i for i in tokens_summary)

    f3.write(tokens_a_rp +'\n')
    f4.write(tokens_s_rp + '\n')
    f5.write(ques + '\t' + answer + '\t' + summary.strip('\r\n') + '\t' + index + '\n')
```
**3 生成`ground_truth`文件**  

`ground_truth`的生成由以下脚本完成：https://github.com/sirfyx/cnndm_acl18/find_oracle_para.py  

**4 用`ground_truth`和包含`question-answer-summary-index`的文件生成最终格式的数据**
```python
#遍历并提取
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
```
若运行中止后想再次运行，注意手动删除中间文件
