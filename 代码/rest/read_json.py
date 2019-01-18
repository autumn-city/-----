import json
import jieba

with open("/Users/yangchengran/Desktop/综合设计2/3个样本数据/微博_3个话题/同仁堂致歉.json",'r') as load_f:
    load_dict = json.load(load_f)

file = open('/Users/yangchengran/Desktop/综合设计2/out-3.txt','a')
for i in range(len(load_dict)):
    word = load_dict[i]['content']+'\n'
    file.write(word)

file.close()
