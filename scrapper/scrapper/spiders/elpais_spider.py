import scrapy

class FincaRaizSpider(scrapy.Spider):
    name = "el_pais"
    allowd_domains = ["fincaraiz.elpais.com.co"]

    def parse(self, response):
        for item in response.css('article.flexArticle'):
            full_description = item.css('div.info>div.description::text').extract_first()
            city, rooms, bathrooms, surface = full_description.split(',') else ['', 0,0,0]
            yield {
                'link':  response.urljoin(item.css('div.info>a.link-info::attr(href)').extract_first()),
                'surface': surface,
                'price': item.css('div.info>div.price::text').extract_first(),
                'rooms': rooms,
                'bathrooms': bathrooms,
                'city': city
            }