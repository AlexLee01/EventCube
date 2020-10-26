import csv
import jieba
import jieba.posseg as seg
import pandas as pd
import os, json
import numpy as np
from bert.extract_feature import BertVector
from keras.models import load_model
from att import Attention
from model_predict import predict
def name():
    jieba.enable_paddle()
    csvFile = open("data1.csv", "r", encoding='UTF-8')
    reader = csv.reader(csvFile)
    result = []
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        result.append(item[1])
    csvFile.close()
    List = []
    for text in result[:1000]:
        words = seg.cut(text,use_paddle = True)
        li = []
        for word, flag in words:
            if flag == "PER":
                li.append(word)
        #delete the repeated items
        li = list(set(li))
        if li != []:
            #multi-names cases
            if len(li)>2:
                for i in range(len(li)):
                    for j in range(i+1,len(li)):
                        segLi = [li[i],li[j],text]
                        List.append("#".join(segLi))
            else:
                if len(li)==1:
                    li.append("none")
                li.append(text)    
                List.append("#".join(li))

    return List



def main():
    List = name()
    print(List)
    predict(List)

if __name__ == "__main__":
    main()
