# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from __future__ import print_function

import os
import shutil
import requests
import scrapy

from scrapy.contrib.loader import ItemLoader
from scrapy.contrib.loader.processor import TakeFirst, MapCompose, Join, Compose


class MediaItem(scrapy.Item):
    slug = scrapy.Field()
    title = scrapy.Field()
    original = scrapy.Field()

    def save_file(self):
        url = self['original']
        out_dir = os.path.join('downloaded', self['slug'])
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)


        try:
            req = requests.get(url, stream=True)

            if req.status_code == 200:
                with open(os.path.join(out_dir, os.path.basename(url)),
                          'wb') as f:
                    req.raw.decode_content = True
                    shutil.copyfileobj(req.raw, f)
        except IOError as exc:
            print('Exception! {}'.format(exc))


class MediaItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    #default_input_processor = Compose(TakeFirst(), unicode.strip)

    title_in = MapCompose(unicode.strip)
