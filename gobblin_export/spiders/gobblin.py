# -*- coding: utf-8 -*-
from __future__ import print_function
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.spiders.crawl import Rule, CrawlSpider
from gobblin_export.items import MediaItem, MediaItemLoader


class GobblinSpider(CrawlSpider):
    name = "gobblin"
    allowed_domains = ["gobblin.se"]
    start_urls = (
        'https://gobblin.se/',
    )

    rules = [
        Rule(LinkExtractor(allow=r'/u/.*/m/.*/.*'), 'parse_media'),
        Rule(
            LinkExtractor(restrict_xpaths=('//div[@class="pagination"]/p'
                                           '/a[contains(text(), "Older")]',)),
            follow=True)
    ]

    def __init__(self, username=None):
        super(GobblinSpider, self).__init__()
        if username is not None:
            self.start_urls = ['https://gobblin.se/u/{}/'.format(username)]

    def parse_media(self, response):
        l = MediaItemLoader(item=MediaItem(), response=response)
        # Image
        l.add_xpath('original',
                    '//div[@class="media_image_container"]/a[1]/@href')
        l.add_xpath('original',
                    '//div[@class="media_image_container"]/img/@src')

        # Video and audio
        l.add_xpath('original',
                    '//div[contains(@class, "media_sidebar")]'
                    '//a[contains(text(), "Original")]/@href')

        l.add_xpath('title', '//h2[@class="media_title"]/text()')

        try:
            l.add_value('slug', response.url.strip('/').split('/').pop())
        except Exception as exc:
            print(exc)

        item = l.load_item()

        item.save_file()

        return item



