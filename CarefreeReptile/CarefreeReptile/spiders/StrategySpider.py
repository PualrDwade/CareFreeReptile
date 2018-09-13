# coding=utf-8
import scrapy
from ..items import StrategyMsgItem


class StrategySpider(scrapy.Spider):
    stratege_dict = {
        '长沙': 'http://travel.qunar.com/search/gonglue/22-changsha-300022'}
    stratege_id_dict = {
        stratege_dict['长沙']: 'CN00001_1_Strategy_'
    }
    name = 'StrategySpider'
    count = 0

    # 设置爬取的开始链接

    def start_requests(self):
        urls = [item for item in self.stratege_dict.values()]
        for url in urls:
            # 创建内容传入parse函数
            meta = {
                'strategy_id': self.stratege_id_dict[url]
            }
            yield scrapy.Request(url=url, callback=self.parse, meta=meta)  # 提交给parse处理

    def parse(self, response):
        hotelpages = response.xpath('/html/body/div[2]/div/div[4]/ul/li')
        for hotelpage in hotelpages:
            # 创建一个item用来存储数据
            hotelitem = StrategyMsgItem()
            self.count += 1
            hotelitem['id'] = response.meta['strategy_id'] + str(self.count)
            hotelitem['title'] = hotelpage.xpath('h2/a/text()').extract_first().strip()
            hotelitem['link_url'] = hotelpage.xpath('h2/a/@href').extract_first().strip()
            hotelitem['simple_content'] = ''.join(hotelpage.xpath('p[2]/text()').extract())
            hotelitem['simple_content'] += ''.join(hotelpage.xpath('p[3]/text()').extract())
            hotelitem['img_url'] = hotelpage.xpath('a[2]/img/@src').extract_first()
            hotelitem['supplier'] = '00004'#去哪儿
            hotelitem['scenic_name'] = hotelpage.xpath('div[2]/div/div[3]/a/@href').extract_first().strip()
            # 存入数据库
            yield hotelitem
