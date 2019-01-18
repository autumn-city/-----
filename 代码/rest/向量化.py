from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix
import numpy as np



with open('/Users/yangchengran/Desktop/综合设计2/out.txt') as f3:
    res1 = f3.read()

outfilename = "/Users/yangchengran/Desktop/综合设计2/TF_IDF.txt"
outfilename_1 = "/Users/yangchengran/Desktop/综合设计2/词向量.txt"

outputs = open(outfilename, 'w', encoding='UTF-8')
output_2=open(outfilename_1, 'w', encoding='UTF-8')

corpus = [res1]
vector = TfidfVectorizer()
tfidf = vector.fit_transform(corpus)

#输出TF-IDF
wordlist = vector.get_feature_names()#获取词袋模型中的所有词
# tf-idf矩阵 元素a[i][j]表示j词在i类文本中的tf-idf权重
weightlist = tfidf.toarray()
#打印每类文本的tf-idf词语权重,第一个for遍历所有文本,第二个for便利某一类文本下的词语权重
for i in range(len(weightlist)):
    print("-------第",i,"段文本的词语tf-idf权重------")
    for j in range(len(wordlist)):
        # print(wordlist[j],weightlist[i][j])
        outputs.write(str(wordlist[j])+": ")
        outputs.write(str(weightlist[i][j])+"     ")
        if j%3==0:
            outputs.writelines("\n")

#输出词向量
for k in range(len(tfidf.indices)):
    output_2.write(str(wordlist[k]) + ": ")
    output_2.writelines(str(tfidf.indices[k])+"   ")
    output_2.writelines(str(tfidf.data[k]) + '\n')

