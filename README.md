# Specific data format transformation for WikiHowQA dataset  
## Download & Installation  

+ Dataset: [WikiHowQA](https://github.com/dengyang17/wikihowQA/)  
+ Python package: [NLTK](http://www.nltk.org/install.html)  

**Note：Pay attention to the path problem of nltk offline download and installation.**  
## Data format
+ **Input**

`test.txt`
| question | index | label |
| :--------: | :-----: | :----: |

`summary.txt`
| index | answer_all | summary |  
| :-----: | :------: | :-------: |  

+ **Output**

`final.txt`
| question | answer_split | label | index |
| :--------: | :------: | :-----: | :-----: |

**Note:`answer_all` and `answer_split` is the corresponding whole paragraph answer and the corresponding single sentence answer of `question`.**  

## Steps	
**1 extract the QA pairs whose `label` is 1**  
```python
# Extract and write
while True:
    line = f1.readline()
    if not line:
        break
    if line.split('\t')[2] == '1\n':
        f2.write(str(line))
```
**2 extract and synthesize the corresponding data of `question answer summary index`**  
```python
# Read the text content of question, answer and summary into the list
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
# Traverse the question list and use nltk to divide the corresponding answers into sentences, synthesize and generate three texts
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
**3 answer selection**  

Done by `find_oracle_para.py` from [cnndm_acl18](https://github.com/sirfyx/cnndm_acl18/)

**4 use`ground_truth`and the file containing`question answer summary index`to generate data in the final format**
```python
# Traverse and extract  
for (line1, line2) in zip(f1, f2):
    ques = line1.split('\t')[0]
    answer = line1.split('\t')[1]
    index = line1.split('\t')[3]
    a = line2.split('\t')[0].strip('(').strip(')')
    b = a.split(',')
    tokens_answer = tk.sent_tokenize(answer)
    length = len(tokens_answer)
    for i in range(length):
        if str(i) in b or (' ' + str(i)) in b:
            f3.write(ques + '\t' + tokens_answer[i] + '\t' + '1\t' + index.strip('\r\n') + '\n')
        else:
            f3.write(ques + '\t' + tokens_answer[i] + '\t' + '0\t' + index.strip('\r\n') + '\n')
    if str(i) in b or (' ' + str(i)) in b:
        f3.write(ques + '\t' + tokens_answer[i] + '\t' + '1\t' + index.strip('\r\n') + '\n')
    else:
        f3.write(ques + '\t' + tokens_answer[i] + '\t' + '0\t' + index.strip('\r\n') + '\n')
```

## Usage 
```
python main.py test.txt summary.txt
```
**Note：  
The data file after format transformation is stored in `final.txt`.  
Delete the intermediate file manually if you want to run again after failed.**
