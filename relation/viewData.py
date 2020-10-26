import csv

file_path = "J:/weibo.txt"

line_num = 0
'''
f = open('weibo.csv','a+',encoding='utf-8',newline='')
csv_writer = csv.writer(f)
csv_writer.writerow(["LineNumber","CreatedTime","UserID","content"])
'''
with open(file_path, encoding='utf-8') as file_obj:
    line = file_obj.readline()
    while line_num < 10000:
        line_num = line_num + 1
        #print("\nline No.:", line_num)
        line = file_obj.readline().strip()
        weibo = line.split("\t")
        if weibo[6] != "":
            geo = weibo[6].split("#")
            print(geo[-2:])
        #csv_writer.writerow([line_num, weibo[4], weibo[21], weibo[18]])
        print("This is line ",line_num,end="\r")
