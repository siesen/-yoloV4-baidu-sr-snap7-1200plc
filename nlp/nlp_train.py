import jieba
import os
import tensorflow as tf
import numpy as np
import pickle
# tf.compat.v1.disable_v2_behavior()

folders='train'

#载入自定义词典
jieba.load_userdict('mydict.txt')

#筛选掉不是文件的文件
subfolders=os.listdir(folders)
for each in subfolders:
    if each.find('.')>-1:
        subfolders.remove(each)
subfolders=[os.path.join(folders,i) for i in subfolders]

#读取文件,并分词，获得文本
files_num=[]
texts=[]
for folder in subfolders:
    files=os.listdir(folder)
    files_num.append(len(files))
    for each in files:
        path=os.path.join(folder,each)
        with open(path,'r') as f:
            text=f.read()
            word_list=jieba.lcut(text)
            #去掉‘吧’，‘了’
            if '吧' in word_list:
                word_list.remove('吧')
            if '了' in word_list:
                word_list.remove('了') 
            texts.append(word_list)

#获得标签
labels=[]
for i,ele in enumerate(files_num):
    for j in range(ele):
        labels.append(i)

#建立词汇词典
token=tf.keras.preprocessing.text.Tokenizer(num_words=30,filters="!#$%&()*+,-.。！？，/:;<=>?@[\\]^_`{|}~\t\n")
token.fit_on_texts(texts)
#print(token.document_count)
print(token.word_index)
#print(token.word_counts)

#保存token词汇索引
with open('token.pkl','wb') as f:
    pickle.dump(token,f,protocol=pickle.HIGHEST_PROTOCOL)


#文字转数字列表，建立词汇索引
texts_sq=token.texts_to_sequences(texts)
#print(texts_sq)

#padding
x_texts=tf.keras.preprocessing.sequence.pad_sequences(texts_sq,padding='post',truncating='post',maxlen=8)

#shuffle数据
q=list(zip(x_texts,labels))
np.random.shuffle(q)
x_train=[i[0] for i in q]
y_train=[i[1] for i in q]

#tricks,如果说的命令不在7大类中，添加第8类，放说的废话
x_train.insert(0,np.zeros(8))
x_train=np.asarray(x_train,dtype=np.float)
y_train.insert(0,7)
y_train=np.asarray(y_train,dtype=np.float)

#建立模型
model=tf.keras.models.Sequential([tf.keras.layers.Embedding(output_dim=4,input_dim=30,input_length=8),
                                 tf.keras.layers.Flatten(),
                                 tf.keras.layers.Dense(units=256,activation='relu'),
                                 tf.keras.layers.Dense(units=8,activation='softmax')])

#model.summary()
      
model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

history=model.fit(x_train,
                  y_train,
                #   validation_split=0.1,
                  epochs=100,
                  batch_size=2,
                  verbose=2)

model.save('nlp.h5')

#test
def test(text):
    word_list=jieba.lcut(text)
    #文字转数字列表，建立词汇索引
    texts_sq=token.texts_to_sequences([word_list])
    x_test=tf.keras.preprocessing.sequence.pad_sequences(texts_sq,padding='post',truncating='post',maxlen=8)
    print(x_test)
    a=model.predict(x_test)
    return a

b=test('你在干嘛呢')
print(b)




