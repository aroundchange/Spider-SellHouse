# -*- coding = utf8 -*-
# @Time  :2022/2/4 16:35
# @Author : Nico
# File : Spider-Spider-SellHouse.py
# @Software: PyCharm


import requests
import parsel
import csv
import time

f = open('静安区售房信息.csv', mode='a', encoding='utf_8_sig', newline='')
csv_write = csv.DictWriter(f, fieldnames=['标题', '地址', '户型', '面积', '朝向', '装修', '楼层', '年代', '关注及发布', '其它', '总价', '单价', '详情'])
csv_write.writeheader()

for page in range(1, 28):
    # time.sleep(3)
    print(f'======================正在爬取第{page}页数据内容======================')
    url = f'https://sh.lianjia.com/ershoufang/jingan/pg{page}/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36'}
    response = requests.get(url=url, headers=headers)
    # print(response.text)
    selector = parsel.Selector(response.text)
    divs = selector.css('div.info.clear')
    # print(divs)
    for div in divs:
        title = div.css('.title a::text').get()
        area_list = div.css('.positionInfo a::text').getall()
        area = '-'.join(area_list)
        house_info = div.css('.houseInfo::text').get().split('|')
        house_type = house_info[0]
        house_area = house_info[1]
        house_face = house_info[2]
        decoration = house_info[3]
        floor = house_info[4]
        years = house_info[5]
        follow_info = div.css('.followInfo::text').get().replace(' / ', ',')
        tag_list = div.css('.tag span::text').getall()
        tag = '|'.join(tag_list)
        totalprice = div.css('.totalPrice span::text').get() + '万'
        unitprice = div.css('.unitPrice span::text').get().replace('单价', '')
        href = div.css('.title a::attr(href)').get()
        dit = {
            '标题': title,
            '地址': area,
            '户型': house_type,
            '面积': house_area,
            '朝向': house_face,
            '装修': decoration,
            '楼层': floor,
            '年代': years,
            '关注及发布': follow_info,
            '其它': tag,
            '总价': totalprice,
            '单价': unitprice,
            '详情': href,
        }
        csv_write.writerow(dit)
        print(title, area, house_type, house_area, house_face, decoration, floor, years, follow_info, tag, totalprice,
              unitprice, href, sep='|')
print("爬取完毕！")

