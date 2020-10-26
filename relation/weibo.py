import csv
import jieba
import jieba.posseg as seg
import chardet
from model_predict import predict

def readfile():
    jieba.enable_paddle()
    csvFile = open("weibo.csv", "r", encoding='UTF-8')
    reader = csv.reader((line.replace('\0','') for line in csvFile))
    result = []
    for item in reader:
        # 忽略第一行
        if reader.line_num == 1:
            continue
        result.append(item[1:])
    csvFile.close()
    return result



def name(results):
    #传入整个excel数据, length=5
    #字段为 id, time_created, content, location, gender

    List = []
    for result in results:
        text =result[2]
        words = seg.cut(text,use_paddle = True)
        # store names in li
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
                        List.append("#".join([li[i],li[j],text]))
            else:
                if len(li)==1:
                    li.append(result[0])#如果只提取到一个人名，则用username代替另一个
                li.append(text)
                List.append("#".join(li))

    return List

def openExcel(path):
    jieba.enable_paddle()
    '''
    f = open(path,'rb')
    r = f.read()
    r.decode(encoding='utf-8')
    f_charInfo = chardet.detect(r)
    print(f_charInfo)
    #print(r.decode(f_charInfo['encoding']))
    f.close()
    return 0
    '''
    with open(path, "r", encoding='utf-8') as file:
        result = []
        line = file.readline()
        print(line)
        line_num = 0
        while line != "":
            line_num +=1
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


def main():

    path = 'J:/weibodata/a.csv'
    #result = readfile()
    result = openExcel(path)
    print(result)
    List = name(result)
    print(List)

    relations = (predict(List))

    f = open('relation.csv','w',encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["number","person1", "person2", "relation","content","time_created"])
    for number in range(len(relations)):
        relation = relations[number]
        if relation[2] != '':
            csv_writer.writerow([number]+relation+[result[number][1]])





if __name__ == "__main__":
    main()
