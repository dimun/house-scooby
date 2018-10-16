import scrapy
import pprint

class FincaRaizSpider(scrapy.Spider):
    name = "finca_raiz"
    allowd_domains = ["fincaraiz.com.co"]
    start_urls = [
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|1||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||',
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|2||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||',
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|3||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||',
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|4||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||',
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|5||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||',
        'https://www.fincaraiz.com.co/lote-casa/venta/cali-jamundi/?ad=30|6||||1||2,9|||82|8200006,8200003|||190000000|||||||||||||1|||1||griddate%20desc||||-1||'
    ]

    def parse(self, response):
        for item in response.css('ul.advert'):
            yield {
                'link':  response.urljoin(item.css('li.title-grid .span-title>a::attr(href)').extract_first()),
                'description':  item.css('li.title-grid .span-title>a h2.h2-grid::text').extract_first() or
                                item.css('li.information .title-grid a::attr(title)').extract_first(),
                'surface':  item.css('li.surface::text').extract_first() or
                            item.css('li.information .title-grid .description::text').extract_first(),
                'price':    item.css('li.price div:first-child meta::attr(content)').extract_first() or
                            item.css('li.information .title-grid .descriptionPrice::text').extract_first(),
                'rooms': item.css('li.surface>div::text').extract_first(),
                'city': item.css('li.title-grid .span-title>a>div:last-child::text').extract_first(),
                'status': item.css('li.media .usedMark::text').extract_first() or 'Nuevo',
            }

        # next_page = response.css('div.pagination a.link-pag:last-child::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     print('page')
        #     print(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)
