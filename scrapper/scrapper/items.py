# -*- coding: utf-8 -*-
from scrapy import Item,  Field
from scrapy.loader.processors import Compose, MapCompose, Join, TakeFirst, Identity

# processing utilities
import re
from w3lib.html import remove_tags

# cleaning and extracting utilities
def strip_spaces(input):
    return input.rstrip('\r\n ')

def extract_digits(input):
    return  re.findall(r'\b\d+\b',input)

class PropertyItem(Item):
    city = Field(
        input_processor=MapCompose(strip_spaces),
        output_processor=Join()
    )
    price = Field(
        input_processor=MapCompose(extract_digits),
        output_processor=TakeFirst()
    )
    bedrooms = Field(
        input_processor=MapCompose(extract_digits),
        output_processor=TakeFirst()
    )
    bathrooms = Field(
        input_processor=MapCompose(extract_digits),
        output_processor=TakeFirst()
    )
    surface = Field(
        input_processor=MapCompose(extract_digits),
        output_processor=TakeFirst()
    )
    neighborhood = Field(
        input_processor=MapCompose(strip_spaces),
        output_processor=Join()
    )
    status = Field()

    description = Field(
        input_processor=MapCompose(remove_tags),
        output_proccesor=Identity()
    )

    features = Field(
        
    )
