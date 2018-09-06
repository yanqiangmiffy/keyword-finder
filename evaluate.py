import pandas as pd
import jieba
from jieba import posseg
from jieba.analyse import extract_tags
from utlis import generate_name,judge_not_one,judge_not_two
jieba.load_userdict('data/custom_dict.txt')
jieba.analyse.set_stop_words('data/stop_words.txt')
allow_pos={'nr':1,'nz':2,'ns':3,'nt':4,'eng':5,'n':6,'l':7,'i':8,'a':9,'nrt':10,'v':11,'t':12}

train_data=pd.read_csv('data/train_docs.csv')
true_keywords=train_data['keyword'].apply(lambda x:x.split(',')).tolist()
titles=train_data['title'].tolist()
train_docs=train_data['doc'].tolist()

labels_1=[]
labels_2=[]

not_one=0
not_two=0

use_tfidf=0
for title,doc,true_key in zip(titles,train_docs,true_keywords):
    # 筛选标签重要的词
    title_word_tags=[(word,tag) for word,tag in posseg.cut(title) if tag in allow_pos]
    # 解决分词的标点符号问题
    if '·' in title:
        word_tags = generate_name(title_word_tags)
    # 筛选长度>1的词
    title_word_tags = [keyword for keyword in title_word_tags if len(keyword[0]) > 1]
    # 去除重复
    title_word_tags=list(set(title_word_tags))
    title_word_tags = sorted(title_word_tags, reverse=False, key=lambda x: (allow_pos[x[1]], -len(x[0])))

    title_allow_pos=['nr','nz','ns']
    flag=len(title_word_tags)>=2 and title_word_tags[0][1] in title_allow_pos and title_word_tags[1][1] in title_allow_pos
    if flag or '·' in title:
            labels_1.append(title_word_tags[0][0])
            labels_2.append(title_word_tags[1][0])
            # print(title_word_tags)
            # print(true_key)
            # print(title)
            # print('--'*69)
    else:
        use_tfidf +=1
        # 使用tf-idf 提取关键词
        # tf_pos = ['nr', 'nz', 'ns', 'nt', 'vn', 'eng', 'nrt', 'v','n','a']
        doc_word_tags = [(word, tag) for word, tag in posseg.cut(title+doc) if tag in allow_pos ]
        doc_word_tags = [word_tag for word_tag in doc_word_tags if len(word_tag[0])>1 ]

        title_text="".join([word for word,_ in title_word_tags])
        doc_text="".join([word for word,_ in doc_word_tags])
        text=title_text*10+doc_text

        word_weight=[(word,weight) for word ,weight in extract_tags(text,withWeight=True)]
        key_1,key_2=word_weight[0][0],word_weight[1][0]

        labels_1.append(key_1)
        labels_2.append(key_2)
        if judge_not_one(key_1,key_2,true_key):
            not_one+=1
        #     print("true_key:{}".format(true_key))
        #     print("title_word_tags:{} \t title:{}".format(title_word_tags, title))
        #     print("doc_word_tags{}".format(doc_word_tags))
        #     print("word_weight:{}".format(word_weight))
        #     print(text)
        #     print('--' * 69)
        if judge_not_two(key_1,key_2,true_key):
            not_two+=1
            print("true_key:{}".format(true_key))
            print("title_word_tags:{} \t title:{}".format(title_word_tags, title))
            print("doc_word_tags{}".format(doc_word_tags))
            print("word_weight:{}".format(word_weight))
            print('--' * 69)


print("使用tf-idf提取的次数：",use_tfidf)
print("只命中一个关键词的情况次数：{}".format(not_one))
print("两个关键词都未命中的情况次数：{}".format(not_two))

score=0
for label_1,label_2,true_key in zip(labels_1,labels_2,true_keywords):
    if label_1 in true_key:
        score+=0.5
    if label_2 in true_key:
        score+=0.5
print("最终得分：{}".format(score))