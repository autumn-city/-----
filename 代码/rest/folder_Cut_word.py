import  os
import jieba
import sklearn
import re
from collections import Counter


# 创建停用词列表
def stopwordslist():
    stopwords = [line.strip() for line in open('/Users/yangchengran/Desktop/综合设计2/停用词表.txt',encoding='UTF-8').readlines()]
    return stopwords

# 对句子进行中文分词
def seg_depart(sentence):
    # 对文档中的每一行进行中文分词
    print("正在分词")
    sentence = re.sub("[A-Za-z0-9\[\`\~\!\@\#\$\^\&\*\(\)\=\|\{\}\'\:\;\'\,\[\]\.\<\>\/\?\~\！\@\#\\\&\*\%]", "", sentence) #去标点符号
    sentence_depart = jieba.cut(sentence.strip())
    # 创建一个停用词列表
    stopwords = stopwordslist()
    # 输出结果为outstr
    outstr = ''

    # 去停用词
    for word in sentence_depart:
        if word not in stopwords:
            if word != '\t':
                # c[word] += 1
                outstr += word
                outstr += " "
    return outstr

# createVar = locals()
# k=0
# for info in os.listdir(r'/Users/yangchengran/Desktop/test/wechat'):
#     domain = os.path.abspath(r'/Users/yangchengran/Desktop/test/wechat') #获取文件夹的路径，此处其实没必要这么写，目的是为了熟悉os的文件夹操作
#     info = os.path.join(domain,info) #将路径与文件名结合起来就是每个文件的完整路径
#     with open(info) as createVar['res'+info]:
#         k=k+1
#         i = 0
#         c = Counter()
#         print(createVar["res"+info])
#         outputs = open('/Users/yangchengran/Desktop/test/wechatresult/wechat'+str(k)+'.txt', 'w', encoding='UTF-8')
#         for line in createVar['res'+info]:
#             line_seg = seg_depart(line)
#             outputs.write(line_seg)
#             print("-------------------正在分词和去停用词-----------" + str(i))
#             i = i + 1
#         outputs.close()
#         print("删除停用词和分词成功！！！")



# 将输出结果写入out.txt中







