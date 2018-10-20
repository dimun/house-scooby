# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from pprint import pprint


class ElPaisSpider(Spider):
    name = "el_pais"
    allowd_domains = ["fincaraiz.elpais.com.co"]
    # cities = ['cali', 'jamundi', 'palmira']
    cities = ['cali']
    # types = ['casas', 'lotes', 'apartamentos', 'fincas-y-casas-campestres', 'apartaestudios']
    types = ['casas']
    start_urls = [
        "https://fincaraiz.elpais.com.co/avisos/venta/{0}/{1}".format(t,c) for t in types for c in cities
    ]

    def parse(self, response):
        for item in response.css('article.flexArticle'):
            full_description = item.css('div.info div.description::text').extract_first()
            features = full_description.split(', ') if full_description else []
            city = features[0] if 0 in features else '' 
            rooms = features[1] if 1 in features else 0
            bathrooms = features[2] if 2 in features else 0
            surface = features[3] if 3 in features else 0
            property_url = response.urljoin(item.css('div.info>a.link-info::attr(href)').extract_first())
            property_item = {
                'link':  property_url,
                'surface': surface,
                'price': item.css('div.info div.price::text').extract_first(),
                'rooms': rooms,
                'bathrooms': bathrooms,
                'city': city
            }
            # call single element page
            yield Request(url=property_url, callback=self.parse_single, meta=dict(item=property_item))

        next_page = response.css('nav.pagination-box>ul.pagination>li.next>a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)

    def parse_single(self, response):
        item = response.meta['item']
        item['description'] = response.css('div.descripcion p::text').extract_first()
        item['contact_info'] = response.css('div.info p::text').extract()

        # extract feature list
        feature_names = list(map(lambda x: x.strip(), response.css('div.caract ul li strong::text').extract()))
        feature_values = list(map(lambda x: x.strip(), response.css('div.caract ul li:not(strong)::text').extract()))

        # remove empty values before create dict
        feature_values = [v for v in feature_values if v != '']
        item['features'] = dict(zip(feature_names, feature_values))

        # process other features
        item['other_features'] = list(
            map(
                lambda x: x.strip(),
                response.css('div.caract ul:nth-child(2) li::text').extract() + \
                response.css('div.caract ul:nth-child(3) li::text').extract()
            )
        )

        yield item
