# -*- coding: utf-8 -*-
import scrapy
from JobSpider.items import JobspiderItem
import re

class PythonpositonSpider(scrapy.Spider):
    name = 'pythonPositon' # 爬虫名称
    allowed_domains = ['51job.com'] # 允许爬取的域

    def __init__(self):
        self.city = 10000
        self.max_city = 50000
        self.page = 1
        self.max_pages = 3
        self.str1 = 'https://search.51job.com/list/0'
        self.str2 = ',000000,0000,00,9,99,python,2,'
        self.str3 = '.html?lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='

    start_urls = ['https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']  # 爬虫爬取的起始地址

    def get_url(self):
        return self.str1 + str(self.city) + self.str2 + str(self.page) + self.str3

    def parse(self, response):
        self.log('qiku parse data...')
        #print(response.body)
        job_list = response.xpath("//div[@class='dw_table']/div[contains(@class,'el')]")
        print('len:', len(job_list))
        job_list.pop(0)
        print(len(job_list))
        if len(job_list)>0:
            for each in job_list:
                name = each.xpath("./p/span/a/text()").extract()[0].strip()
                self.log('name:'+name)
                corp = each.xpath("./span[@class='t2']/a/text()").extract()[0].strip()
                self.log("corp:"+corp)
                city = each.xpath("./span[@class='t3']/text()").extract()[0]
                self.log("city:" + city)
                salary = each.xpath("./span[@class='t4']/text()").extract()
                if len(salary)>0:
                    salary = salary[0].strip()
                else:
                    salary = '面议'
                self.log("salary:" + salary)
                pub_date = each.xpath("./span[@class='t5']/text()").extract()[0]
                self.log("pub_date:" + pub_date)
                    #city = each.xpath("").extract()[0]

                item = JobspiderItem()
                item['name'] = name
                item['corp'] = corp
                item['city'] = city
                item['salary'] = salary
                item['pub_date'] = pub_date
                print('cur url:', response.url)
                # 把提取的数据提交给pipeline
                yield item

        # 获取城市的编码
        p = self.str1 + r'(\d+)'
        curcity = re.search(p,response.url).group(1)
        # 获取页码数
        p = self.str1 + curcity + self.str2 +r'(\d+)'
        curpage = re.search(p,response.url).group(1)
        print('curcity:', curcity)
        print('curpage:', curpage)
        self.page = int(curpage) + 1
        if self.page <= self.max_pages:
            # 翻页
            print('new page:',self.page)
            url = self.get_url()
            print('new url:', url)
            # 发送新的请求，加入等待队列
            yield scrapy.Request(url,callback=self.parse)
        else:
            # 更换城市
            print('new city')
            self.city = int(curcity) + 10000
            if self.city <= self.max_city:
                self.page = 1
                url = self.get_url()
                print('new city:',self.city)
                yield scrapy.Request(url,callback=self.parse)



