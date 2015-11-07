# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from forum.items import PostItemsList


class EpilepsyCancerSpiderSpider(CrawlSpider):
    name = 'epilepsy_cancer_spider'
    allowed_domains = ['csn.cancer.org']
    start_urls = ['https://csn.cancer.org/forum/127']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//td[@class="title"]'),
             callback='parse_item', follow=True),

        # pagination
        Rule(LinkExtractor(allow=(r'/forum/127\?page=\d+')),
             follow=True),
    )

    def parse_item(self, response):
        items = []
        node_item = PostItemsList()
        subject = response.xpath(
            '//div[@class="left-corner"]/h2/text()'
        ).extract()[0]
        url = response.url
        node_post = response.xpath('//table[@class="node node-forum"]')
        node_author = node_post.xpath(
            './/div[@class="author"]/text()').extract()[0]
        node_time = u''.join(
            node_post.xpath('.//div[@class="date"]//text()').extract()).strip()
        node_message = u''.join(
            node_post.xpath(
                './/div[@class="content"]//text()').extract())
        posts = response.xpath('//table[@class="comment comment-forum"]')

        node_item['author'] = node_author
        node_item['author_link'] = '*'
        node_item['create_date'] = node_time
        node_item['post'] = node_message
        node_item['tag'] = 'epilepsy'
        node_item['topic'] = subject
        node_item['url'] = url

        items.append(node_item)

        for post in posts:
            item = PostItemsList()
            author = post.xpath('.//div[@class="author"]/text()').extract()[0]
            date = post.xpath('.//div[@class="date"]//text()').extract()[0]
            message = u''.join(
                post.xpath('.//div[@class="content"]//text()')
                .extract()).strip()

            item['author'] = author
            item['author_link'] = '*'
            item['create_date'] = date
            item['post'] = message
            item['tag'] = 'epilepsy'
            item['topic'] = subject
            item['url'] = url

            items.append(item)
        return items
