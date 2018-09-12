# -*- coding: utf-8 -*-

import pymysql
from . import settings


# 门票信息爬取的数据库模块
class TicketSpiderPipeline(object):
    """docstring for TicketsSpiderPipeline"""

    def __init__(self):
        # 链接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 然后通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        print('connect success')

    # 定义处理函数
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_ticketsmsg(id,ticket_content,ticket_price,ticket_link,scenic_name,supplier_id_id,
scense_address,city_id,img_url,score)
                values (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s)""",
                (item['id'],
                 item['description'],
                 item['price'],
                 item['ticket_url'],
                 item['name'],
                 item['supplier'],
                 item['address'],
                 item['city'],
                 item['ticket_img'],
                 item['grade']
                 )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 酒店信息爬取的数据库模块
class HotelSpiderPipeline(object):
    def __init__(self):
        # 链接数据库
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            charset='utf8',
            use_unicode=True)
        # 然后通过cursor执行增删查改
        self.cursor = self.connect.cursor();
        print('connect success')

    # 定义处理函数
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_hotelmsg(id, name, score, hotel_price ,
hotel_content,img_url,hotel_link,scenic_id,supplier_id_id,latest_time,sell_num)
                values (%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)""",
                (item['id'],
                 item['name'],
                 item['score'],
                 item['hotel_price'],
                 item['hotel_content'],
                 item['img_url'],
                 item['hotel_link'],
                 item['scenic_id'],
                 item['supplier_id'],
                 item['latest_time'],
                 item['sell_num']
                 )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item
