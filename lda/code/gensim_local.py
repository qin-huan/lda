import os
import re
import jieba
from gensim import corpora
from gensim import models
from gensim.models import CoherenceModel
import pyLDAvis
import pyLDAvis.gensim
import plotly.offline as py
import plotly.graph_objs as go
import xlwt 

stopwords_file = '../data/in/stop_words.txt'
weibo_stopwords = ['转发','微博','全文','为了','此间','味儿','近日','全省','我市','新闻','视频','小时','展开','工作','原图','期间','组图','张','例', '市', '省','原始','用户','江苏','常州','淮安','连云港','南京','南通','宿迁','苏州','徐州','无锡','盐城','扬州','泰州','镇江','句容','江阴','徐州市','做好','情况','原创','江苏省','丹徒区','仪征市','镇江市','句容市','扬州市','仪征','丹徒','邳州','丹阳']

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
    stopwords = read_file(stopwords_file)
    stopwords += weibo_stopwords
    all_words = []

    for line in lines:
        all_words.append([word for word in jieba.cut(line) if word not in stopwords and len(word) > 1])

    return all_words

input_file = '../data/in/weibojiangsu.csv_yq_content.csv'
html_path = '../data/out/jiangsu.html'
json_path = '../data/out/jiangsu.json'
output_excel = '../data/out/jiangsu_theme.xlsx'

# py.init_notebook_mode()

def plot_difference(mdiff, title="", annotation=None):
    """
    Helper function for plot difference between models
    """
    annotation_html = None
    if annotation is not None:
        annotation_html = [
            [
                "+++ {}<br>--- {}".format(", ".join(int_tokens), ", ".join(diff_tokens)) 
                for (int_tokens, diff_tokens) in row
            ] 
            for row in annotation
        ]
        
    data = go.Heatmap(z=mdiff, colorscale='RdBu', text=annotation_html)
    layout = go.Layout(width=950, height=950, title=title, xaxis=dict(title="topic"), yaxis=dict(title="topic"))
    py.iplot(dict(data=[data], layout=layout))

def main():
    # 按行读取文件
    lines = read_file(input_file)
    
    # 使用正则过滤
    for i in range(len(lines)):
        lines[i] = regex_change(lines[i])
    
    # 去除停用词，并返回词袋字典
    bow_words = delete_stopwords(lines)

    dictionary = corpora.Dictionary(bow_words)
    dictionary.filter_extremes(no_above=0.4)

    corpus = [dictionary.doc2bow(text) for text in bow_words]
    # print(corpus)

    # lda = LdaMulticore(corpus=corpus, num_topics=10, id2word=dictionary, workers=4, eval_every=None, passes=10, batch=True)
    lda = models.LdaModel(corpus=corpus, id2word=dictionary, num_topics=10, random_state=10, update_every=1, chunksize=50, passes=10, alpha='auto', per_word_topics=True)

    # 计算困惑度 (分数越低越好)
    print('Perplexity: ', round(lda.log_perplexity(corpus), 2))

    # 计算连贯性 (分数越高越好)
    coherence_model_lda = CoherenceModel(model=lda, texts=bow_words, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('Coherence Score: ', round(coherence_lda, 2))

    topic_list=lda.print_topics(10)
    print(topic_list)
    wb = xlwt.Workbook() 
    sheet1 = wb.add_sheet('sheet1') 
    for i in range(len(topic_list)):
        topic_id = topic_list[i][0]
        s = str(topic_list[i][1])
        strs = s.split('+')
        sum = float(0)
        for j in range(len(strs)):
            list = str(strs[j]).split('*')
            sum += float(list[0])
            sheet1.write(i, j+1, list[1])
        sheet1.write(i, len(strs)+1, sum)

        # sum = float(0)
        # terms = lda.get_topic_terms(topic_id)
        # print(terms)
        # for j in range(len(terms)):
        #     sum += float(terms[j][1])
        #     sheet1.write(i, j+1, float(terms[j][1]))
        # sheet1.write(i, len(terms)+1, sum)
    wb.save(output_excel)    

    # 使用 pyLDAvis 进行可视化
    data = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
    pyLDAvis.save_json(data, json_path)
    pyLDAvis.save_html(data, html_path)
    # 清屏
    os.system('clear')
    # 浏览器打开 html 文件以查看可视化结果
    os.system(f'start {html_path}')

if __name__ == '__main__':
    main()