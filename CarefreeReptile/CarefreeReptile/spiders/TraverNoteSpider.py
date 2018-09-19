# coding=utf-8
import scrapy
from ..items import TraverNoteMsgItem

import pymysql
from .. import settings

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

class TraverNoteSpider(scrapy.Spider):
    traverNoteCitys_dict = ['shanghai2', 'hangzhou14', 'suzhou11', 'nanjing9', 'xiamen21', 'sanya61', 'beijing1', 'changsha148', 'chengdu104', 'lijiang32', 'hangkong38', 'dali31']
    city_name = ['上海市', '杭州市', '苏州市', '南京市', '厦门市', '三亚市', '北京市', '长沙市', '成都市', '丽江市', '香港市', '大理市']
    
    name = 'TraverNoteSpider'
    count = 0
    base_url = 'http://you.ctrip.com/travels/'

    def getCitysId(self, city_name):
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
        select_sql = 'SELECT ID FROM TraverMsg_citymsg where name = \'' + city_name + '\''
        print (select_sql)
        self.cursor.execute(select_sql)
        result = self.cursor.fetchall()
        return result

    def start_requests(self):
        i = 0
        for traverNoteCitys in self.traverNoteCitys_dict:
            city_id = self.getCitysId(self.city_name[i])
            yield scrapy.Request(url=self.base_url+traverNoteCitys+'.html', meta={'city_id': city_id}, callback=self.parse)
            i += 1

    def parse(self, response):
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(executable_path='geckodriver', firefox_options=options)
        wait = WebDriverWait(driver, timeout=4)



        item = TraverNoteMsgItem()
        traverNote_pages = response.xpath('//a[@class="journal-item cf"]')
        for traverNote_page in traverNote_pages:
            item['id'] = "CN_traverNote_" + str(self.count)
            self.count += 1
            item['title'] = traverNote_page.xpath('div/dl/dt/text()').extract_first().strip()
            item['note_content'] = traverNote_page.xpath('div/dl/dd[2]/text()').extract_first().strip()
            item['star_num'] = traverNote_page.xpath('div/ul/li[2]/i/text()').extract_first().strip()
            item['notify_status'] = '2'
            item['add_time'] = traverNote_page.xpath('div/dl/dd[1]/text()').extract_first().strip()[-10:]
            # item['img_url'] = traverNote_page.xpath('div/span/img/@src').extract_first().strip()
            item['img_url'] = 'http://software.csu.edu.cn/'
            item['user_id'] = '544493924@qq.com'
            item['city_id'] = response.meta['city_id'][0][0]

            # 存入数据库
            yield item
