# -*- coding: utf-8 -*-
import scrapy
import urllib
import os
import logging
from suumo.items import *
from scrapy.loader import ItemLoader
# Scrape every day, check the relistings

class RentSpider(scrapy.Spider):
    name = 'rent'
#    download_delay = 0.3
#    start_urls = ['http://suumo.jp/chintai/shikoku/','http://suumo.jp/chintai/kyushu/','http://suumo.jp/chintai/chugoku/','http://suumo.jp/chintai/kansai/','http://suumo.jp/chintai/tokai/','http://suumo.jp/chintai/kanto/','http://suumo.jp/chintai/koshinetsu/','http://suumo.jp/chintai/tohoku/','http://suumo.jp/chintai/hokkaido/']
#    start_urls = ['http://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&tc=0401303&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=12&pc=50']
    start_urls = ['http://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=030&bs=040&cb=0.0&ct=9999999&mb=0&mt=9999999&et=9999999&cn=9999999&tc=0401303&tc=0401304&shkr1=03&shkr2=03&shkr3=03&shkr4=03&sngz=&po1=09&pc=50']

    def parse(self, response):
#    	for href in response.xpath(u'//a[text()="新着物件を見る"]/@href'):
#    		yield response.follow(href, self.parse_properties)
#
#    def parse_properties(self, response):
        self.logger.info('parse_properties function called on %s', response.url)
        next_page = response.xpath(u'//p[contains(@class,"pagination-parts")][last()]/a/@href').extract_first()
    	for href in response.xpath(u'//a[text()="詳細を見る"]/@href').extract():
            yield scrapy.Request(href, callback=self.parse_details)

        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
   
    def parse_details(self, response):
        self.logger.info('  parse_details function called on %s', response.url)
    	itemrent = ItemLoader(item=Itemrent(), response=response)

    	itemrent.replace_xpath('rent',u"//span[contains(@class,\"detailvalue-item-accent\")]/text()")
        itemrent.replace_xpath('title_listing',u"//h1[contains(@class,\"section_title\")]/text()")
        itemrent.replace_xpath('deposit',u"//span[text()=\"敷\"]/../span[last()]/text()")
        itemrent.replace_xpath('key_money',u"//span[text()=\"礼\"]/../span[last()]/text()")
        itemrent.replace_xpath('room_layout',u"//td[contains(@class,\"detailinfo-col--03\")][1]//div[contains(@class,\"detailvalue-txt\")][1]/text()")
        itemrent.replace_xpath('m2',u"//td[contains(@class,\"detailinfo-col--03\")][1]//div[contains(@class,\"detailvalue-txt\")][2]/text()")
        itemrent.replace_xpath('direction_faced',u"//td[contains(@class,\"detailinfo-col--03\")][1]//div[contains(@class,\"detailvalue-txt\")][3]/text()")
        itemrent.replace_xpath('type_property',u"//td[contains(@class,\"detailinfo-col--03\")][2]//div[contains(@class,\"detailvalue-txt\")][1]/text()")
        itemrent.replace_xpath('age',u"//td[contains(@class,\"detailinfo-col--03\")][2]//div[contains(@class,\"detailvalue-txt\")][2]/text()")
        itemrent.replace_xpath('address',u"//td[contains(@class,\"detailinfo-col--04\")][1]//div[contains(@class,\"detailvalue-txt\")][1]/text()")
        itemrent.replace_xpath('sales_point_title',u"//div[contains(@class,\"cassettepoint-desc-title\")]/text()")
        itemrent.replace_xpath('agency',u"//span[contains(@class,\"itemcassette-header-ttl\")]/text()")
        itemrent.replace_xpath('agency_address',u"//div[contains(@class,\"itemcassette_matrix-cell01\")]/text()")
        itemrent.replace_xpath('agency_tel_nb',u"//span[contains(@class,\"itemcassette_matrix-strong\")]/text()")
        itemrent.add_xpath('subway_times',u"//div[contains(@class,\"detailnote-value-list\")]/text()")
        itemrent.replace_xpath('details_property',u"///div[contains(@class,\"bgc-wht\")]//li/text()")
        itemrent.replace_xpath('conditions',u"//th[text()='条件']/../td[1]/text()")
        itemrent.replace_xpath('floors',u"//th[text()='間取り詳細']/../td[1]/text()")
        itemrent.replace_xpath('floor_detail',u"//th[text()='階建']/../td[1]/text()")
        itemrent.replace_xpath('insurance_details',u"//th[text()='損保']/../td[1]/text()")
        itemrent.replace_xpath('moving_in_date',u"//th[text()='入居']/../td[1]/text()")
        itemrent.replace_xpath('suumo_code',u"//th[text()='物件コード']/../td[1]/text()")
        itemrent.replace_xpath('material',u"//th[text()='構造']/../td[2]/text()")
        itemrent.replace_xpath('handling_store_code',u"//th[contains(text(),'物件コード')]/../td[2]/text()")
        itemrent.replace_xpath('units_number',u"//th[contains(text(),'総戸数')]/../td[2]/text()")
        itemrent.replace_xpath('construction_date',u"//th[text()='築年月']/../td[2]/text()")
        itemrent.replace_xpath('parking',u"//th[text()='駐車場']/../td[2]/text()")
        itemrent.replace_xpath('transaction_type',u"//th[text()='取引態様']/../td[2]/text()")
        itemrent.replace_xpath('update_infos',u"//div[contains(text(),'情報更新日')]/text()")
        itemrent.replace_xpath('image_urls',u"//a[contains(@class,js-imageGallery-navi-panel)]/img/@data-src")
#       itemrent.replace_xpath('images',u"//a[contains(@class,js-imageGallery-navi-panel)]/img/@data-img").extract()
#        for image in itemrent.replace_xpath('images']:
#            urllib.urlretrieve(image,"images_apartments/"+image.split("/")[-1])
        

        itemrent.add_value('urldet',response.url)
        map_page = response.xpath(u'//a/img[@alt="周辺環境"]/../@href').extract_first()
        
        yield scrapy.Request(response.urljoin(map_page), callback=self.parse_map,meta={'itemrent':itemrent.load_item()})
        
    def parse_map(self, response):
        itemrent = ItemLoader(item=response.meta['itemrent'], response=response)
        itemrent.replace_xpath('lat',u"//form[@id='js-timesForm']/@action")
        itemrent.replace_xpath('lng',u"//form[@id='js-timesForm']/@action")
        itemrent.add_value('urlmap',response.url)
        yield itemrent.load_item()