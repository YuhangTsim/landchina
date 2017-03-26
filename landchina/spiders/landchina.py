# encoding:utf-8

import datetime
import time
import random
import re
from datetime import datetime, timedelta
import scrapy
from scrapy import Request, FormRequest
from scrapy.selector import Selector
from selenium import webdriver

from landchina.items import DealItem
from landchina.spiders.post_header import post_data, date_data, next_period, makepost, cate, returnItem
from landchina.start import start_date, end_date, delta

class Spider(scrapy.Spider):

    name = 'landchina'

    host = 'http://www.landchina.com'
    allowed_domain = ['landchian.com']
    start_urls = ['http://www.landchina.com/default.aspx?tabid=263']

    start_time = start_date
    end_time = start_date + delta
    end = end_date

    def start_requests(self):
        print('------ Post Data Gotten ------')
        start_time = self.start_time
        end_time = self.end_time
        baseurl = self.start_urls[0]
        while (self.end-end_time).days >= 0:
            if (start_time - end_time).days>0:
                print('------ Crawling End ------')
                break
            post = post_data
            print(start_time)
            period = makepost(start_time, end_time)
            start_time, end_time = next_period(start_time, end_time)
            post_filter = date_data + period +cate
            post['TAB_QuerySubmitConditionData'] = post_filter
            page = 1
            num_page = 1
            deals = []
            print('------ 爬取 %s -----' % period[:-1])
            yield FormRequest(baseurl, formdata = post,
                meta = {'post_date':period, 'baseurl':baseurl, 'page':page,'num_page':num_page, 'period':period, 'deals': deals}, callback = self.parse0, dont_filter = True)



    def parse0(self, response):
        ''' 进入当前日期页面'''
        selector = Selector(response)
        baseurl = self.host + '/'
        post = post_data
        period = response.meta['post_date']
        post_filter = date_data + period +cate
        post['TAB_QuerySubmitConditionData'] = post_filter
        page = response.meta['page']
        deals = response.meta['deals']
        post['TAB_QuerySubmitPagerData'] = str(page)
        if page == 1:
            try:
                num_page = selector.xpath('//td[@class="pager"]/text()').extract()
                num_page = int(re.findall('[0-9]+',num_page[0])[0])
                period = response.meta['period']
                print('------ There are %s pages in %s ------' % (num_page,period[:-1]))
            except Exception:
                print('------ Error Miss %s ------' % period[:-1])
                num_page = response.meta['num_page']
                yield FormRequest(baseurl, formdata = post,
                    meta = {'post_date':period, 'baseurl':baseurl, 'page':page,'num_page':num_page, 'period':period, 'deals': deals}, callback = self.parse0, dont_filter = True)

        else:
            num_page = response.meta['num_page']
        page += 1

        urls = selector.xpath('//tr[@onmouseout="this.className=rowClass"]//@href').extract()
        deals += urls
        for u in deals:
            url = baseurl+u
            yield Request(url=url, callback = self.parse1)

        if page-1 <= num_page:
            try:
                info = str(page-1)+'/'+str(num_page)
                print('------ There are %d deals in page %s-  in %s-----' % (len(urls),info,period[:-1]))
                print('------ Crawling Page No.%s ------' % info )
                yield FormRequest(self.start_urls[0], formdata = post,
                    meta = {'post_date':period, 'num_page':num_page, 'page':page,'deals': deals}, callback = self.parse0,dont_filter = True)
            except Exception as e:
                print(e)
        else:
            print('------ Crawling End ------')


    def parse1(self, response):
        ''' 爬取交易细节'''
        selector = Selector(response)
        DealItems = DealItem()
        Dist = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c2_ctrl"]/text()').extract()
        DealItems['Dist'] = returnItem(Dist)
        DealItems['E_ID'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r1_c4_ctrl"]/text()')[0].extract()
        DealItems['Project_Name'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r17_c2_ctrl"]/text()')[0].extract()
        DealItems['Project_where'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r16_c2_ctrl"]/text()')[0].extract()
        Area = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c2_ctrl"]/text()').extract()
        DealItems['Area'] = returnItem(Area)
        Source = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r2_c4_ctrl"]/text()').extract()
        Source = returnItem(Source)
        if Area == Source:
            DealItems['Source'] = "现有建设用地"
        elif Source == '0.000000':
            DealItems['Source'] = "新增建设用地"
        else:
            DealItems['Source'] = "新增建设用地(来自存量库)"
        DealItems['Usage'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c2_ctrl"]/text()')[0].extract()
        DealItems['Provide_Method'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r3_c4_ctrl"]/text()')[0].extract()
        expiry_date = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c2_ctrl"]/text()').extract()
        DealItems['expiry_date'] = returnItem(expiry_date)
        DealItems['category'] =selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r19_c4_ctrl"]/text()')[0].extract()
        DealItems['rank'] = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c2_ctrl"]/text()')[0].extract()
        price = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r20_c4_ctrl"]/text()').extract()
        DealItems['price'] = returnItem(price)
        table_len = len(selector.xpath('//table[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3"]/tbody/tr').extract())-3
        ZFYD = []
        for i in range(table_len):
            YD = {}
            ZFQH = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c1_%d_ctrl"]/text()' % i).extract()
            YDZFRQ = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c2_%d_ctrl"]/text()' % i).extract()
            YDZFJE = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c3_%d_ctrl"]/text()'% i).extract()
            BZ = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f3_r2_c4_%d_ctrl"]/text()'% i).extract()
            if ZFQH and YDZFRQ and YDZFJE:
                YD['支付期号'] = ZFQH[0]
                YD['约定支付日期'] = YDZFRQ[0]
                YD['约定支付金额'] = YDZFJE[0]
                if BZ:
                    YD['备注'] = BZ[0]
                else:
                    YD['备注'] = 'Nah'
            else:
                YD = 'Nah'
            ZFYD.append(YD)
        # DealItems['payment'] = ZFYD
        use_right_owner = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r9_c2_ctrl"]/text()').extract()
        DealItems['use_right_owner'] = returnItem(use_right_owner)
        Min = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c2_ctrl"]/text()').extract()
        if Min:
            Min = Min[0]
        else:
            Min = 'Nah'
        Max = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f2_r1_c4_ctrl"]/text()').extract()
        if Max:
            Max = Max[0]
        else:
            Max = 'Nah'
        # DealItems['FAR'] = [{'Min': Min}, {'Max': Max}]
        deal_date = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r21_c4_ctrl"]/text()').extract()
        DealItems['deal_date'] = returnItem(deal_date)
        P_start_date = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c2_ctrl"]/text()').extract()
        DealItems['P_start_date'] = returnItem(P_start_date)
        P_end_date = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r22_c4_ctrl"]/text()').extract()
        DealItems['P_end_date'] = returnItem(P_end_date)
        A_start = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c2_ctrl"]/text()').extract()
        DealItems['A_start_date'] = returnItem(A_start)
        A_end = selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r10_c4_ctrl"]/text()').extract()
        DealItems['A_end_date'] = returnItem(A_end)
        Ratify= selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c2_ctrl"]/text()').extract()
        DealItems['Ratify'] = returnItem(Ratify)
        DealItems['Contract_date'] =  selector.xpath('//span[@id="mainModuleContainer_1855_1856_ctl00_ctl00_p1_f1_r14_c4_ctrl"]/text()')[0].extract()

        yield DealItems
