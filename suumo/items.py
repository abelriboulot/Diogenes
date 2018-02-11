# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst

import re

# ([0-9]*\.[0-9]+|[0-9]+)
def get_number(x):
	x = strip_breaks(x)
	regex_number = r"([0-9]*\.[0-9]+|[0-9]+)"
	if type(x) is str and re.search(regex_number, x):
		match = re.search(regex_number, x).group(0)
		return float(match)
	else:
		return 0

def get_number_floors(x):
	x = strip_breaks(x)
	regex_number = r"([0-9]*\.[0-9]+|[0-9]+)"
	if type(x) is str and re.search(regex_number, x):
		for match in re.finditer(regex_number, x):
			pass
		return float(match.group(0))
	else:
		return 0

def strip_breaks(x):
	if (type(x) is unicode) or (type(x) is str):
		x = x.encode('utf-8')
		return x.replace("\n", "").replace("\r", "").replace(" ", "").replace("	", "")
	else:
		return x

def get_lat_long(x):
	x = strip_breaks(x)
	x = x.split("?ido=")[1]
	x = x.split("&keido=")
	x = map(get_number,x)
	return x

def get_dets(x):
	x = strip_breaks(x).split("、")
	return x

def get_lat(x):
	x = get_lat_long(x)[1]
	return x

def turn_image_into_original(x):
	return x[:-5]+'o.jpg'

number_field = Field(
				input_processor= MapCompose(get_number),
				output_processor=TakeFirst()
			)
text_field = Field(
				input_processor= MapCompose(strip_breaks),
				output_processor=TakeFirst()
			)

class Itemrent(Item):
	rent = number_field
	image_urls = Field(
				input_processor= MapCompose(turn_image_into_original)
					)
	images = Field()
	title = text_field
	Shiki = number_field
	Rei = number_field
	Typoroom = text_field
	m2 = number_field
	unknown3 = text_field
	manshionka = text_field
	age = number_field
	address = text_field
	sales_point_title = text_field
	agency = text_field
	agency_address = text_field
	agency_tel_nb = text_field
	subway_times = Field(
						input_processor= MapCompose(strip_breaks)
					)
	conditions = text_field
	details_property = Field(
						input_processor= MapCompose(get_dets)
					)
	floors = number_field
	floor_detail = Field(
						input_processor= MapCompose(get_number_floors),
						output_processor=TakeFirst()
					)
	insurance = text_field
	moving_in = text_field
	suumo_code = text_field
	material = text_field
	construction_date = text_field
	parking = text_field
	transaction_type = text_field
	update_infos = text_field
	lng = Field(
						input_processor= MapCompose(get_lat_long),
						output_processor=TakeFirst()
					)
	lat = Field(
						input_processor= MapCompose(get_lat),
						output_processor=TakeFirst()
					)
	urldet = text_field
	urlmap = text_field
	handling_store_code = text_field
	units_number = number_field
	pass
