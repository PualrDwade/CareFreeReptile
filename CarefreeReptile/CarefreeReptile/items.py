# -*- coding: utf-8 -*-
import scrapy


# 携程的酒店信息字段
class Ctrip_HotelMsgItem(scrapy.Item):
    # 酒店id
    id = scrapy.Field()
    # 酒店名字
    name = scrapy.Field()
    # 酒店评分
    score = scrapy.Field()
    # 酒店价格(起价)
    hotel_price = scrapy.Field()
    # 酒店简介(包括位置)
    hotel_content = scrapy.Field()
    # 图片url(可以为空)
    img_url = scrapy.Field()
    # 酒店链接(必须要有,直接跳转到对应商家的链接上去)
    hotel_link = scrapy.Field()
    # 所属景点(可以为空)
    scenic_id = scrapy.Field()
    # 供应商(可以为空,具体看爬取的是哪个网站)
    supplier_id = scrapy.Field()
    # 最近动态
    latest_time = scrapy.Field()
    # 人气
    sell_num = scrapy.Field()


# 美团的酒店信息字段
class Meituan_HotelMsgItem(scrapy.Item):
    # 在此定义数据库字段
    # 酒店id
    id = scrapy.Field()
    # 酒店名字
    name = scrapy.Field()
    # 酒店评分
    score = scrapy.Field()
    # 酒店价格(起价)
    hotel_price = scrapy.Field()
    # 酒店简介(包括位置)
    hotel_content = scrapy.Field()
    # 图片url(可以为空)
    img_url = scrapy.Field()
    # 酒店链接(必须要有,直接跳转到对应商家的链接上去)
    hotel_link = scrapy.Field()
    # 所属景点(可以为空)
    scenic_id = scrapy.Field()
    # 供应商(可以为空,具体看爬取的是哪个网站)
    supplier_id = scrapy.Field()
    # 最近动态
    latest_time = scrapy.Field()
    # 人气
    sell_num = scrapy.Field()


class Ctrip_TicketItem(scrapy.Item):
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
