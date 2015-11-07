# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from forum.items import PostItemsList


class EpilepsyBreastcancerSpiderSpider(CrawlSpider):
    name = 'epilepsy_breastcancer_spider'
    allowed_domains = ['breastcancer.org']
    start_urls = ['https://community.breastcancer.org/']

    rules = (
        Rule(LinkExtractor(allow=r'/forum/\d+$'), follow=True),
        Rule(LinkExtractor(allow=r'/forum/\d+/topics/\d+$'), follow=True),
        Rule(
            LinkExtractor(allow=(r'/forum/\d+/topics/\d+\?page=\d+')),
            callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=r'/forum/\d+\?page=\d+$'), follow=True),
    )

    def parse_item(self, response):
        def clean_date(date):
            if len(date) > 1:
                date = date[0].split('\n')
                date = date[2]
                return date.strip()
            else:
                date = date[0].split('\n')[2]
                return date.strip()


        url = response.url
        original_author = response.xpath(
            '//div[@class="original-topic"]//div[@class="user-post"]/p/strong/a/text()').extract()[0]
        original_author_link = response.xpath(
            '//div[@class="original-topic"]//div[@class="user-post"]/p/strong/a/@href').extract()[0]
        original_create_date = response.xpath(
            '//div[@class="original-topic"]//span[@class="posted-time left"]//text()'
            ).extract()
        original_create_date = clean_date(original_create_date)
        print('_' * 100)
        print(len(original_create_date))
        print(original_create_date)
