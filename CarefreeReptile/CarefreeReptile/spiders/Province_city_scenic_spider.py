# coding=utf-8
import re
import scrapy
from cpca import * # 用于提取中文地址描述中的省市区信息

from ..items import ProvinceItem
from ..items import ScenicItem
from ..items import CityItem

class Province_city_scenic_spider(scrapy.Spider):
    name = "province_city_scenic_spider"
    scenic_count = 0
    city_count = 0
    province_count = 0

    def start_requests(self):
        pages = list(range(1,3))
        for page in pages:
            page_url = 'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest&page=' + str(page)
            yield scrapy.Request(url=page_url, callback=self.parse)


    def parse(self, response):
        item1 = ScenicItem()
        item2 = CityItem()
        item3 = ProvinceItem()

        scenic_num_list = list(range(1,16))
        for scenic_num in scenic_num_list:
            item1["id"] = ''.join(['CN_scenic' + str(self.scenic_count)])
            self.scenic_count += 1
            item1["name"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/h3/a/text()').extract_first()
            item1["link_url"] = 'http://piao.qunar.com' + response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/h3/a/@href').extract_first()
            
            item1["address"]  = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/p/span/text()').extract()[0][3:]
            # 城市名称从地址中截取出来
            item1["city_name"] = transform([item1["address"]])['市'][0]

            item2["id"] = ''.join(['CN_city' + str(self.city_count)])
            self.city_count += 1
            item2["name"] = transform([item1["address"]])['市'][0]
            item2["provinceName"] = transform([item1["address"]])['省'][0]
            item2["img_url"] = "city_img_url"

            # 省份名称从地址中截取出来
            item3["id"] = ''.join(['CN_province' + str(self.province_count)])
            self.province_count += 1
            item3["name"] = transform([item1["address"]])['省'][0]
            item3["img_url"] = 'http://piao.qunar.com'
            
            # 要乘以5才是五星级评判标准
            item1["popular_level"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/div[1]/div/span[1]/em/span/text()').extract()[0][3:]
            item1["img_url"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[1]/div/a/img/@data-original').extract_first()
            item1["basic_desc"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/div[2]/text()').extract_first()
            
            yield item1
            yield item2
            yield item3