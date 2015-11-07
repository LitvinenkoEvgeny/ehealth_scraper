import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor


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
    name = "epilepsy_komen_spider"
    allowed_domains = ["komen.org"]
    start_urls = [
        "https://apps.komen.org/Forums/",
    ]

    rules = (

        Rule(LinkExtractor(
            # get all forums
            allow=(r"forumid=\d+")),
            callback="new_req", follow=True),

        #     Rule(LinkExtractor(
        # get all topics
        #         restrict_xpaths='//a[contains(@id, "msgSubjectLink_")]'),
        #         callback="topic_parse", follow=True),

        # Rule(LinkExtractor(
        #     # forume pagination
        #     allow=(r"forumid=\d+&p=\d+")),
        #     callback="topic_parse", follow=True),
    )

    def new_req(self, response):
        request = scrapy.Request(
            url=response.url,
            cookies={"KomenForumApptimefilter": "0"},
            callback="topic_parse"
        )
        return request

    def topic_parse(self, response):
        print("=" * 50)
        print("fdsaafdssdfkljflajflkjsfkljsdklfjskljfksjklfdsjkljfsdkljfsdalj")
        print("=" * 50)
        # print(response.url)
        # items = []

        # subject = response.xpath(
        #     '//div[@class="navbar"]/strong/text()').extract()[0]
        # subject = subject.strip()
        # url = response.url
        # posts = response.xpath('//table[contains(@id, "post")]')

        # for post in posts:
        #     item = PostItemsList()
        #     author = post.xpath(
        #         './/div[contains(@id, "postmenu")]/text()').extract()[0]
        #     author = author.strip()
        #     author_link = "*"
        #     create_date = post.xpath(
        #         './/td[@class="thead"]//text()'
        #     ).extract()[1].strip()

        #     message = ''.join(post.xpath(
        #         './/div[contains(@id, "post_message_")]//text()'
        #     ).extract()).strip()

        #     item['author'] = author
        #     item['author_link'] = author_link
        #     item['create_date'] = create_date
        #     item['post'] = message
        #     item['tag'] = 'epilepsy'
        #     item['topic'] = subject
        #     item['url'] = url

        #     items.append(item)
        # return items
