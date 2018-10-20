# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from scrapper.items import PropertyItem

# cities = ['cali', 'jamundi', 'palmira']
cities = ['cali']
# types = ['casas', 'lotes', 'apartamentos', 'fincas-y-casas-campestres', 'apartaestudios']
types = ['casas']

class ElPaisSpider(Spider):
    name = "el_pais"
    allowed_domains = ["fincaraiz.elpais.com.co"]
    start_urls = [
        "https://fincaraiz.elpais.com.co/avisos/venta/{0}/{1}".format(t,c) for t in types for c in cities
    ]

    def parse(self, response):
        for item in response.css('article.flexArticle'):
            property_item = PropertyItem()
            full_description = item.css('div.info div.description::text').extract_first()
            city, rooms, bathrooms, surface = full_description.split(', ') if full_description else ['', 0, 0, 0]
            property_url = response.urljoin(item.css('div.info>a.link-info::attr(href)').extract_first())
            
            # fill properties
            property_item['link'] = property_url
            property_item['surface'] = surface
            property_item['price'] = item.css('div.info div.price::text').extract_first()
            property_item['bedrooms'] = rooms
            property_item['bathrooms'] = bathrooms
            property_item['city'] = city

            # call single element page
            request = Request(property_url, self.parse_single)
            request.meta['item'] = property_item
            yield request

        next_page = response.css('nav.pagination-box>ul.pagination>li.next>a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield Request(next_page, callback=self.parse)

    def parse_single(self, response):
        item = response.meta['item']

        # internal unique identifier
        item['internal_id'] = response.css('.id-web p.id').extract_first().split(':')[1]

        # general desc
        item['description'] = response.css('div.descripcion p::text').extract_first()
        item['contact_info'] = response.css('div.info p::text').extract()

        # extract feature list
        feature_names = list(map(lambda x: x.strip(), response.css('div.caract ul li strong::text').extract())) + \
            list(map(lambda x: x.strip(), response.css('div.caract ul:nth-child(2) li strong::text').extract()))
        feature_values = list(map(lambda x: x.strip(), response.css('div.caract ul li:not(strong)::text').extract())) + \
            list(map(lambda x: x.strip(), response.css('div.caract ul:nth-child(2) li:not(strong)::text').extract()))

        # remove empty values before create dict
        feature_values = [v for v in feature_values if v != '']
        item['features'] = dict(zip(feature_names, feature_values))

        # process other features
        item['other_features'] = list(
            filter(
                (lambda x: x != ''),
                list(
                    map(
                        lambda x: x.strip(),
                        response.css('div.caract ul:nth-child(3) li::text').extract()
                    )
                )
            )
            
        )

        yield item
