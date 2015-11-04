from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from forum.items import PostItemsList
import logging


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
    name = "epilepsy_idonline_spider"
    allowed_domains = ["ldonline.org"]
    start_urls = [
        "http://www.ldonline.org/xarbb/?catid=769",
    ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//span[@class="xar-title"]/a'),
            follow=True),

        Rule(LinkExtractor(
            restrict_xpaths='//a[contains(@title, "Next 10 pages")]'),
            follow=True),

        Rule(LinkExtractor(
            restrict_xpaths='//td[@class="xar-norm icon"]/a'),
            callback="topic_parse", follow=True),
    )

    def topic_parse(self, response):
        print("*" * 50)
        print(response.url)
        items = []

        subject = response.xpath(
            '//title/text()').extract()[0]
        subject = subject.split('|')[0]
        url = response.url
        posts = response.xpath('//table//tr')[1:-1:2]

        for post in posts:
            item = PostItemsList()
            author = post.xpath(
                './/td[@class="xar-norm author"]/*/a/text()').extract()[0]
            author_link = post.xpath(
                './/td[@class="xar-norm author"]/*/a/@href').extract()[0]
            create_date = post.xpath(
                './/span[@class="xar-sub"][contains(text(), "Posted")]/text()'
            ).extract()[0]
            message = ''.join(post.xpath(
                './/div[2]/p//text()'
            ).extract())

            item['author'] = author
            item['author_link'] = author_link
            item['create_date'] = create_date
            item['post'] = message
            item['tag'] = 'epilepsy'
            item['topic'] = subject
            item['url'] = url

            items.append(item)
        return items
        print("*" * 50)
