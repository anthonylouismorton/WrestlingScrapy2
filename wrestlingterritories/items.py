# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


def remove_quotes(value):
    return value.replace('"', '').strip()


class WrestlingterritoriesItem(scrapy.Item):
    # define the fields for your item here like:
    Wrestler = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Currentgimmick = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Age = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Promotion = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Brand = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Birthplace = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Gender = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Height = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Weight = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Backgroundinsports = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    SocialMedia = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Alteregos = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Roles = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Beginningofinringcareer = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=TakeFirst())
    Endofinringcareer = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Inringexperience = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Wrestlingstyle = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Trainer = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Nicknames = scrapy.Field(input_processor=MapCompose(
        remove_tags, remove_quotes), output_processor=TakeFirst())
    Signaturemoves = scrapy.Field(input_processor=MapCompose(
        remove_tags, remove_quotes), output_processor=TakeFirst())
    Dayofdeath = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    Causeofdeath = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())


class WrestlingPromotionInfo(scrapy.Item):
    Currentname = scrapy.Field()
    HeadQuarters = scrapy.Field()
    SocialMedia = scrapy.Field()
    ActiveTime = scrapy.Field()
    Website = scrapy.Field()
    Names = scrapy.Field()
    Abbreviations = scrapy.Field()
    Owners = scrapy.Field()
    OwnerDate = scrapy.Field()
    Popularevents = scrapy.Field()
    Televisionshows = scrapy.Field()
    Logos = scrapy.Field()
    LogoDates = scrapy.Field()


class WrestlingEventItem(scrapy.Item):
    Promotion = scrapy.Field()
    EventName = scrapy.Field()
    Date = scrapy.Field()
    Type = scrapy.Field()
    Location = scrapy.Field()
    Arena = scrapy.Field()
    Broadcasttype = scrapy.Field()
    Broadcastdate = scrapy.Field()
    TVStation = scrapy.Field()
    Commentators = scrapy.Field()
    Attendance = scrapy.Field()
    Wrestlers = scrapy.Field()
    WWW = scrapy.Field()
    EventNumber = scrapy.Field()


class WrestlingMatchItem(scrapy.Item):
    EventName = scrapy.Field()
    MatchType = scrapy.Field()
    MatchResults = scrapy.Field()
    EventNumber = scrapy.Field()
