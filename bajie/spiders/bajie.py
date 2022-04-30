# -*- coding: utf-8 -*-
import scrapy
import json
import os
import time
import datetime
import sys
import re
import pymysql
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bajie.items import BajieItem




class bajie(CrawlSpider):
    name = 'bajie'
    allowed_domains = [
        'bajiecaiji.com'
    ]

    start_urls = []
    filmUrls = [
        'http://cj.bajiecaiji.com/?m=vod-type-id-4.html',
        'http://cj.bajiecaiji.com/?m=vod-type-id-4-pg-$.html',
    ]

    pageNum = 26 #534 #81 #20 #26
    i = 1
    while i <= pageNum:
        if i == 1:
            start_urls.append(filmUrls[0])
        else:
            start_urls.append(filmUrls[1].replace('$', str(i), 1))
        i += 1

    # http://cj.bajiecaiji.com/?m=vod-type-id-1.html
    # http://cj.bajiecaiji.com/?m=vod-type-id-1-pg-2.html
    rules = (
        # Rule(LinkExtractor(allow=('\?m=vod-detail-id-207365\.html')), callback = 'parseFilmSpider'),
        Rule(LinkExtractor(allow=('\?m=vod-detail-id-\d+\.html')), callback = 'parseFilmSpider'),
    )

    def parseFilmSpider(self, response):
        item = BajieItem()
        name = response.xpath("//div[@class='videoDetail']/li[1]/text()").extract()[0].split(': ')[1]
        item['filmsName'] = re.sub(r"\[|]|\"|”|\'|’|\s|（|）|(|)",'',name)   
        item['directors'] = response.xpath("//div[@class='videoDetail']/li[5]/text()").extract()[0].split(': ')[1]
        item['stars'] = response.xpath("//div[@class='videoDetail']/li[4]/text()").extract()[0].split(': ')[1].replace('更多...','').strip('、')
        item['tags'] = response.xpath("//div[@class='videoDetail']/li[6]/div[1]/text()").extract()[0].split(': ')[1].replace(' ','')
        years = response.xpath("//div[@class='videoDetail']/li[8]/div[2]/text()").extract()[0].split(': ')[1]
        item['years'] = time.mktime(time.strptime(years, "%Y"))
        item['language'] = response.xpath("//div[@class='videoDetail']/li[7]/div[1]/text()").extract()[0].split(': ')[1]
        item['content'] = response.xpath("//div[@class='movievod']/p[2]/text()").extract()
        item['countries'] = response.xpath("//div[@class='videoDetail']/li[7]/div[2]/text()").extract()[0].split(': ')[1]
        item['picAddr'] = response.xpath("//div[@class='videoPic']/img/@src").extract()[0]
        item['playAddr'] = {
            'yun' : {
                'name' : [],
                'addr' : []
            },
            'm3u8' : {
                'name' : [],
                'addr' : []
            }
        }
        playAddr = response.xpath("//div[@class='movievod']/ul/li/input/@value").extract()
        playAddr.pop()
        playAddrArr = self.list_split(playAddr,int(len(playAddr) / 2))

        for i in range(len(playAddrArr[0])):
            addrArr = playAddrArr[0][i].split('$')
            item['playAddr']['yun']['name'].append(addrArr[0])
            item['playAddr']['yun']['addr'].append(addrArr[1])

        for i in range(len(playAddrArr[1])):
            addrArr = playAddrArr[1][i].split('$')
            item['playAddr']['m3u8']['name'].append(addrArr[0])
            item['playAddr']['m3u8']['addr'].append(addrArr[1])


        item['douban'] = 0
        item['filmLength'] = 0
        item['createTime'] = int(round(time.time()))
        item['updateTime'] = int(round(time.time()))
        yield item


    def list_split(self, items, n):
        return [items[i:i+n] for i in range(0, len(items), n)]





      