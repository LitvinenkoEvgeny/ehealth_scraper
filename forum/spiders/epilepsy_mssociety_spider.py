import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.selector import Selector
from forum.items import PostItemsList
import re
import logging

from helpers import cleanText


class ForumsSpider(CrawlSpider):
    name = "epilepsy_mssociety_spider"
    allowed_domains = ["mssociety.org.uk"]
    start_urls = [
        "https://community.mssociety.org.uk/forum",
    ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="forum-name"]',
        ), follow=True),

        Rule(LinkExtractor(
            allow=(r'\?page=\d+$'),
        ), callback="parsePostsList", follow=True),

        Rule(LinkExtractor(
            restrict_xpaths='//td[@class="views-field views-field-title"]/a',
        ), callback='parsePostsList', follow=True),

        Rule(LinkExtractor(
            restrict_xpaths='//li[@class="next"]',
        ), follow=True),

    )

    def parsePostsList(self, response):
        items = []
        subject = response.xpath('//div[@class="breadcrumb"]/text()')\
            .extract()

        subject = subject[3]
        url = response.url
        for post in response.xpath('//div[contains(@id, "post-")]'):
            item = PostItemsList()
            author = post.xpath(
                './/div[@class="author-pane-line author-name"]/a/text()')\
                .extract()
            author_link = post.xpath(
                './/div[@class="author-pane-line author-name"]/a/@href')\
                .extract()

            if len(author) == 0 and len(author_link) == 0:
                author = [u"anon"]
                author_link = [u"anon"]

            author = author[0]
            author_link = author_link[0]
            create_date = post.xpath(
                './/div[@class="forum-posted-on"]/text()')\
                .extract()[0].strip()
            message = " ".join(
                post.xpath('.//div[@class="forum-post-content"]//text()')
                .extract())
            message = cleanText(message)

            item['author'] = author
            item['author_link'] = author_link
            item['create_date'] = create_date
            item['post'] = message
            item['tag'] = 'epilepsy'
            item['topic'] = subject
            item['url'] = url

            items.append(item)
        return items
