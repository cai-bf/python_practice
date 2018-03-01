#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import re
from multiprocessing.pool import Pool

import requests
from requests.exceptions import RequestException
num = 1


def get_page(url):
    global num
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('抓取第'+str(num)+'页')
            num = num+1
            return response.text
        return None
    except RequestException:
        return None


def parse_page(html_cont):
    pattern = re.compile(r'.*?(\d+)</em>.*?<span class="title">(.*?)</span>.*?'
                         + '<span class="rating_num" property="v:average">(.*?)</span>.*?<span class="inq">(.*?)'
                         + '</span>', re.S)
    items = re.findall(pattern, html_cont)
    for item in items:
        yield 'index:' + item[0] + '  ' + 'name:' + item[1] + '  ' + 'score:' + item[2] + '  ' + 'quote:' + item[3]


def write2file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'https://movie.douban.com/top250?start=' + str(offset) + '&filter='
    html_cont = get_page(url)
    for item in parse_page(html_cont):
        write2file(item)


if __name__ == '__main__':
    # for i in range(0, 50, 5):
    #     main(i*5)
    # 使用进程池，可能存在抓取后信息写入丢失情况
    pool = Pool()
    pool.map(main, [i*5 for i in range(1, 50, 5)])
    pool.close()
    pool.join()
