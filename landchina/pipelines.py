# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import os
from landchina.items import DealItem
import re
import xlwt

class LandchinaPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client['landchina']
        self.Deal = db['Deal']

    def process_item(self,item,spider):
        try:
            self.Deal.insert(dict(item))
        except Exception as e:
            print(e)

        return item



XLS_FILE_DIR = os.path.dirname(os.path.abspath("__file__"))+r'/landchina/results'


class SaveExcelPipeline(object):

    def __init__(self):
        # {filename: index in handlers}
        self.file_mapper = {}
        self.handlers = []

    def gc_old_xls(self):
        free_list = []
        if len(self.file_mapper) > 10:
            for filename, index in self.file_mapper.items():
                i = index - 1
                if i < 0:
                    del self.handlers[index]
                    free_list.append(filename)
                else:
                    self.file_mapper[filename] = i

        for i in free_list:
            self.file_mapper.pop(i)

    def save_to_file(self, filename, item):
        if filename not in self.file_mapper:
            self.init_new_excel(filename)
            self.gc_old_xls()

        self.text_to_excel(filename, item)

    def init_new_excel(self, filename):
        xls = xlwt.Workbook()
        sheet = xls.add_sheet('sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, '所在地')
        sheet.write(0, 1, '电子监管号')
        sheet.write(0, 2, '项目名称')
        sheet.write(0, 3, '项目位置')
        sheet.write(0, 4, '面积(公顷)')
        sheet.write(0, 5, '土地来源')
        sheet.write(0, 6, '土地用途')
        sheet.write(0, 7, '供地方式')
        sheet.write(0, 8, '土地使用年限')
        sheet.write(0, 9, '行业分类')
        sheet.write(0, 10, '土地级别')
        sheet.write(0, 11, '成交价格(万元)')
        sheet.write(0, 12, '土地使用权人')
        sheet.write(0, 13, '约定交地时间')
        sheet.write(0, 14, '约定开工时间')
        sheet.write(0, 15, '约定竣工时间')
        sheet.write(0, 16, '实际开工时间')
        sheet.write(0, 17, '实际竣工时间')
        sheet.write(0, 18, '批准单位')
        sheet.write(0, 19, '合同签订日期')
        xls.save(os.path.join(XLS_FILE_DIR, filename + '.xls'))
        self.handlers.append(xls)
        self.file_mapper[filename] = len(self.handlers) - 1

    def process_item(self, item, spider):
        date = item['Contract_date']
        cate = item['Usage']
        r = re.compile('[0-9]\d*年[0-9]\d*月')
        date = re.search(r, date).group(0)
        filename = '-'.join([date,cate])
        self.save_to_file(filename, item)
        return item

    def text_to_excel(self, filename, item):
        index = self.file_mapper[filename]
        xls = self.handlers[index]
        sheet = xls.get_sheet('sheet1')
        row = sheet.last_used_row + 1
        sheet.write(row, 0, item['Dist'])
        sheet.write(row, 1, item['E_ID'])
        sheet.write(row, 2, item['Project_Name'])
        sheet.write(row, 3, item['Project_where'])
        sheet.write(row, 4, item['Area'])
        sheet.write(row, 5, item['Source'])
        sheet.write(row, 6, item['Usage'])
        sheet.write(row, 7, item['Provide_Method'])
        sheet.write(row, 8, item['expiry_date'])
        sheet.write(row, 9, item['category'])
        sheet.write(row, 10, item['rank'])
        sheet.write(row, 11, item['price'])
        sheet.write(row, 12, item['use_right_owner'])
        sheet.write(row, 13, item['deal_date'])
        sheet.write(row, 14, item['P_start_date'])
        sheet.write(row, 15, item['P_end_date'])
        sheet.write(row, 16, item['A_start_date'])
        sheet.write(row, 17, item['A_end_date'])
        sheet.write(row, 18, item['Ratify'])
        sheet.write(row, 19, item['Contract_date'])
        xls.save(os.path.join(XLS_FILE_DIR, filename + '.xls'))
