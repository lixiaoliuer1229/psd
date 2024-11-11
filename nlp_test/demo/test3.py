import spacy

# 加载预训练的中文模型
nlp = spacy.blank("zh")

# 处理文本
doc = nlp("自然语言处理是计算机科学领域与人工智能中的一个重要方向。")

# 词性标注
print("\n词性标注：")
for token in doc:
    print(f"{token.text}: {token.pos_}")

# 命名实体识别
print("\n命名实体识别：")
for ent in doc.ents:
    print(f"{ent.text}: {ent.label_}")