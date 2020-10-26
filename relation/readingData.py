import pymysql.cursors
import logging
import traceback

file_path = "D:/weibo.txt"

line_num = 0

logging.basicConfig(filename='D:/data_load.log', level=logging.INFO)

with open(file_path, encoding='utf-8') as file_obj:
    line = file_obj.readline()
    while line != '':
        print(line)
        line_num = line_num + 1
        print("\nline No.:", line_num)
        line = file_obj.readline().strip()
        weibo = line.split("\t")
        # in_weibo.append(tuple(weibo))
        # if line_num % 50 == 0:
        conn = pymysql.connect(host='localhost', user='root', passwd='youp', db='weibo', charset='utf8mb4')
        sql = """insert into `bigdata`( `weiboId`,       
                                        `attitudes_count`,       
                                        `bmiddle_pic`,      
                                        `comments_count`,       
                                        `created_at`,      
                                        `favorited`,       
                                        `geo`,       
                                        `id`,       
                                        `idstr`,      
                                        `in_reply_to_screen_name`,       
                                        `in_reply_to_status_id`,       
                                        `in_reply_to_user_id`,       
                                        `mid`,       
                                        `mlevel`,       
                                        `original_pic`,       
                                        `pic_urls`,       
                                        `reposts_count`,       
                                        `source`,       
                                        `text`,       
                                        `thumbnail_pic`,       
                                        `truncated`,       
                                        `uid`,       
                                        `visible`,
                                        `retweeted_status_id`,
                                        `gatherTime`)'''
                                        
                                    

