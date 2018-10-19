# -*- coding: utf-8 -*-

from scrapy import Spider, Request

class ElPaisSpider(Spider):
    name = "el_pais"
    allowd_domains = ["fincaraiz.elpais.com.co"]
    cities = ['cali', 'jamundi', 'palmira']
    types = ['casas', 'lotes', 'apartamentos', 'fincas-y-casas-campestres', 'apartaestudios']
    start_urls = [
        "https://fincaraiz.elpais.com.co/avisos/venta/{0}/{1}".format(t,c) for t in types for c in cities
    ]

    def parse(self, response):
        for item in response.css('article.flexArticle'):
            full_description = item.css('div.info div.description::text').extract_first()
            features = full_description.split(', ') if full_description else ['', 0,0,0]
            city, rooms, bathrooms, surface = features
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
        item['contact_phone'] = response.css('div.info p:first-child::text').extract_first()
        item['contact_email'] = response.css('div.info p:last-child::text').extract_first()

        # extract feature list
        feature_names = response.css('div.caract ul li strong::text').extract_all()
        feature_values = response.css('div.caract ul li::text').extract_all()
        item['features'] = dict(zip(feature_names, feature_values))
        yield item
