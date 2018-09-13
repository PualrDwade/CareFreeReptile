# coding=utf-8
import re

import scrapy
from ..items import productItem
from ..items import product_scenic_Item
from ..items import product_city_Item


class ProductSpider(scrapy.Spider):
    name = 'ProductSpider'
    # 各城市的产品页面链接
    product_dict = {
        '韶山': 'http://vacations.ctrip.com/grouptravel-1B64/?searchValue=%e9%9f%b6%e5%b1%b1&searchText=%e9%9f%b6%e5%b1'
              '%b1&from=do',
        '三亚': 'http://vacations.ctrip.com/tours/d-sanya-61/grouptravel?from=do'
    }
    list_urls = {}

    id_dict = {
        '长沙': 'CN01_1Prd03'
    }
    # 用来生成id
    count = 0

    def start_requests(self):
        urls = [self.product_dict['三亚']]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # 爬携程
    def parse(self, response):

        urls = response.xpath('//h2[@class="product_title"]/a/@href').extract()
        url_num = 0
        for url in urls:
            self.list_urls[str(url_num)] = "http:" + url
            yield scrapy.Request("http:" + url, meta={'num': str(url_num)}, callback=self.product_parse)
            url_num += 1

    # 爬携程
    def product_parse(self, response):
        item = productItem()  # 创建一个item
        item1 = product_scenic_Item()
        item2 = product_city_Item()

        item['prd_url'] = self.list_urls[response.meta['num']]
        item['prd_img'] = ("http:" + response.xpath(
            '/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/div[3]/div/div[1]'
            '/a/div/div/div[2]/img/@src').extract_first()).strip()
        # 产品名称
        item['product_name'] = response.xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/h1/text()').extract()
        # 产品的标识号
        if len(response.xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/text()')) > 1:
            prd_num = \
                response.xpath('/html/body/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[2]/text()').extract()[1]
        else:
            prd_num = "none"
        item['id'] = self.id_dict["长沙"] + prd_num

        # product_name不是string类型，是list类型
        item['schedule_days'] = re.findall("\\d+", item['product_name'][0])[0]

        # 产品类型
        item['sr_team'] = re.findall("晚....", item['product_name'][0])[0][1:-1]  # [1:-1]是对去除晚和(

        # 这里有反爬虫机制
        item['score_s'] = '5'
        # ''.join(response.xpath(
        # '/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/span[1]/em/text()').extract())

        item['comments_num'] = '100'
        # ''.join(response.xpath(
        #     '/html/body/div[2]/div/div/div[1]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div/div/span[2]').re(r'\\d+'))

        # 出售量
        if len(response.xpath('//span[@data-reactid="30"]/text()').extract()) > 0:
            item['sales_volume'] = response.xpath('//span[@data-reactid="30"]/text()').extract()[0]
        else:
            item['sales_volume'] = response.xpath('//span[@data-reactid="30"]/text()').extract()
        # 供应商
        item['supplier'] = '00003'  # 携程供应商
        # 产品钻级
        if len(response.xpath('//h1/span/@class')) > 0:
            item['product_grade'] = response.xpath('//h1/span/@class').extract()[0][-1]
        else:
            item['product_grade'] = "0"
        print('插入item进入数据库')
        print(item)
        yield item
        #######################################################################################
        # 产品景点
        item1['id'] = self.count
        self.count += 1
        item1['product_id'] = item['id']
        item1['scenic_name'] = "韶山"
        print('插入item1进入数据库')
        yield item1

        #######################################################################################
        # 产品、出发城市、起价
        if len(response.xpath('//div[@class="from_city"]/text()').extract()) > 1:
            the_city = response.xpath('//div[@class="from_city"]/text()').extract()[1]  # 当前页面出发城市
        else:
            the_city = response.xpath('//div[@class="prd_num"]/text()').extract()[1]
        if len(response.xpath('//span[@class="total_price"]/em/text()').extract()) > 0:
            the_price = response.xpath('//span[@class="total_price"]/em/text()').extract()[0]  # 当前页面出发城市起价
        else:
            the_price = response.xpath('//span[@class="total_price"]/em/text()').extract()
        item2['id'] = self.count
        self.count += 1
        item2['product_id'] = item['id']
        item2['city_id'] = the_city
        item2['product_price'] = the_price
        print('插入item2到数据库')
        yield item2

        from_city = response.xpath('//div[@class="city_price"]').re(r'<em>.*?</em>.*?</div>')
        for city in from_city:
            res_city_pattern = r'<em>(.*?)</em>'
            res_price_pattern = r'</dfn>(.*?)</div>'
            from_city_name = re.findall(res_city_pattern, city, re.S | re.M)[0]
            if len(re.findall(res_price_pattern, city, re.S | re.M)) != 0:
                price = re.findall(res_price_pattern, city, re.S | re.M)[0]
            else:
                price = "实时计价"
            item2['id'] = self.count
            self.count += 1
            item2['product_id'] = item['id']
            item2['city_id'] = from_city_name
            item2['product_price'] = price
            item2
            print('插入item2到数据库')
            yield item2

        print("-----------------------------------------------------------------------")
