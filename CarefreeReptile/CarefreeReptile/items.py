# -*- coding: utf-8 -*-
from scrapy import Item, Field


# 携程的酒店信息字段
<<<<<<< HEAD
class HotelMsgItem(scrapy.Item):
=======
class Ctrip_HotelMsgItem(Item):
>>>>>>> 459975b5ff89dac74f3f77c5d399e30edc393ab1
    # 酒店id
    id = Field()
    # 酒店名字
    name = Field()
    # 酒店评分
    score = Field()
    # 酒店价格(起价)
    hotel_price = Field()
    # 酒店简介(包括位置)
    hotel_content = Field()
    # 图片url(可以为空)
    img_url = Field()
    # 酒店链接(必须要有,直接跳转到对应商家的链接上去)
    hotel_link = Field()
    # 所属景点(可以为空)
    scenic_id = Field()
    # 供应商(可以为空,具体看爬取的是哪个网站)
    supplier_id = Field()
    # 最近动态
    latest_time = Field()
    # 人气
    sell_num = Field()


<<<<<<< HEAD
class TicketItem(scrapy.Item):
    id = scrapy.Field()  # 门票ID
    name = scrapy.Field()  # 所属景点名称
    ticket_url = scrapy.Field()  # 门票具体地址URL
    ticket_img = scrapy.Field()  # 门票图片URL
    address = scrapy.Field()  # 地址
    city = scrapy.Field()  # 所属城市
    description = scrapy.Field()  # 门票描述
    grade = scrapy.Field()  # 评分（5分满分）
    price = scrapy.Field()  # 门票价格
    supplier = scrapy.Field()  # 供应商
=======
# 美团的酒店信息字段
class Meituan_HotelMsgItem(Item):
    # 在此定义数据库字段
    # 酒店id
    id = Field()
    # 酒店名字
    name = Field()
    # 酒店评分
    score = Field()
    # 酒店价格(起价)
    hotel_price = Field()
    # 酒店简介(包括位置)
    hotel_content = Field()
    # 图片url(可以为空)
    img_url = Field()
    # 酒店链接(必须要有,直接跳转到对应商家的链接上去)
    hotel_link = Field()
    # 所属景点(可以为空)
    scenic_id = Field()
    # 供应商(可以为空,具体看爬取的是哪个网站)
    supplier_id = Field()
    # 最近动态
    latest_time = Field()
    # 人气
    sell_num = Field()


# 携程的门票信息字段
class Ctrip_TicketItem(Item):
    id = Field()  # 门票ID
    name = Field()  # 所属景点名称
    ticket_url = Field()  # 门票具体地址URL
    ticket_img = Field()  # 门票图片URL
    address = Field()  # 地址
    city = Field()  # 所属城市
    description = Field()  # 门票描述
    grade = Field()  # 评分（5分满分）
    price = Field()  # 门票价格
    supplier = Field()  # 供应商


# 携程的产品信息字段
class Ctrip_productItem(Item):
    product_name = Field()  # 产品名字
    id = Field()            #产品id
    # prd_num = Field()  # 产品编号
    schedule_days = Field()  # 产品行程天数
    sr_team = Field()  # 产品类型
    supplier = Field() # 产品供应商
    score_s = Field()  # 评分
    comments_num = Field()  # 评论数
    sales_volume = Field()  # 销售量
    product_grade = Field()  # 产品等级、钻级
    departs_citys = Field()  # 出发城市
    price = Field()  # 各个出发城市起价
    prd_url = Field()  # 产品链接
    prd_img = Field()  # 产品图片
    prd_scenic = Field()  # 产品景点
>>>>>>> 459975b5ff89dac74f3f77c5d399e30edc393ab1
