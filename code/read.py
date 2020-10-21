from numpy.random import randn
import matplotlib.pyplot as plt
import csv
import pandas as pd
def readFile(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
    return rows
def read_draw_from_csv(rows):
    id = ''
    users = []
    for row in rows[1:]:
        if id != row[0]:
            id = row[0]
            users.append(id)
    for id in users:
        print(id)
        readcsv = id + ".csv"
        df = pd.read_csv(readcsv)
        username = df['username']
        time = df['time']
        sentiment = df['sentiment']
        surprise = df['surprise']
        #df['sadness'] = float(df['sadness'])
        sadness = df['sadness']
        disgust = df['disgust']
        happiness = df['happiness']
        anger= df['anger']
        like = df['like']
        fear = df['fear']
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
        '''
        location = user[0][-2]
        gender =  user[0][-1]
        time, sentiment, surprise, disgust, happiness, anger, like, fear = [],[],[],[],[],[],[],[]
        sadness = []
        
        for weibo in user:
            time.append(weibo[1])
            sentiment.append(weibo[2])
            surprise.append(float(weibo[3]))
            #if float(weibo[4]) > 0.6:
            #    sadness[weibo[1]] = float(weibo[4])
            sadness.append(float(weibo[4]))
            disgust.append(float(weibo[5]))
            happiness.append(float(weibo[6]))
            anger.append(float(weibo[7]))
            like.append(float(weibo[8]))
            fear.append(float(weibo[9]))

        #print(sadness)

                #print(time, sentiment, surprise, sadness, disgust, happiness, anger, like, fear)
        colors = "#000000"  # 定义颜色
        label = "sadness"  # 图例标签


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
        plt.title(username)  # 折线图标题
        print(username)
        plt.show()
        '''

def main():
    path = "predictResult.csv"
    rows = readFile(path)
    #draw(rows)
    read_draw_from_csv(rows)
if __name__ == "__main__":
    main()
