# -*- coding: utf-8 -*-
from scrapy import Item,  Field
from scrapy.loader.processors import Compose, MapCompose, Join

# cleaning and extracting utilities
clean_text = Compose(MapCompose(lambda v: v.strip()), Join())   

class PropertyItem(Item):
    city = Field()
    price = Field()
    bedrooms = Field()
    bathrooms = Field()
    surface = Field()
    neighborhood = Field()
    status = Field()
