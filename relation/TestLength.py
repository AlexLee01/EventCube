import csv
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
def readLine():
    file_path = "J:/weibo.txt"
    line_num = 0
    cnt = 0
    li = []
    try:
        with open(file_path, encoding='utf-8') as file_obj:
            line = file_obj.readline()[5000000:]
            while line_num < 1000000:
                line_num = line_num + 1
                line = file_obj.readline().strip()
                weibo = line.split("\t")
                li.append(len(weibo[18]))
    except OSError:
        print(line_num)
    finally:
        return li
def distribution(data, bins_interval = 1, margin = 1):
    bins = range(min([0,100]), max([0,100]) + bins_interval - 1, bins_interval)
    prob,left,rectangle = plt.hist(x=data, bins=bins, normed=True, histtype='bar', color=['r'])
    for i in range(0, len(bins)):
        print(bins[i])
    plt.xlim(min(data) - margin, max(data) + margin)
    plt.title("Probability-distribution")
    plt.xlabel('Interval')
    plt.ylabel('Probability')
    for x, y in zip(left, prob):
        # 字体上边文字
        # 频率分布数据 normed=True
        plt.text(x + bins_interval / 2, y + 0.003, '%.2f' % y, ha='center', va='top')
        # 频次分布数据 normed=False
        # plt.text(x + bins_interval / 2, y + 0.25, '%.2f' % y, ha='center', va='top')
    plt.show()
def main():
    li = readLine()
    #distribution(li)
    plt.hist(li,bins=30)
    plt.show()
if __name__ == "__main__":
    main()
