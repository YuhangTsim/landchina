# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LandchinaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DealItem(scrapy.Item):
    ''' 土地成交信息'''
    Dist = scrapy.Field() # 行政区
    E_ID = scrapy.Field() # 电子监管号
    Project_Name = scrapy.Field() # 项目名称
    Project_where = scrapy.Field() # 项目位置
    Area = scrapy.Field() # 面积
    Source = scrapy.Field() # 土地来源
    Usage = scrapy.Field() # 土地用途
    Provide_Method = scrapy.Field() # 供地方式
    expiry_date = scrapy.Field() # 土地使用年限
    category = scrapy.Field() # 行业分类
    rank = scrapy.Field() # 土地级别
    price = scrapy.Field() # 成交价格
    payment = scrapy.Field() # 分期支付约定
    use_right_owner = scrapy.Field() # 土地使用权人
    FAR_min = scrapy.Field() # 容积率最小值
    FAR_max = scrapy.Field() # 容积率最大值
    deal_date = scrapy.Field() # 约定交地日期
    P_start_date = scrapy.Field() # 约定开工时间
    P_end_date = scrapy.Field() # 约定竣工时间
    A_start_date = scrapy.Field() # 实际开工时间
    A_end_date = scrapy.Field() # 实际竣工时间
    Ratify = scrapy.Field() # 批准单位
    Contract_date = scrapy.Field() # 合同签订日期
