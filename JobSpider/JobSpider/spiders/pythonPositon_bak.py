# -*- coding: utf-8 -*-
import scrapy
from JobSpider.items import JobspiderItem

class PythonpositonSpider(scrapy.Spider):
    name = 'pythonPositon_bak' # 爬虫名称
    allowed_domains = ['51job.com'] # 允许爬取的域


    start_urls = ['https://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']  # 爬虫爬取的起始地址

    def parse(self, response):
        self.log('qiku parse data...')
        print(response.body)
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

                # 把提取的数据提交给pipeline
                yield item
