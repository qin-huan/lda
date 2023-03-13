import pyLDAvis.sklearn
import pyLDAvis
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pandas as pd
import jieba
import re
import os

# 待做 LDA 的文本 csv 文件，可以是本地文件，也可以是远程文件，一定要保证它是存在的！！！！
source_csv_path = 'all_yq_content.csv'
# 文本 csv 文件里面文本所处的列名,注意这里一定要填对，要不然会报错的！！！
document_column_name = '微博正文'
# 输出主题词的文件路径
top_words_csv_path = './out/top-topic-words.csv'
# 输出各文档所属主题的文件路径
predict_topic_csv_path = './out/document-distribution.csv'
# 可视化 html 文件路径
html_path = './out/document-lda-visualization.html'
# 选定的主题数
n_topics = 10
# 要输出的每个主题的前 n_top_words 个主题词数
n_top_words = 10
# 去除无意义字符的正则表达式
pattern = u'[\\s\\d,.<>/?:;\'\"[\\]{}()\\|~!\t"@#$%^&*\\-_=+，。\n《》、？：；“”‘’｛｝【】（）…￥！—┄－]+'

def top_words_data_frame(model: LatentDirichletAllocation,
                         tf_idf_vectorizer: TfidfVectorizer,
                         n_top_words: int) -> pd.DataFrame:
    '''
    求出每个主题的前 n_top_words 个词

    Parameters
    ----------
    model : sklearn 的 LatentDirichletAllocation 
    tf_idf_vectorizer : sklearn 的 TfidfVectorizer
    n_top_words :前 n_top_words 个主题词

    Return
    ------
    DataFrame: 包含主题词分布情况
    '''
    rows = []
    feature_names = tf_idf_vectorizer.get_feature_names_out()
    for topic in model.components_:
        top_words = [feature_names[i]
                     for i in topic.argsort()[:-n_top_words - 1:-1]]
        rows.append(top_words)
    columns = [f'topic word {i+1}' for i in range(n_top_words)]
    df = pd.DataFrame(rows, columns=columns)

    return df


def predict_to_data_frame(model: LatentDirichletAllocation, X: np.ndarray) -> pd.DataFrame:
    '''
    求出文档主题概率分布情况

    Parameters
    ----------
    model : sklearn 的 LatentDirichletAllocation 
    X : 词向量矩阵

    Return
    ------
    DataFrame: 包含主题词分布情况
    '''
    matrix = model.transform(X)
    columns = [f'P(topic {i+1})' for i in range(len(model.components_))]
    df = pd.DataFrame(matrix, columns=columns)
    return df


df = (
    pd.read_csv(
        source_csv_path,
        encoding='utf-8')
    .drop_duplicates()
    .rename(columns={
        document_column_name: 'text'
    }))

stopwordsFile = 'stop_words.txt'
weiboStopWords = ['转发','微博','全文','为了','此间','味儿','近日','全省','我市','新闻','视频','小时','展开','工作','原图','期间','江苏','常州','淮安','连云港','南京','南通','宿迁','苏州','徐州','无锡','盐城','扬州','泰州','镇江','组图','张','例', '市', '省']

#按行读取文件，返回文件的行字符串列表
def read_file(file_name):
    fp = open(file_name, "r", encoding="utf-8")
    content_lines = fp.readlines()
    fp.close()
    #去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines

stopwords = read_file(stopwordsFile)
stopwords += weiboStopWords

# # 设置停用词集合
# stop_words_set = set(['转发','微博','?','...','#','全文','为了','怎么','此间','味儿','正浓','其实','那么','着急','没有','关系','不要','种','什么','有','下午','的','最为','我们','双臂','越','会','却','做','有个','是','不','的','_','上午','第四次','中心','一年','展开','情况','日晚','参加','我市','全省','近日','年月日','一年','今日','期间','早安','关注','时间','现场','身边','举办','做好','相关','来到','网页','链接','视频','新闻','小时','展开','工作','年月日时','降降','cn','http'])
# stop_words = pd.read_table('./stop_words.txt', names=['records'])
# for i in range(len(stop_words)):
#     stop_words_set.add(stop_words['records'][i])
# print(len(stop_words_set))

# 去重、去缺失、分词
df['cut'] = (
    df['text']
    .apply(lambda x: str(x))
    .apply(lambda x: re.sub(pattern, ' ', x))
    .apply(lambda x: " ".join([word for word in jieba.lcut(x) if word not in set(stopwords)]))
)

# 构造 tf-idf
tf_idf_vectorizer = TfidfVectorizer()
tf_idf = tf_idf_vectorizer.fit_transform(df['cut'])

lda = LatentDirichletAllocation(
    n_components=n_topics,
    max_iter=100,
    learning_method='online',
    learning_offset=50,
    random_state=5)

# 使用 tf_idf 语料训练 lda 模型
lda.fit(tf_idf)

# 计算 n_top_words 个主题词
top_words_df = top_words_data_frame(lda, tf_idf_vectorizer, n_top_words)

# 保存 n_top_words 个主题词到 csv 文件中
top_words_df.to_csv(top_words_csv_path, encoding='utf-8-sig', index=None)

# 转 tf_idf 为数组，以便后面使用它来对文本主题概率分布进行计算
X = tf_idf.toarray()

# 计算完毕主题概率分布情况
predict_df = predict_to_data_frame(lda, X)

# 保存文本主题概率分布到 csv 文件中
predict_df.to_csv(predict_topic_csv_path, encoding='utf-8-sig', index=None)

# 使用 pyLDAvis 进行可视化
data = pyLDAvis.sklearn.prepare(lda, tf_idf, tf_idf_vectorizer)
pyLDAvis.save_html(data, html_path)
# 清屏
os.system('clear')
# 浏览器打开 html 文件以查看可视化结果
os.system(f'start {html_path}')

print('本次生成了文件：',
      top_words_csv_path,
      predict_topic_csv_path,
      html_path)