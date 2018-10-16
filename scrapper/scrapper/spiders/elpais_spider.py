# -*- coding: utf-8 -*-

import scrapy

class FincaRaizSpider(scrapy.Spider):
    name = "el_pais"
    allowd_domains = ["fincaraiz.elpais.com.co"]
    start_urls = [
        "https://fincaraiz.elpais.com.co/avisos/venta/casas/cali"
    ]

    def parse(self, response):
        for item in response.css('article.flexArticle'):
            full_description = item.css('div.info div.description::text').extract_first()
            features = full_description.split(', ') if full_description else ['', 0,0,0]
            city, rooms, bathrooms, surface = features
            yield {
                'link':  response.urljoin(item.css('div.info>a.link-info::attr(href)').extract_first()),
                'surface': surface,
                'price': item.css('div.info div.price::text').extract_first(),
                'rooms': rooms,
                'bathrooms': bathrooms,
                'city': city
            }

        next_page = response.css('nav.pagination-box>ul.pagination>li.next>a::attr(href)').extract_first()
        if next_page is not None:
             next_page = response.urljoin(next_page)
             yield scrapy.Request(next_page, callback=self.parse)