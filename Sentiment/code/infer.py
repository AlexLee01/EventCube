import numpy as np
import  jieba
import re
from keras.models import load_model
import gensim
from gensim.models.word2vec import Word2Vec
from keras.preprocessing import sequence
import csv
import yaml

def readFile(path):
    with open(path, "r", encoding='utf-8') as file:
        result = []
        line = file.readline()
        line_num = 0
        while line != "":
            line_num += 1
            line = file.readline().strip()
            try:
                weibo = line.split("\t")
                weibo[2] = weibo[2].replace(u'\u200b', '')
                weibo[2] = weibo[2].replace(u'\xa0', '')
                result.append(weibo)
            except:
                print("error")
                continue
    return result
def evaluate(model):
    from lstm import lstm
    from word2vec import word2vec_train
    from dataset import loadfile, clean_data
    import keras.utils
    from keras.preprocessing import sequence
    from sklearn.model_selection import train_test_split
    from train import data2inx
    voc_dim = 150  # word的向量维度
    batch_size = 32  # batch
    X_Vec = np.load('tokened_text.npy', allow_pickle = True)
    y = np.load('y.npy', allow_pickle = True)

    print("下载数据完成................")
    print("开始构建词向量................")
    input_dim, embedding_weights, w2dic = word2vec_train(X_Vec)
    print("构建词向量完成................")

    index = data2inx(w2dic, X_Vec)
    index2 = sequence.pad_sequences(index, maxlen=voc_dim)
    x_train, x_test, y_train, y_test = train_test_split(index2, y, test_size=0.2, random_state=1)
    y_train = keras.utils.to_categorical(y_train, num_classes=7)
    y_test = keras.utils.to_categorical(y_test, num_classes=7)
    print("Evaluate...")
    print(model.predict(x_test))
    score = model.evaluate(x_test, y_test,
                           batch_size=batch_size)
    print(model.metrics_names)
    print('Test score:', score)
    """
    ['loss', 'mae', 'acc']
    Test score: [0.5281349422051703, 0.14651137590408325, 0.8690578937530518]
    """
def predict(predictList):

    model = load_model('../model/lstm_java_total.h5')
    #evaluate(model)

    voc_dim = 150

    model_word=Word2Vec.load('../model/Word2Vec_java.pkl')

    input_dim = len(model_word.wv.vocab.keys()) + 1
    embedding_weights = np.zeros((input_dim, voc_dim))
    w2dic={}
    for i in range(len(model_word.wv.vocab.keys())):
        embedding_weights[i+1, :] = model_word [list(model_word.wv.vocab.keys())[i]]
        w2dic[list(model_word.wv.vocab.keys())[i]]=i+1

    pchinese = re.compile('([\u4e00-\u9fa5]+)+?')


    label={0:"surprise",1:"sadness",2:"disgust",3:"happiness",4:"anger",5:"like",6:"fear"}
    with open("predictResult.csv", "w", encoding='utf-8', newline='') as csvFile:
        csv_writer = csv.writer(csvFile)
        csv_writer.writerow(["ID","Published time","Sentiment","surprise","sadness","disgust","happiness","anger","like","fear","context","location","gender"])
        for weibo in predictList:
            in_stc=''.join(pchinese.findall(weibo[2]))
            in_stc=list(jieba.cut(in_stc,cut_all=True, HMM=False))
            new_txt=[]
            data=[]
            for word in in_stc:
                try:
                    new_txt.append(w2dic[word])
                except:
                    new_txt.append(0)
            data.append(new_txt)

            data=sequence.pad_sequences(data, maxlen=voc_dim )
            pre=model.predict(data)[0].tolist()
            csv_writer.writerow(weibo[0:2]+[label[pre.index(max(pre))]]+pre+weibo[2:])


def main():
    path = 'J:/weibodata/a.csv'
    predictList = readFile(path)
    predict(predictList)
if __name__ == "__main__":
    main()
