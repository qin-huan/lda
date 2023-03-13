import jieba
import stylecloud
import re
from collections import Counter
import json

inputfile = 'all_yq_content.csv'
stopwordsFile = 'stopwords.txt'
ciyunFile = 'ciyun.jpg'
outputFile = 'count_collection.json'
weiboStopWords = ['转发','微博','全文','为了','此间','味儿','近日','全省','我市','新闻','视频','小时','展开','工作','原图','期间','江苏','常州','淮安','连云港','南京','南通','宿迁','苏州','徐州','无锡','盐城','扬州','泰州','镇江','组图','张','例', '市', '省','原始','用户']

#按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    #去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines

def regex_change(line):
    #前缀的正则
    username_regex = re.compile(r"^\d+::")
    #URL，为了防止对中文的过滤，所以使用[a-zA-Z0-9]而不是\w
    url_regex = re.compile(r"""
        (https?://)?
        ([a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)
        (\.[a-zA-Z0-9]+)*
        (/[a-zA-Z0-9]+)*
    """, re.VERBOSE|re.IGNORECASE)
    #剔除日期
    data_regex = re.compile(u"""        #utf-8编码
        年 |
        月 |
        日 |
        (周一) |
        (周二) | 
        (周三) | 
        (周四) | 
        (周五) | 
        (周六)
    """, re.VERBOSE)
    #剔除所有数字
    decimal_regex = re.compile(r"[^a-zA-Z]\d+")
    #剔除空格
    space_regex = re.compile(r"\s+")

    line = username_regex.sub(r"", line)
    line = url_regex.sub(r"", line)
    line = data_regex.sub(r"", line)
    line = decimal_regex.sub(r"", line)
    line = space_regex.sub(r"", line)

    return line

def delete_stopwords(lines):
    stopwords = read_file(stopwordsFile)
    stopwords += weiboStopWords
    all_words = []

    for line in lines:
        all_words += [word for word in jieba.cut(line) if word not in stopwords]

    # 生成词云图
    # result = " ".join(all_words) #分词用空格隔开

    # 统计词频
    dict_words = dict(Counter(all_words)) 

    return dict_words

def ciyun(words, ciyunFile):
    stylecloud.gen_stylecloud(
        text=words, # 上面分词的结果作为文本传给text参数
        size=1024,
        font_path='MSYH.ttc', # 字体设置
        palette='cartocolors.qualitative.Pastel_7', # 调色方案选取，从palettable里选择
        gradient='horizontal', # 渐变色方向选了垂直方向
        icon_name='fab fa-python',
        # icon_name='fab fa-weixin',  # 蒙版选取，从Font Awesome里选
        output_name=ciyunFile) # 输出词云图

def main():
    # 按行读取文件
    lines = read_file(inputfile)
    
    # 使用正则过滤
    for i in range(len(lines)):
        lines[i] = regex_change(lines[i])
    
    # 去除停用词，并返回词袋字典
    bow_words = delete_stopwords(lines)

    # 统计词频
    # ciyun(bow_words, ciyunFile)
    
    # 对词袋字典进行排序
    sorted_bow = sorted(bow_words.items(), key=lambda d:d[1], reverse=True)

    # 将排序结果保存到json文件中
    with open(outputFile, "w") as output_file:
        json.dump(sorted_bow, output_file, ensure_ascii=False)
        print("加载数据完成...")

    # 打印出出现次数最高的100个数据，方便观察
    for words in sorted_bow[:100]:
        print(words)

if __name__ == '__main__':
    main()