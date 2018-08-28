import scrapy


class FincaRaizSpider(scrapy.Spider):
    name = "finca_raiz"
    start_urls = ['https://www.fincaraiz.com.co/finca-raiz/cali/']

    def parse(self, response):
        for item in response.css('.Product_Code'):
            yield {
                'surface': item.css('li.surface>div.text::text').extract_first(),
                'price': item.css('li.price>div.text::text').extract_first(),
                'rooms': item.css('li.text-city>div.rooms::text').extract_first(),
                'city': item.css('li.text-city>a::text').extract_first(),
            }

        next_page = response.css('div.pagination>a.link-page:last-child::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
