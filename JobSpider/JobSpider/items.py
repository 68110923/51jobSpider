# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JobspiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()  # 职位名称
    corp = scrapy.Field()  # 招聘的公司
    city = scrapy.Field()  # city
    salary = scrapy.Field()   # 薪资
    pub_date = scrapy.Field()  # 发布的时间

