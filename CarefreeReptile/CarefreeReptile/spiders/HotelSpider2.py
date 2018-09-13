# coding=utf-8
# 爬取美团的酒店信息

# coding=utf-8
import scrapy
from ..items import HotelMsgItem


class HotelSpider2(scrapy.Spider):
    hotel_dict = {
        '长沙': 'http://hotel.meituan.com/changsha/',
        '株洲': 'http://hotel.meituan.com/zhuzhou/',
        '湘潭': 'http://hotel.meituan.com/xiangtan/',
        '衡阳': 'http://hotel.meituan.com/hengyang/',
        '韶山': 'http://hotel.meituan.com/shaoshan/'
    }
    hotel_id_dict = {
        hotel_dict['长沙']: 'CN00001_1_Hotel2_',
        hotel_dict['株洲']: 'CN00001_2_Hotel2_',
        hotel_dict['湘潭']: 'CN00001_3_Hotel2_',
        hotel_dict['衡阳']: 'CN00001_4_Hotel2_',
        hotel_dict['韶山']: 'CN00001_5_Hotel2_'

    }
    name = 'HotelSpider2'
    count = 0

    # 设置爬取的开始链接

    def start_requests(self):
        urls = [item for item in self.hotel_dict.values()]
        for url in urls:
            # 创建内容传入parse函数
            meta = {
                'hotel_id': self.hotel_id_dict[url]
            }
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)  # 提交给parse处理

    def parse(self, response):
        hotelpages = response.xpath('/html/body/main/section/div/div[1]/div[1]/div[2]/div[1]/article')
        for hotelpage in hotelpages:
            # 创建一个item用来存储数据
            hotelitem = HotelMsgItem()
            self.count += 1
            hotelitem['id'] = response.meta['hotel_id'] + str(self.count)
            hotelitem['name'] = hotelpage.xpath('div[2]/h3/a/text()').extract_first().strip()
            hotelitem['score'] = hotelpage.xpath('div[2]/div/div[2]/div[1]/text()').extract_first().strip()
            hotelitem['hotel_price'] = hotelpage.xpath('div[2]/div/div[3]/div[1]/em/text()').extract_first().strip()
            hotelitem['hotel_content'] = hotelpage.xpath('div[2]/div/div[1]/div[1]/text()').extract_first().strip()
            hotelitem['img_url'] = hotelpage.xpath('div[1]/a/img/@src').extract_first().strip()
            hotelitem['hotel_link'] = hotelpage.xpath('div[2]/div/div[3]/a/@href').extract_first().strip()
            hotelitem['scenic_id'] = hotelpage.xpath('div[2]/div/div[1]/div[1]/span/text()').extract_first()
            hotelitem['supplier_id'] = '00001'  # 美团
            hotelitem['latest_time'] = hotelpage.xpath('div[2]/div/div[3]/div[2]/text()').extract_first()
            hotelitem['sell_num'] = hotelpage.xpath('div[2]/div/div[2]/div[2]/text()').extract_first().strip()
            # 存入数据库
            yield hotelitem
