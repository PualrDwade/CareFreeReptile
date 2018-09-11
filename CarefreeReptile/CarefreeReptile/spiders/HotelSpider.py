# coding=utf-8
import scrapy
from ..items import Ctrip_HotelMsgItem


class HotelSpider(scrapy.Spider):
    hotel_dict = {
        '长沙': 'http://hotels.ctrip.com/hotel/changsha206'
    }
    name = 'HotelSpider'
    count = 0
    base_url = 'http://hotels.ctrip.com'

    # 设置爬取的开始链接

    def start_requests(self):
        urls = [self.hotel_dict['长沙']]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)  # 提交给parse处理

    def parse(self, response):
        hotelpages = response.css('.hotel_new_list.J_HotelListBaseCell')
        for hotelpage in hotelpages:
            # 创建一个item用来存储数据
            hotelitem = Ctrip_HotelMsgItem()
            self.count += 1
            hotelitem['id'] = 'CN00001_1_Hotel' + str(self.count)
            hotelitem['name'] = hotelpage.xpath('ul/li[2]/h2/a/text()').extract_first().strip()
            hotelitem['score'] = hotelpage.xpath('ul/li[4]/div[1]/a/span[2]/text()').extract_first().strip()
            hotelitem['hotel_price'] = hotelpage.xpath('ul/li[3]/div[1]/div/div/a/span/text()').extract_first().strip()
            hotelitem['hotel_content'] = hotelpage.xpath('ul/li[2]/p[1]/text()').extract()[-1][1:].strip()
            hotelitem['img_url'] = hotelpage.xpath('ul/li[1]/div/a/div/img/@src').extract_first().strip()
            hotelitem['hotel_link'] = self.base_url + hotelpage.xpath('ul/li[2]/h2/a/@href').extract_first().strip()
            hotelitem['scenic_id'] = hotelpage.xpath('ul/li[2]/p[1]/a[1]/text()').extract_first().strip()
            hotelitem['supplier_id'] = '00003'  # 携程
            hotelitem['latest_time'] = hotelpage.xpath('ul/li[2]/p[3]/text()').extract_first().strip()
            hotelitem['sell_num'] = hotelpage.xpath('ul/li[4]/div[1]/a/span/span/text()').extract_first().strip()
            # 存入数据库
            yield hotelitem

        # 判断是否还有下一页
        next_url = hotelpage.xpath('//*[@id="downHerf"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(url=response.urljoin(next_url.strip()), callback=self.parse)
