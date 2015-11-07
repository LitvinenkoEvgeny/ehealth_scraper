from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from forum.items import PostItemsList


# import lxml.html
# from lxml.etree import ParserError
# from lxml.cssselect import CSSSelector

# LOGGING to file
# import logging
# from scrapy.log import ScrapyFileLogObserver

# logfile = open('testlog.log', 'w')
# log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
# log_observer.start()

# Spider for crawling Adidas website for shoes


class ForumsSpider(CrawlSpider):
    name = "epilepsy_healthboards_spider"
    allowed_domains = ["healthboards.com"]
    start_urls = [
        "http://www.healthboards.com/boards/cancer-breast/",
    ]

    rules = (

        Rule(LinkExtractor(
            # forum pagination
            restrict_xpaths='//*[@rel="next"]',
            allow=(r"/index\d+\.html")),
            follow=True),

        Rule(LinkExtractor(
            restrict_xpaths='//a[contains(@id, "thread_title")]'),
            callback="topic_parse", follow=True),

        Rule(LinkExtractor(
            # topic pagination
            restrict_xpaths='//a[@rel="next"][@class="smallfont"]'),
            callback="topic_parse", follow=True),

    )

    def topic_parse(self, response):
        print(response.url)
        items = []

        subject = response.xpath(
            '//div[@class="navbar"]/strong/text()').extract()[0]
        subject = subject.strip()
        url = response.url
        posts = response.xpath('//table[contains(@id, "post")]')

        for post in posts:
            item = PostItemsList()
            author = post.xpath(
                './/div[contains(@id, "postmenu")]/text()').extract()[0]
            author = author.strip()
            author_link = "*"
            create_date = post.xpath(
                './/td[@class="thead"]//text()'
            ).extract()[1].strip()

            message = ''.join(post.xpath(
                './/div[contains(@id, "post_message_")]//text()'
            ).extract()).strip()

            item['author'] = author
            item['author_link'] = author_link
            item['create_date'] = create_date
            item['post'] = message
            item['tag'] = 'epilepsy'
            item['topic'] = subject
            item['url'] = url

            items.append(item)
        return items
