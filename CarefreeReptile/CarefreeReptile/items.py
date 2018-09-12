# -*- coding: utf-8 -*-
import scrapy


# 携程的酒店信息字段
class HotelMsgItem(scrapy.Item):
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


# 携程的产品信息字段
class Ctrip_productItem(scrapy.Item):
    product_name = scrapy.Field()  # 产品名字
    id = scrapy.Field()  # 产品id
    schedule_days = scrapy.Field()  # 产品行程天数
    sr_team = scrapy.Field()  # 产品类型
    supplier = scrapy.Field()  # 产品供应商
    score_s = scrapy.Field()  # 评分
    comments_num = scrapy.Field()  # 评论数
    sales_volume = scrapy.Field()  # 销售量
    product_grade = scrapy.Field()  # 产品等级、钻级
    departs_citys = scrapy.Field()  # 出发城市
    price = scrapy.Field()  # 各个出发城市起价
    prd_url = scrapy.Field()  # 产品链接
    prd_img = scrapy.Field()  # 产品图片
    prd_scenic = scrapy.Field()  # 产品景点
