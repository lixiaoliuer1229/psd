import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 下载必要的资源
nltk.download('punkt')
nltk.download('stopwords')

# 示例文本
text = "自然语言处理是计算机科学领域与人工智能中的一个重要方向。"

# 分词
tokens = word_tokenize(text)
print("分词结果：")
print(tokens)

# 去除停用词
stop_words = set(stopwords.words('chinese'))
filtered_tokens = [word for word in tokens if word not in stop_words]
print("\n去除停用词后的结果：")
print(filtered_tokens)