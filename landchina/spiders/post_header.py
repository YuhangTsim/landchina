#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import random
import sys
from datetime import datetime, timedelta
from landchina.start import end_date, category

def get_post_data(url, headers):
    # 访问一次网页,获取post需要的信息
    data = {
        'TAB_QuerySubmitSortData': '',
        'TAB_RowButtonActionControl': '',
    }

    try:
        req = requests.get(url, headers=headers)
    except Exception as e:
        print('get baseurl failed, try again!', e)
        sys.exit(1)
    try:
        soup = BeautifulSoup(req.text, "html.parser")
        TAB_QueryConditionItem = soup.find(
            'input', id="TAB_QueryConditionItem270").get('value')
        # print TAB_QueryConditionItem
        data['TAB_QueryConditionItem'] = TAB_QueryConditionItem
        TAB_QuerySortItemList = soup.find(
            'input', id="TAB_QuerySort0").get('value')
        # print TAB_QuerySortItemList
        data['TAB_QuerySortItemList'] = TAB_QuerySortItemList
        data['TAB_QuerySubmitOrderData'] = TAB_QuerySortItemList
        __EVENTVALIDATION = soup.find(
            'input', id='__EVENTVALIDATION').get('value')
        # print __EVENTVALIDATION
        data['__EVENTVALIDATION'] = __EVENTVALIDATION
        __VIEWSTATE = soup.find('input', id='__VIEWSTATE').get('value')
        # print __VIEWSTATE
        data['__VIEWSTATE'] = __VIEWSTATE
    except Exception as e:
        print('get post data failed, try again!', e)
        sys.exit(1)

    return data

def next_period(start, end):
    ''' 计算日期'''
    delta = (end-start).days
    start += timedelta(delta+1)
    end += timedelta(delta+1)
    distent2end = end_date-end
    if distent2end.days <= 0:
        start = start
        end = end_date
    return start, end

def makepost(start, end):
    start = datetime.strftime(start, '%Y-%m-%d')
    end = datetime.strftime(end,'%Y-%m-%d')
    period = start + '~' + end + '|'
    period
    return period

def returnItem(xpathItem):
    if xpathItem:
        ret = xpathItem[0]
    else:
        ret = 'Nah'
    return ret



baseurl = 'http://www.landchina.com/default.aspx?tabid=263'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36',
    'Host': 'www.landchina.com'
}

Cate = {'批发零售用地':'051',
        '住宿餐饮用地':'052',
        '商务金融用地':'053',
        '其他商服用地':'054',
        '工业用地':'061',
        '采矿用地':'062',
        '仓储用地':'063',
        '高档住宅用地':'071',
        '中低价位、中小套型普通商品住房用地':'072',
        '其他普通商品住房用地':'073',
        '经济适用住房用地':'074',
        '廉租住房用地':'075',
        '其他住房用地':'076',
        '公共租赁住房用地':'077',
        '机关团体用地':'081',
        '新闻出版用地':'082',
        '科教用地':'083',
        '医卫慈善用地':'084',
        '文体娱乐用地':'085',
        '公共设施用地':'086',
        '公园与绿地':'087',
        '风景名胜设施用地':'088',
        '军事设施用地':'091',
        '使领馆用地':'092',
        '监教场所用地':'093',
        '宗教用地':'094',
        '殡葬用地':'095',
        '铁路用地':'101',
        '公路用地':'102',
        '街巷用地':'103',
        '农村道路':'104',
        '机场用地':'105',
        '港口码头用地':'106',
        '管道码头用地':'107',
        '河流水面':'111',
        '湖泊水面':'112',
        '水库水面':'113',
        '坑塘水面':'114',
        '沿海滩涂':'115',
        '内陆滩涂':'116',
        '沟渠':'117',
        '水工建筑用地':'118',
        '冰川及永久积雪':'119',
        '工矿仓储用地':'gongy',
        '商业':'shangy',
        '住宅':'zhuz',
        '综合':'zhongh',
        '其他':'qiet',}

post_data = (get_post_data(baseurl, headers))
date_data = '9f2c3acd-0256-4da2-a659-6949c4671a2a:'
if category is not '':
    cate = 'ec9f9d83-914e-4c57-8c8d-2c57185e912a:'+Cate[category]+'~'+category
else:
    cate = ''
