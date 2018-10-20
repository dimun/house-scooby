# -*- coding: utf-8 -*-

from scrapy import Spider, Request

types = ['apartamento', 'casa-lote', 'casa-campestre', 'casa', 'lote', 'finca']
cities = ['cali', 'jamundi', 'palmira']
min_price = '60000000'
max_price = '190000000'
base_url = 'https://www.fincaraiz.com.co/{0}/venta/{1}/?ad=30|{2}||||1||8,21,23,7|||82|8200006|8200104|{3}|{4}||||||||||||||||1||griddate%20desc||||-1||'

class FincaRaizSpider(Spider):
    name = "finca_raiz"
    allowed_domains = ["fincaraiz.com.co"]
    start_urls = [
        base_url.format(t, c, i, min_price, max_price) 
        for t in types
        for c in cities
        for i in range(1, 10)
    ]

    def parse(self, response):
        for item in response.css('ul.advert'):
            # clean input data
            description = item.css('li.title-grid .span-title>a h2.h2-grid::text').extract_first() or \
                item.css('li.information .title-grid a::attr(title)').extract_first()

            surface = item.css('li.surface::text').extract_first() or \
                item.css('li.information .title-grid .description::text').extract_first()

            price = item.css('li.price div:first-child meta::attr(content)').extract_first() or \
                item.css('li.information .title-grid .descriptionPrice::text').extract_first()

            full_location = item.css('li.title-grid .span-title>a>div:last-child::text').extract_first()
            neighborhood, city = full_location.split('-') if full_location else ["", ""]

            yield {
                'link':  response.urljoin(item.css('li.title-grid .span-title>a::attr(href)').extract_first()),
                'description': description,
                'surface':  surface,
                'price':    price,
                'rooms': item.css('li.surface>div::text').extract_first(),
                'neighborhood': neighborhood,
                'city': city,
                'status': item.css('li.media .usedMark::text').extract_first() or 'Nuevo',
            }

        # next_page = response.css('div.pagination a.link-pag:last-child::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     print('page')
        #     print(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
