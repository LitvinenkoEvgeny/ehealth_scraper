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
    name = "epilepsy_macmillan_spider"
    allowed_domains = ["macmillan.org.uk"]
    start_urls = [
        "https://community.macmillan.org.uk/cancer_types/breast-cancer/discussions?pi1116=1",
    ]

    rules = (

        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="pager ui-page"]'),
            follow=True, callback='topic_parse'),

        Rule(LinkExtractor(
            restrict_xpaths='//h4[@class="post-name"]'),
            follow=True, callback='topic_parse'),

    )

    def topic_parse(self, response):
        if 'discussions' not in response.url:
            print(response.url)
            print("*" * 50)
            print(response.url)
            items = []

            subject = response.xpath(
                '//div[@class="forum-stats-container"]/h1/text()').extract()[0]
            subject = subject.strip()
            url = response.url
            posts = response.xpath(
                '//div[@class="full-post-container fiji-full-post-container evolution2-full-post-container"]')

            for post in posts:
                item = PostItemsList()
                author = post.xpath(
                    './/span[@class="user-name"]/a/text()')\
                    .extract()[1].strip()
                author_link = post.xpath(
                    './/span[@class="user-name"]/a/@href').extract()[0]
                create_date = post.xpath(
                    './/a[@class="internal-link view-post"]/text()')\
                    .extract()[0]
                message = ' '.join(post.xpath(
                    './/div[@class="post-content user-defined-markup"]//text()'
                ).extract())
                message = message.strip()

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
