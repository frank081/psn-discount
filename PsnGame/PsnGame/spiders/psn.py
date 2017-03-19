# -*- coding: utf-8 -*-

import urllib.parse

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

from PsnGame.items import PsnGameItem


class PsnGameLoader(ItemLoader):
    default_item_class = PsnGameItem
    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()


class PsnSpider(scrapy.Spider):
    name = "psn"

    def start_requests(self):
        domain_urls = {
            "JP": [
                'https://store.playstation.com/#!/ja-jp/ゲーム・追加アイテム/cid=PN.CH.JP-PN.CH.MIXED.JP-PS4GAMEADD/',
                'https://store.playstation.com/#!/ja-jp/ゲーム・追加アイテム/cid=PN.CH.JP-PN.CH.MIXED.JP-PSVGAMEADD'
            ],
            "HK": [
                'https://store.playstation.com/#!/zh-hans-hk/ps4-游戏/cid=STORE-MSF86012-PS4TITLES',
                'https://store.playstation.com/#!/zh-hans-hk/ps-vita-游戏/cid=STORE-MSF86012-PSVITAGAMES'
            ]
        }

        for (domain, urls) in domain_urls.items():
            for url in urls:
                yield scrapy.Request(
                    url=url, callback=lambda response, d=domain: self.parse_game(response, d))

    def parse_game(self, response, domain):
        for game in response.css(".cellGridGameStandard"):
            loader = PsnGameLoader(selector=game)
            loader.add_value("domain", domain)
            loader.add_css("game_name", ".cellTitle::text")
            loader.add_css("platform", ".pforms::text")
            loader.add_css("buy_price", ".buyPrice::text")
            loader.add_css("ps_plus_price", ".psPlusPrice::text")
            loader.add_css("origin_price", ".strikePrice .price::text")
            loader.add_value("game_url", urllib.parse.unquote(response.urljoin(
                urllib.parse.quote(game.css("a.permalink::attr(href)").extract_first()))))
            loader.add_css("image_url", ".thumbPane img::attr(src)")
            yield loader.load_item()

        next_page = response.css(".headCtls .pageLink.selected + a::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(next_page, lambda r, d=domain: self.parse_game(r, d))

    def parse(self, response):
        pass
