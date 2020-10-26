
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import csv
import pandas as pd
import numpy as np
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号'


def readFile(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows
def getID(rows):
    id = ''
    users = []
    for row in rows[1:]:
        if id != row[0]:
            id = row[0]
            users.append(id)
    return users
def read_draw_from_csv(rows):
    users = getID(rows)
    for id in users:
        print(id)
        readcsv = id + ".csv"
        df = readDate(readcsv)
        '''
        username = df['username']
        time = df['time']
        sentiment = df['sentiment']

        content = df['content']
        location = df['location']
        window = 7
        df['sadness_SMA7'] = df.sadness.rolling(window=window).mean()
        df['sadness_SMA7'].plot()
        df['happiness_SMA7'] = df.happiness.rolling(window=window).mean()
        df['happiness_SMA7'].plot()
        df['disgust_SMA7'] = df.disgust.rolling(window=window).mean()
        df['disgust_SMA7'].plot()
        df['surprise_SMA7'] = df.surprise.rolling(window=window).mean()
        df['surprise_SMA7'].plot()
        df['anger_SMA7'] = df.anger.rolling(window=window).mean()
        df['anger_SMA7'].plot()
        df['like_SMA7'] = df.like.rolling(window=window).mean()
        df['like_SMA7'].plot()
        df['fear_SMA7'] = df.fear.rolling(window=window).mean()
        df['fear_SMA7'].plot()
        surprise = df['surprise']
        sadness = df['sadness']
        disgust = df['disgust']
        happiness = df['happiness']
        anger= df['anger']
        like = df['like']
        fear = df['fear']
        plt.bar(time, sadness, label="sadness")
        plt.bar(time, happiness, label="happiness")
        plt.bar(time, disgust, label="disgust")
        plt.bar(time, surprise, label="surprise")
        plt.bar(time, anger, label="anger")
        plt.bar(time, like, label="like")
        plt.bar(time, fear, label="fear")

        plt.legend(loc='upper left')  # 图例的位置是左上
        plt.xlabel('Date')  # X轴标签
        plt.ylabel('percentage')  # Y轴标签
        plt.title(id)  # 折线图标题
        plt.show()
        '''
def draw(rows):
    id = ''
    lines = []
    users = []
    for row in rows[1:]:
        if id != row[0]:
            users.append(lines)
            lines = []
            id = row[0]
        lines.append(row)
    users.append(lines)
    for user in users[1:]:
        for i in range(len(user)):
            for j in range(7):
                user[i][j+3] = float(user[i][j+3] )
        df = pd.DataFrame(user, columns=['username', 'time', 'sentiment', 'surprise', 'sadness','disgust', 'happiness', 'anger', 'like', 'fear','content','location','gender'])

        username = user[0][0]
        outcsv = username+".csv"
        df.to_csv(outcsv)
def readDate(path):
    df = pd.read_csv(path)

    date = []
    month = []
    year = []
    hour = []
    minute = []
    for string in df['time']:
        timeList = string.split()
        dateList = timeList[0].split('/')
        time = timeList[1].split(':')
        date.append(int(dateList[0]))
        month.append(int(dateList[1]))
        year.append(int(dateList[2]))
        hour.append(int(time[0]))
        minute.append(int(time[1]))
    df['year'] = year
    df['month'] = month
    df['date'] = date
    df['hour'] = hour
    df['minute'] = minute
    return df
def drawbyDate(rows):
    users = getID(rows)
    for id in users:
        print(id)
        readcsv = id + ".csv"
        df = readDate(readcsv)
        time = pd.to_datetime(df['time'])
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))  # 設置x軸主刻度顯示格式（日期）
        plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # 設置x軸主刻度間距
        plt.bar(time, df.sadness, label="sadness")
        plt.bar(time, df.happiness, label="happiness")
        plt.bar(time, df.disgust, label="disgust")
        plt.bar(time, df.surprise, label="surprise")
        plt.bar(time, df.anger, label="anger")
        plt.bar(time, df.like, label="like")
        plt.bar(time, df.fear, label="fear")

        plt.legend(loc='upper left')  # 图例的位置是左上
        plt.xlabel('Date')  # X轴标签
        plt.ylabel('percentage')  # Y轴标签
        plt.title(id)  # 折线图标题
        plt.show()
def main():
    path = "predictResult.csv"
    rows = readFile(path)
    #draw(rows)
    #read_draw_from_csv(rows)
    drawbyDate(rows)
if __name__ == "__main__":
    main()
