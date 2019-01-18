import jieba
from collections import Counter


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('/Users/yangchengran/Desktop/综合设计2/停用词表.txt',encoding='UTF-8').readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence,c):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''

    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                c[word] += 1
                outstr += word
                outstr += " "
    return outstr


# 给出文档路径
filename = "/Users/yangchengran/Desktop/综合设计2/out-3.txt"
outfilename = "/Users/yangchengran/Desktop/综合设计2/use-3.txt"
inputs = open(filename, 'r', encoding='UTF-8')
outputs = open(outfilename, 'w', encoding='UTF-8')

# 将输出结果写入out.txt中
i=0
c=Counter()
for line in inputs:
    line_seg = seg_depart(line)
    outputs.write(line_seg + '\n')
    print("-------------------正在分词和去停用词-----------"+str(i))
    i=i+1
outputs.close()
inputs.close()
print("删除停用词和分词成功！！！")

print('常用词频度统计结果')
f = open("/Users/yangchengran/Desktop/综合设计2/统计结果.txt", 'w+')
for (k, v) in c.most_common(300):
    print('%s%s %d' % ('  ' * (5 - len(k)), k, v), file=f)

