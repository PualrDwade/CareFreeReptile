# -*- coding: utf-8 -*-
import scrapy
from ..items import TicketItem


class TicketSpider(scrapy.Spider):
    name = 'TicketSpider'
    allowed_domains = ['ctrip.com']
    start_urls = ['http://piao.ctrip.com/dest/u-_ba_fe_c4_cf/s-tickets/P1/']
    count = 0

    def parse(self, response):
        next_url = None  # 首先声明全局变量
        trs = response.xpath(
            "//div[@id='searchResultContainer']//div[@class='searchresult_product04']")
        for tr in trs:
            self.count += 1
            # 这里id指定为湖南
            id = "CN00001_Ticket_" + str(self.count)
            name = tr.xpath(".//div[1]//h2/a/text()").get().strip()
            ticket_url = tr.xpath(".//div[1]/a/@href").get()
            ticket_url = 'http://piao.ctrip.com' + str(ticket_url)
            ticket_img = tr.xpath(".//div[1]/a/img/@src").get()
            address = tr.xpath(
                ".//div[1]/div[@class='adress']/text()").get().strip()
            city = tr.xpath(".//div[1]//h2/span/span/a/text()").get().strip()
            description = tr.xpath(
                ".//div[1]/div[@class='exercise']/text()").get().strip()
            grade = tr.xpath(
                ".//div[1]/div[@class='search_ticket_assess']/span[1]/em/text()").get().strip()
            grade = str(grade)
            price = tr.xpath(
                "normalize-space(.//table/tbody/tr[2]/td[4]/span[1])").get().strip()
            price = str(price)
            supplier = '00003'

            item = TicketItem(
                id=id,
                name=name,
                ticket_url=ticket_url,
                ticket_img=ticket_img,
                address=address,
                city=city,
                description=description,
                grade=grade,
                price=price,
                supplier=supplier)
            yield item
            next_url = response.xpath(
                '//*[@id="searchResultContainer"]/div[11]/a[11]/@href').get()

        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.parse, meta={})
