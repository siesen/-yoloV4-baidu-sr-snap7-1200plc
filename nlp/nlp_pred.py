import sys
import os
sys.path.append('..')
import jieba
import tensorflow as tf
import pickle
import numpy as np
from nlp import baidu

#载入文件路径
mydict_abs=os.path.join(os.path.dirname(__file__),'mydict.txt')
mynlp_model=os.path.join(os.path.dirname(__file__),'nlp.h5')
mytoken=os.path.join(os.path.dirname(__file__),'token.pkl')

class NLP():
    def __init__(self):
        #载入自定义词典
        jieba.load_userdict(mydict_abs)

        #载入模型
        # tf.compat.v1.keras.backend.clear_session()
        self.model=tf.keras.models.load_model(mynlp_model)
        # self.model.make_predict_function()     

        #建立百度语音连接        
        self.baidu_sr=baidu.Baidu_sr()

        #read token from pickle
        with open(mytoken,'rb') as f:
            self.token=pickle.load(f)
        
    def predict(self):
        #读取语音
        for text in self.baidu_sr.speech_recog():
            if text=='Error' or text[:5]=='Info:':
                # yield text,None
                yield text+str(8)
            else:
                word_list=jieba.lcut(text)
                #去掉‘吧’，‘了’
                if '吧' in word_list:
                    word_list.remove('吧')
                if '了' in word_list:
                    word_list.remove('了')
                #文字转数字列表，建立词汇索引
                texts_sq=self.token.texts_to_sequences([word_list])
                x_test=tf.keras.preprocessing.sequence.pad_sequences(texts_sq,padding='post',truncating='post',maxlen=8)
                # tf.compat.v1.disable_v2_behavior()
                # global graph
                # graph=tf.compat.v1.get_default_graph()
                # with graph.as_default():
                #解决keras载入多个模型出错的问题，耗资源，需要改进,有知道的请告诉我
                try:
                    # tf.keras.backend.clear_session()
                    a=self.model.predict(x_test)
                except:
                    tf.keras.backend.clear_session()
                    self.model=tf.keras.models.load_model(mynlp_model)
                    a=self.model.predict(x_test)
                # print(a[0])
                #置信度>0.8，认为命令是能正确认识的
                # yield text,np.argmax(a[0]) if max(a[0])>0.8 else text,None
                yield text+str(np.argmax(a[0])) if max(a[0])>0.8 else text+str(8)

if __name__=='__main__':
    a=NLP()
    while(1):
        for text in a.predict():
            print(text)
