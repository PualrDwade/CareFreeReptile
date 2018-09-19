# coding=utf-8
import re

import scrapy

from ..items import productItem
from ..items import product_scenic_Item
from ..items import product_city_Item

import time
import random

import pymysql
from .. import settings

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

class ProductSpider(scrapy.Spider):
    name = 'ProductSpider'
    # 各城市的产品页面链接
    product_dict = {
        '韶山': 'http://vacations.ctrip.com/grouptravel-1B64/?searchValue=%e9%9f%b6%e5%b1%b1&searchText=%e9%9f%b6%e5%b1'
              '%b1&from=do',
        '三亚': 'http://vacations.ctrip.com/tours/d-sanya-61/grouptravel?from=do'
    }

    id_dict = {
        '长沙': 'CN01_1Prd03'
    }
    # 用来生成id
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
        # citys = ["长沙", "上海", "北京", "天津", "南京", "内蒙古", "广州", "厦门", "韶山", "南昌"]
        citys = self.getCitys()

        for city in citys:
            if city[0] != '':
                city_url = 'http://vacations.ctrip.com/grouptravel-206B64/?searchValue=' + city[0] + '&searchText=' + city[0] + '&from=do'
                yield scrapy.Request(url=city_url, callback=self.parse)
                break

    # 爬携程
    def parse(self, response):

        urls = response.xpath('//h2[@class="product_title"]/a/@href').extract()
        for url in urls:
            yield scrapy.Request("http:" + url, meta={'url': "http:" + url}, callback=self.product_parse)

    # 爬携程
    def product_parse(self, response):
        # 使用selenium爬取动态页面
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='geckodriver', firefox_options=options)
        wait = WebDriverWait(driver, timeout=10)
        item['score_s'] = driver.find_element_by_class_name('score_s').text[0:-1]
        item['comments_num'] = driver.find_element_by_class_name('score_dp').text[0:-3]
        driver.quit()


        item = productItem()  # 创建一个item
        item1 = product_scenic_Item()
        item2 = product_city_Item()

        item['prd_url'] = response.meta['url']
        temp = response.xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/div[3]/div/div[1]/a/div/div/div[2]/img/@src').extract_first()
        if temp == None:
            item['prd_img'] = "none"
        else:
            item['prd_img'] = "http:" + temp
        # 产品名称
        item['product_name'] = response.xpath(
            '/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/h1/text()').extract()
        # 产品的标识号
        if len(response.xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/text()')) > 1:
            prd_num = \
                response.xpath(
                    '/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/text()').extract()[1]
        else:
            prd_num = "none"
        item['id'] = self.id_dict["长沙"] + prd_num

        # product_name不是string类型，是list类型
        item['schedule_days'] = re.findall("\\d+", item['product_name'][0])[0]

        # 产品类型
        # [1:-1]是对去除晚和(
        try:
            item['sr_team'] = re.findall("晚....", item['product_name'][0])[0][1:-1]
        except IndexError:
            item['sr_team'] = re.findall("晚....", item['product_name'][0])

        # 出售量
        if len(response.xpath('//span[@data-reactid="30"]/text()').extract()) > 0:
            item['sales_volume'] = response.xpath(
                '//span[@data-reactid="30"]/text()').extract()[0]
        else:
            item['sales_volume'] = response.xpath(
                '//span[@data-reactid="30"]/text()').extract()
        # 供应商
        item['supplier'] = '00003'  # 携程供应商
        # 产品钻级
        if len(response.xpath('//h1/span/@class')) > 0:
            item['product_grade'] = response.xpath(
                '//h1/span/@class').extract()[0][-1]
        else:
            item['product_grade'] = "0"

        print('插入item进入数据库')
        yield item

        #######################################################################################
        # 产品景点
        item1['id'] = self.count
        self.count += 1
        item1['product_id'] = item['id']
        item1['scenic_name'] = "韶山"
        print('插入item1进入数据库')
        # yield item1

        #######################################################################################
        # 产品、出发城市、起价
        if len(response.xpath('//div[@class="from_city"]/text()').extract()) > 1:
            the_city = response.xpath(
                '//div[@class="from_city"]/text()').extract()[1]  # 当前页面出发城市
        else:
            the_city = response.xpath(
                '//div[@class="prd_num"]/text()').extract()[1]
        if len(response.xpath('//span[@class="total_price"]/em/text()').extract()) > 0:
            the_price = response.xpath(
                '//span[@class="total_price"]/em/text()').extract()[0]  # 当前页面出发城市起价
        else:
            the_price = response.xpath(
                '//span[@class="total_price"]/em/text()').extract()
        item2['id'] = self.count
        self.count += 1
        item2['product_id'] = item['id']
        item2['city_id'] = the_city
        item2['product_price'] = the_price
        # print('插入item2到数据库')
        # yield item2

        from_city = response.xpath(
            '//div[@class="city_price"]').re(r'<em>.*?</em>.*?</div>')
        count = 0
        for city in from_city:
            res_city_pattern = r'<em>(.*?)</em>'
            res_price_pattern = r'</dfn>(.*?)</div>'
            from_city_name = re.findall(res_city_pattern, city, re.S | re.M)[0]
            print (from_city_name)
            if len(re.findall(res_price_pattern, city, re.S | re.M)) != 0:
                price = re.findall(res_price_pattern, city, re.S | re.M)[0]
            else:
                price = "实时计价"
            item2['id'] = self.count
            self.count += 1
            item2['product_id'] = item['id']
            item2['city_id'] = from_city_name
            item2['product_price'] = price
            break
            # print('插入item2到数据库')
            # yield item2
            count += 1
            if count > 5:
                break

        print("-----------------------------------------------------------------------")
