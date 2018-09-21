# -*- coding: utf-8 -*-
import scrapy


# 酒店信息字段
class HotelMsgItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    score = scrapy.Field()
    hotel_price = scrapy.Field()
    hotel_content = scrapy.Field()
    img_url = scrapy.Field()
    hotel_link = scrapy.Field()
    city_name = scrapy.Field()
    supplier_id = scrapy.Field()
    latest_time = scrapy.Field()
    sell_num = scrapy.Field()


# 门票信息字段
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


# 攻略链接字段
class StrategyMsgItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    link_url = scrapy.Field()
    simple_content = scrapy.Field()
    img_url = scrapy.Field()
    supplier = scrapy.Field()
    scenic_name = scrapy.Field()


# 游记字段
class TraverNoteMsgItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    note_content = scrapy.Field()
    star_num = scrapy.Field()
    notify_status = scrapy.Field()
    add_time = scrapy.Field()
    img_url = scrapy.Field()
    user_id = scrapy.Field()
    city_id = scrapy.Field()
    

# 产品信息字段
class productItem(scrapy.Item):
    product_name = scrapy.Field()  # 产品名字
    id = scrapy.Field()  # 产品id
    schedule_days = scrapy.Field()  # 产品行程天数
    sr_team = scrapy.Field()  # 产品类型
    supplier = scrapy.Field()  # 产品供应商
    score_s = scrapy.Field()  # 评分
    comments_num = scrapy.Field()  # 评论数
    sales_volume = scrapy.Field()  # 销售量
    product_grade = scrapy.Field()  # 产品等级、钻级
    prd_url = scrapy.Field()  # 产品链接
    prd_img = scrapy.Field()  # 产品图片


# 产品景点信息模块
class product_scenic_Item(scrapy.Item):
    id = scrapy.Field()  # 自增id,自动生成
    product_id = scrapy.Field()  # 产品ID
    scenic_name = scrapy.Field()  # 景点名字


# 产品、出发城市、起价信息模块
class product_city_Item(scrapy.Item):
    id = scrapy.Field()  # 自增,自动生成
    product_id = scrapy.Field()  # 产品ID
    city_id = scrapy.Field()  # 出发城市名字
    product_price = scrapy.Field()  # 起价


# 省份信息模块
class ProvinceItem(scrapy.Item):
    province_id = scrapy.Field()
    province_name = scrapy.Field()
    province_img_url = scrapy.Field()


# 城市信息模块
class CityItem(scrapy.Item):
    city_id = scrapy.Field()
    city_name = scrapy.Field()
    provinceName = scrapy.Field()
    city_img_url = scrapy.Field()


# 景点信息模块
class ScenicItem(scrapy.Item):
    scenic_id = scrapy.Field()
    scenic_name = scrapy.Field()
    link_url = scrapy.Field()
    city_name = scrapy.Field()
    address = scrapy.Field()
    popular_level = scrapy.Field()
    scenic_img_url = scrapy.Field()
    basic_desc = scrapy.Field()
