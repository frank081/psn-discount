# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import locale


class PsnGamePipeline(object):

    _free_str = {
        "JP": "無料",
        "HK": "免费"
    }

    _currency_symbol = {
        "JP": "¥",
        "HK": "HK$"
    }

    _locale_code ={
        "JP": "ja_JP.utf8",
        "HK": "zh_HK.utf8"
    }

    def __parse_currency(self, domain, currency_str):
        locale.setlocale(locale.LC_NUMERIC, PsnGamePipeline._locale_code[domain])

        return str(int(locale.atof(
            currency_str.replace(
                PsnGamePipeline._free_str[domain], "0"
            ).replace(
                PsnGamePipeline._currency_symbol[domain], ""
            )
        )))

    def process_item(self, item, spider):

        item.setdefault("buy_price", "0")
        item.setdefault("origin_price", item["buy_price"])
        item.setdefault("ps_plus_price", item["buy_price"])

        item["buy_price"] = self.__parse_currency(item["domain"], item["buy_price"])
        item["origin_price"] = self.__parse_currency(item["domain"], item["origin_price"])
        item["ps_plus_price"] = self.__parse_currency(item["domain"], item["ps_plus_price"])

        return item
