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

post_data = (get_post_data(baseurl, headers))
date_data = '9f2c3acd-0256-4da2-a659-6949c4671a2a:'
cate = 'ec9f9d83-914e-4c57-8c8d-2c57185e912a:061~'+category
