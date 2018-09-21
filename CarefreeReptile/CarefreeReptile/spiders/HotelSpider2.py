# coding=utf-8
# 爬取美团的酒店信息

# coding=utf-8
import scrapy
from ..items import HotelMsgItem

import pymysql
from .. import settings

import pypinyin

class HotelSpider2(scrapy.Spider):
    name = 'HotelSpider2'
    count = 0

    def getCitys(self):
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
        select_sql = 'SELECT name FROM TraverMsg_citymsg'
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        return result

    def start_requests(self):
        citys = self.getCitys()
        for city in citys:
            pingying_city = ""
            for c in pypinyin.pinyin(city, style=pypinyin.NORMAL)[0:2]:
                pingying_city = pingying_city + "".join(c)
            # 此时已经得到了城市的拼音名
            if pingying_city != '':
                city_url = 'http://hotel.meituan.com/' + pingying_city + '/'
                print (pingying_city)
                yield scrapy.Request(url=city_url, meta={'city': city}, callback=self.parse)

    def parse(self, response):
        hotelpages = response.xpath(
            '/html/body/main/section/div/div[1]/div[1]/div[2]/div[1]/article')
        for hotelpage in hotelpages:
            true_city_name = response.xpath('/html/body/main/section/section/div[1]/div/div/div[1]/label/input/@value').extract_first()
            if ((true_city_name + "市") != response.meta["city"][0]):
                break
            # 创建一个item用来存储数据
            hotelitem = HotelMsgItem()
            self.count += 1
            hotelitem['id'] = "CN00001_hotel_" + str(self.count)
            hotelitem['name'] = hotelpage.xpath(
                'div[2]/h3/a/text()').extract_first().strip()
            hotelitem['score'] = hotelpage.xpath(
                'div[2]/div/div[2]/div[1]/text()').extract_first().strip()
            hotelitem['hotel_price'] = hotelpage.xpath(
                'div[2]/div/div[3]/div[1]/em/text()').extract_first().strip()
            hotelitem['hotel_content'] = hotelpage.xpath(
                'div[2]/div/div[1]/div[1]/text()').extract_first().strip()
            hotelitem['img_url'] = hotelpage.xpath(
                'div[1]/a/img/@src').extract_first().strip()
            hotelitem['hotel_link'] = hotelpage.xpath(
                'div[2]/div/div[3]/a/@href').extract_first().strip()
            hotelitem['city_name'] = response.meta["city"]
            print ("城市名" + hotelitem['city_name'][0])
            hotelitem['supplier_id'] = '00001'  # 美团
            if hotelpage.xpath('div[2]/div/div[3]/div[2]/text()').extract_first() == None:
                hotelitem['latest_time'] = " "
            else:
                hotelitem['latest_time'] = hotelpage.xpath('div[2]/div/div[3]/div[2]/text()').extract_first()
            hotelitem['sell_num'] = hotelpage.xpath('div[2]/div/div[2]/div[2]/text()').extract_first().strip()
            # 存入数据库
            yield hotelitem
