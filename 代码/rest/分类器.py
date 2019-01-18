from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.cluster import KMeans
from sklearn import datasets
import os
import numpy as np
import  sys
from collections import Counter
from sklearn.linear_model import SGDClassifier
from folder_Cut_word import seg_depart

createVar = locals()


#脚本判断正确率->用一个标签内的文件进行判断，输出数组
def judge_right():
    i=0
    j=0
    for info in os.listdir(r'/Users/yangchengran/Desktop/单独文章-数据集的副本/春运火车票开抢/weibo/'):
        domain = os.path.abspath(r'/Users/yangchengran/Desktop/单独文章-数据集的副本/春运火车票开抢/weibo/') #获取文件夹的路径，此处其实没必要这么写，目的是为了熟悉os的文件夹操作
        info = os.path.join(domain,info) #将路径与文件名结合起来就是每个文件的完整路径
        # print(info)
        #分词

        with open(info) as createVar['intern '+str(j)]:
            print(createVar['intern '+str(j)])
            outputs = open('/Users/yangchengran/Desktop/单独文章-数据集的副本/春运火车票开抢/weiboresult/' + str(j) + '.txt', 'w',
                           encoding='UTF-8')
            for line in createVar['intern '+str(j)]:
                line_seg = seg_depart(line)
                outputs.write(line_seg)
                print("-------------------正在分词和去停用词-----------" + str(j))
            outputs.close()
            seg=open('/Users/yangchengran/Desktop/单独文章-数据集的副本/春运火车票开抢/weiboresult/' + str(j) + '.txt',
                           encoding='UTF-8').read()
            print(seg+"-----seg")
            if input_judge(seg)=='wechatresult':
                i=i+1
            print(input_judge(seg)+"--------judge")
            print(seg)
        j=j+1

    print("命中微博的测试文件占了： %f"%((1-i/j)*100)+"%")



#构建管道
# def pipe():
#     from sklearn.pipeline import Pipeline
#     text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), (
#     'clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)), ])
#     text_clf.fit(twenty_train.data, twenty_train.target)
#     text_clf.fit(twenty_train.data, twenty_train.target)

#在这里进行分类器准确度预测的时候，建立了一个管道（TEXT_CLF）隐藏细节，否则的话需要对检验样本进行特征化处理
def prediction():
    from sklearn.pipeline import Pipeline
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', MultinomialNB()), ])
    text_clf.fit(twenty_train.data, twenty_train.target)
    twenty_test=datasets.load_files("/Users/yangchengran/Desktop/test", encoding="utf-8", random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    print(np.mean(predicted == twenty_test.target))

#高粒度的模型性能评估
# from sklearn import metrics
# print(metrics.classification_report(twenty_test.target,predicted,target_names=twenty_test.target_names))
def deep_prediction():
    from sklearn.pipeline import Pipeline
    text_clf = Pipeline([('vect', CountVectorizer()), ('tfidf', TfidfTransformer()), ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None)), ])
    text_clf.fit(twenty_train.data, twenty_train.target)
    twenty_test=datasets.load_files("/Users/yangchengran/Desktop/test", encoding="utf-8", random_state=42)
    docs_test = twenty_test.data
    predicted = text_clf.predict(docs_test)
    from sklearn import metrics
    print(metrics.classification_report(twenty_test.target, predicted,target_names = twenty_test.target_names))
    print(metrics.confusion_matrix(twenty_test.target, predicted))

#键盘输入新文档并判断
def input_doc():
    doc_source = input("input the test text: ")
    input_judge(doc_source)

#对新文档进行判断
def input_judge(doc_source):
    docs_new = [doc_source]
    X_new_counts = count_vect.transform(docs_new)
    X_new_tfidf = tfidf_transformer.transform(X_new_counts)
    predicted = text_clf.predict(X_new_tfidf)
    for doc, category in zip(docs_new, predicted):
        print('该文档更倾向于归属 %s' % (twenty_train.target_names[category]))
    return twenty_train.target_names[category]


#输入训练数据，在这里，DATA就是TRAIN_，TARGET就是TRAIN_Y,就是标签，
twenty_train=datasets.load_files("/Users/yangchengran/Desktop/train/", description=None, categories=None, load_content=True, shuffle=True, encoding="utf-8", random_state=0)
print(twenty_train.target_names)
print(len(twenty_train.data))
# print("\n".join(twenty_train.data[0].split("\n")[:3]))
os.listdir(r'/Users/yangchengran/Desktop/train/')

# 朴素贝叶斯分类器实例化
# count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(twenty_train.data)
# tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
# tfidf_transformer = TfidfTransformer()
# X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# text_clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)


# 支持向量机分类模型与分类器测试
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
text_clf = SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None).fit(X_train_tfidf, twenty_train.target)

# 输入新文档进行检验属于哪一个标签
# input_doc()


# 分类器测试
# prediction()

#高粒度的模型性能评估
# deep_prediction()

#对测试文件命中数的百分比判断
judge_right()



#历史版本数据
# twenty_test=datasets.load_files("/Users/yangchengran/Desktop/train/", shuffle=True, random_state=42)
# # print(twenty_test.target_names)
# docs_test = twenty_test.data
# #对测试集进行特征值变换
# predicted = text_clf.predict(docs_test)
# np.mean(predicted == twenty_test.target)

# doc_source= input("input the test text: ")
# docs_new = [doc_source]
# X_new_counts = count_vect.transform(docs_new)
# X_new_tfidf = tfidf_transformer.transform(X_new_counts)
# predicted = text_clf.predict(X_new_tfidf)
# for doc, category in zip(docs_new, predicted):
#     print('该文档更倾向于归属 %s' % (twenty_train.target_names[category]))

# 构建管道
# from sklearn.pipeline import Pipeline
# text_clf = Pipeline([('vect', CountVectorizer()),('tfidf', TfidfTransformer()),('clf', SGDClassifier(loss='hinge', penalty='l2',alpha=1e-3, random_state=42,max_iter=5, tol=None)),])
# text_clf.fit(twenty_train.data, twenty_train.target)
# text_clf.fit(twenty_train.data, twenty_train.target)