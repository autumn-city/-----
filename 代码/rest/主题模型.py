from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


with open('/Users/yangchengran/Desktop/综合设计2/use-1.txt') as f3:
    res1 = f3.read()
with open('/Users/yangchengran/Desktop/综合设计2/use-2.txt') as f4:
    res2 = f4.read()
with open('/Users/yangchengran/Desktop/综合设计2/use-3.txt') as f5:
    res3 = f5.read()


corpus = [res1,res2,res3]
cntVector = CountVectorizer()
cntTf = cntVector.fit_transform(corpus)
# print(cntTf)
lda = LatentDirichletAllocation(n_components=2,
                                learning_offset=50.,
                                random_state=0)
docres = lda.fit_transform(cntTf)
print(docres)
print(lda.components_)
