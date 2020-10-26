import jieba
import numpy as np
import re
def readFile(path):
    with open(path, 'r', encoding='utf-8') as f:
        sentiment = []
        data = []
        for line in f.readlines():
            line = line.strip()
            line = line.split(':')
            sentiment.append(line[0])
            data.append(line)
        sentiment = list(set(sentiment))
        return sentiment, data

def prepare(sentiment, data):
    """

    :param sentiment: a list of all sentiments
    :param data: list of sentiment and sentence
    :return: list of sentiment and sentence
    """
    pchinese = re.compile('([\u4e00-\u9fa5]+)+?')
    ret_li = []
    length = 0
    for sen in sentiment:
        print(sen)
        for datum in data:
            if datum[0] == sen:
                m = pchinese.findall(str(datum[1]))
                if m:
                    ret_li.append(list(jieba.cut(str(''.join(m)))))
        print((len(ret_li)-length))
        length = len(ret_li)
    return ret_li
def creatY():
    y = np.concatenate((np.zeros(1011, dtype=int),
                        np.ones(14043, dtype=int),
                        2*np.ones(4870, dtype=int),
                        3*np.ones(9939, dtype=int),
                        4*np.ones(4562, dtype=int),
                        5*np.ones(4535, dtype=int),
                        6*np.ones(661, dtype=int)))

    np.save("y.npy", y)

#def cut(data)
def main():
    path = 'J:\sentiment\huati_filter_final_posts_no_sge.txt'
    sentiment, data = readFile(path)
    '''

    data = prepare(sentiment, data)
    data = np.array(data)
    np.save("tokened_text.npy",data)
    '''
    creatY()

if __name__ == '__main__':
    main()

"""
anger4562
disgust4876
surprise1011
fear661
like4540
happiness9959
sadness14052
"""