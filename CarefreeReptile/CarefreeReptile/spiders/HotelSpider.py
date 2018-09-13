# coding=utf-8
import scrapy
from ..items import HotelMsgItem


class HotelSpider(scrapy.Spider):
    hotel_dict = {
        '长沙': 'http://hotels.ctrip.com/hotel/changsha206',
        '株洲': 'http://hotels.ctrip.com/hotel/zhuzhou601',
        '湘潭': 'http://hotels.ctrip.com/hotel/xiangtan598',
        '衡阳': 'http://hotels.ctrip.com/hotel/hengyang297',
        '韶山': 'http://hotels.ctrip.com/hotel/shaoshan446'
    }
    hotel_id_dict = {
        hotel_dict['长沙']: 'CN00001_1_Hotel_',
        hotel_dict['株洲']: 'CN00001_2_Hotel_',
        hotel_dict['湘潭']: 'CN00001_3_Hotel_',
        hotel_dict['衡阳']: 'CN00001_4_Hotel_',
        hotel_dict['韶山']: 'CN00001_5_Hotel_'

    }
    name = 'HotelSpider'
    count = 0
    base_url = 'http://hotels.ctrip.com'

    # 设置爬取的开始链接

    def start_requests(self):
        urls = [item for item in self.hotel_dict.values()]
        for url in urls:
            # 创建内容传入parse函数
            meta = {
                'hotel_id': self.hotel_id_dict[url]
            }
            # 提交给parse处理
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)

    def parse(self, response):
        hotelpages = response.css('.hotel_new_list.J_HotelListBaseCell')
        for hotelpage in hotelpages:
            # 创建一个item用来存储数据
            hotelitem = HotelMsgItem()
            self.count += 1
            hotelitem['id'] = response.meta['hotel_id'] + str(self.count)
            hotelitem['name'] = hotelpage.xpath(
                'ul/li[2]/h2/a/text()').extract_first().strip()
            hotelitem['score'] = hotelpage.xpath(
                'ul/li[4]/div[1]/a/span[2]/text()').extract_first().strip()
            hotelitem['hotel_price'] = hotelpage.xpath(
                'ul/li[3]/div[1]/div/div/a/span/text()').extract_first().strip()
            hotelitem['hotel_content'] = hotelpage.xpath(
                'ul/li[2]/p[1]/text()').extract()[-1][1:].strip()
            hotelitem['img_url'] = hotelpage.xpath(
                'ul/li[1]/div/a/div/img/@src').extract_first().strip()
            hotelitem['hotel_link'] = self.base_url + \
                hotelpage.xpath('ul/li[2]/h2/a/@href').extract_first().strip()
            hotelitem['scenic_id'] = hotelpage.xpath(
                'ul/li[2]/p[1]/a[1]/text()').extract_first().strip()
            hotelitem['supplier_id'] = '00003'  # 携程
            hotelitem['latest_time'] = hotelpage.xpath(
                'ul/li[2]/p[3]/text()').extract_first()
            hotelitem['sell_num'] = hotelpage.xpath(
                'ul/li[4]/div[1]/a/span/span/text()').extract_first().strip()
            # 存入数据库
            yield hotelitem
