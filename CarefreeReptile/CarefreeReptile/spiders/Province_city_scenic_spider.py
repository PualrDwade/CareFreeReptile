# coding=utf-8
import re
import scrapy
from cpca import * # 用于提取中文地址描述中的省市区信息

from ..items import ProvinceItem
from ..items import ScenicItem
from ..items import CityItem
from ..items import TicketItem

class Province_city_scenic_spider(scrapy.Spider):
    name = "province_city_scenic_spider"
    scenic_count = 0
    city_count = 0
    province_count = 0
    ticket_count = 0

    def start_requests(self):
        pages = list(range(1,2000))
        for page in pages:
            page_url = 'http://piao.qunar.com/ticket/list.htm?keyword=%E7%83%AD%E9%97%A8%E6%99%AF%E7%82%B9&region=&from=mpl_search_suggest&page=' + str(page)
            yield scrapy.Request(url=page_url, callback=self.parse)


    def parse(self, response):
        item1 = ScenicItem()
        item2 = CityItem()
        item3 = ProvinceItem()
        item4 = TicketItem()

        scenic_num_list = list(range(1,16))
        for scenic_num in scenic_num_list:
            item1["scenic_id"] = ''.join(['CN_scenic' + str(self.scenic_count)])
            self.scenic_count += 1
            item1["scenic_name"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/h3/a/text()').extract_first()
            item1["link_url"] = 'http://piao.qunar.com' + response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/h3/a/@href').extract_first()
            
            item1["address"]  = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/p/span/text()').extract()[0][3:]
            # 城市名称从地址中截取出来
            item1["city_name"] = transform([item1["address"]])['市'][0]

            item2["city_id"] = ''.join(['CN_city' + str(self.city_count)])
            self.city_count += 1
            item2["city_name"] = transform([item1["address"]])['市'][0]
            item2["provinceName"] = transform([item1["address"]])['省'][0]
            item2["city_img_url"] = "city_img_url"

            # 省份名称从地址中截取出来
            item3["province_id"] = ''.join(['CN_province' + str(self.province_count)])
            self.province_count += 1
            item3["province_name"] = transform([item1["address"]])['省'][0]
            item3["province_img_url"] = 'http://piao.qunar.com'
            
            # 要乘以5才是五星级评判标准
            item1["popular_level"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/div[1]/div/span[1]/em/span/text()').extract()[0][3:]
            item1["scenic_img_url"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[1]/div/a/img/@data-original').extract_first()
            item1["basic_desc"] = response.xpath('/html/body/div[2]/div[2]/div[1]/div[4]/div[1]/div['+str(scenic_num)+']/div/div[2]/div/div[2]/text()').extract_first()
            
            item4["id"] = ''.join(['CN_ticket' + str(self.ticket_count)])
            self.ticket_count += 1
            item4["name"] = item1["scenic_name"]
            item4["ticket_url"] = 'http://piao.qunar.com' + response.xpath('//a[@class="sight_item_do"]/@href').extract_first()
            item4["ticket_img"] = item1["scenic_img_url"]
            item4["address"] = item1["address"]
            item4["city"] = item2["city_name"]
            item4['description'] = item1["basic_desc"]
            item4['grade'] = item1["popular_level"]
            item4['price'] = response.xpath('//span[@class="sight_item_price"]/em/text()').extract_first()
            item4['supplier'] = "00004"

            yield item4
            # yield item3
            # yield item2
            # yield item1