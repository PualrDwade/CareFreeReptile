# -*- coding: utf-8 -*-

import pymysql
from . import settings

import codecs
import json
# 门票信息爬取的数据库模块

class CityJsonPipeline(object):
    def __init__(self):
        self.file = codecs.open('data.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(jsontext)
        return item

    def spider_closed(self, spider):
        self.file.close()


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
        self.cursor = self.connect.cursor()
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
        self.cursor = self.connect.cursor()
        print('connect success')

    # 定义处理函数
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_hotelmsg(id, name, score, hotel_price ,hotel_content,img_url,hotel_link,scenic_id,supplier_id_id,latest_time,sell_num)
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


# 攻略信息爬取的数据库模块
class StrategyPipeline(object):
    """
            docstring
            for TicketsSpiderPipeline"""

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
        self.cursor = self.connect.cursor()
        print('connect success')

    # 定义处理函数
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_strategymsg(id, title, link_url,
            simple_content, img_url, supplier_id_id, scenic_name)
            values ( % s, % s, % s, % s, % s, % s, % s)""",
                (item['id'],
                 item['title'],
                 item['link_url'],
                 item['simple_content'],
                 item['img_url'],
                 item['supplier'],
                 item['scenic_name'],
                 )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 产品信息爬取的数据库模块
class Ctrip_productItemPipeline(object):
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
        self.cursor = self.connect.cursor()
        print('connect success')

    # 定义处理函数
    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """
            insert into ProductDT_productmsg(id, name, product_link, sell_num,
             supplier_id, score, product_type, traver_days,comments_num, img_url, product_grade)
            values( % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)""",
                (item['id'],
                 item['product_name'],
                 item['prd_url'],
                 item['sales_volume'],
                 item['supplier'],
                 item['score_s'],
                 item['sr_team'],
                 item['schedule_days'],
                 item['comments_num'],
                 item['prd_img'],
                 item['product_grade'],
                 )
            )
            # 插入完成提交sql语句
            print('插入产品信息')
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 产品景点
class product_scenic_Item_Pipeline(object):
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
        self.cursor = self.connect.cursor()
        print('connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_product_senic(id, senic_name,product_id)
            values ( % s, % s,% s) """,
                (item['id'],  # 自增id
                 item['scenic_name'],
                 item['product_id']
                 )
            )
            print('插入产品景点')
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 产品、出发城市、起价
class product_city_Item_Pipeline(object):
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
        self.cursor = self.connect.cursor()
        print('connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_product_city(id,product_id,city_id, product_price)
            values ( % s, % s, % s, % s) """,
                (item['id'],
                 item['product_id'],
                 item['city_id'],
                 item['product_price'],
                 )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 产品景点
class Ctrip_product_scenic_Item_Pipeline():
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
        self.cursor = self.connect.cursor()
        print('connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_product_city(id, scenic_name)
                values (%s,%s) """,
                (item['id'],
                 item['scenic_name'],
                )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item



# 产品、出发城市、起价
class Ctrip_product_fromcity_price_Item_Pipeline():
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
        self.cursor = self.connect.cursor()
        print('connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into ProductDT_product_city(ID, id, city_id, product_price)
                values (%s,%s,%s,%s) """,
                (item['ID'],
                 item['id'],
                 item['city_id'],
                 item['product_price'],
                )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item


# 省份信息插入
class Province_Item_Pipeline():
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
        self.cursor = self.connect.cursor()
        print('Province_Item_Pipeline connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into TraverMsg_provincemsg(id, name, img_url)
                values (%s,%s,%s) """,
                (item['province_id'],
                 item['province_name'],
                 item['province_img_url']
                )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item



# 城市信息插入
class City_Item_Pipeline():
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
        self.cursor = self.connect.cursor()
        print('City_Item_Pipeline connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into TraverMsg_citymsg(id, name, img_url, province_name)
                values (%s,%s,%s,%s) """,
                (item['city_id'],
                 item['city_name'],
                 item['city_img_url'],
                 item['provinceName']
                )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item



# 景点信息插入
class Scenic_Item_Pipeline():
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
        self.cursor = self.connect.cursor()
        print('Scenic_Item_Pipeline connect success')

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                """insert into TraverMsg_scenicmsg(id, name, city_name, img_url, address, basic_desc, link_url, popular_level)
                values (%s,%s,%s,%s,%s,%s,%s,%s) """,
                (item['scenic_id'],
                 item['scenic_name'],
                 item['city_name'],
                 item['scenic_img_url'],
                 item['address'],
                 item['basic_desc'],
                 item['link_url'],
                 item['popular_level']
                )
            )
            # 插入完成提交sql语句
            self.connect.commit()
        except Exception as error:
            # 出现错误时打印错误消息
            print(error)
        return item