#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json
import re
# from multiprocessing.pool import Pool

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
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?name">'
                         + '.*?>(.*?)</a>.*?star">(.*?)</p>.*?'
                         + 'integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>', re.S)
    items = re.findall(pattern, html_cont)
    for item in items:
        yield 'index:' + item[0] + '  ' + 'name:' + item[1] + '  ' + 'star:' + item[2].strip()[3:] + '  ' + 'quote:' + item[3] + item[4]


def write2file(content):
    with open('maoyantop100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html_cont = get_page(url)
    for item in parse_page(html_cont):
        write2file(item)


if __name__ == '__main__':
    # pool = Pool()
    # pool.map(main, [i*10 for i in range(10)])           
    # pool.close()
    # pool.join()
    for i in range(10):
        main(i*10)

