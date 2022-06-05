import scrapy
from wrestlingterritories.items import WrestlingPromotionInfo
from scrapy.loader import ItemLoader


class PromotionsSpider(scrapy.Spider):
    name = 'promotions'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']

    def parse(self, response):
        for promotion in response.css('tr.TRow1, tr.TRow2'):
            URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
            # print(URL)
            yield response.follow(URL, callback=self.parse2)
        pageNumber = 0
        next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        while pageNumber < 2400:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber += 100

            next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'

    def parse2(self, response):
        item = WrestlingPromotionInfo()
        for row in response.css('div.InformationBoxRow'):
            try:
                title = row.css(
                    'div.InformationBoxTitle::text').get().replace(':','')
                title2 = title.replace(' ', '')
                title3 = title2.replace('-', '')
                content = row.css('div.InformationBoxContents::text')
            except:
                continue
            if title3 == 'Currentname':
                item[title3] = content.get()
                continue
            if title3 == 'Currentabbreviation':
                continue
            if title3 == 'Status':
                continue
            if title3 == 'Location':
                item['HeadQuarters'] = content.get()
                continue
            if title3 == 'WWW':
                accounts = row.css(
                    'div.InformationBoxContents a::text').getall()
                item['SocialMedia'] = accounts
                continue
            if title3 == 'Owners':
                owners = row.css(
                    'div.InformationBoxContents a::text, div.InformationBoxContents::text').getall()
                newOwners = []
                for owner in owners:
                    if owner == ' & ':
                        pass
                    newOwners.append(owner)
                item['Owners'] = newOwners
                continue
            if title3 == 'Names':
                names = row.css(
                    'div.InformationBoxContents::text').getall()
                item['Names'] = names
                continue
            if title3 == 'Televisionshows':
                shows = row.css(
                    'div.InformationBoxContents a::text').getall()
                item['Televisionshows'] = shows
                continue
            if title3 == 'Popularevents':
                popularEvents = row.css(
                    'div.InformationBoxContents a::text').getall()
                item['Popularevents'] = popularEvents
                continue
            if title3 == 'Logos':
                images = row.css('img').xpath('@src').getall()
                alts = row.css('img').xpath('@alt').getall()
                item['Logos'] = images
                item['LogoDates'] = alts
                continue
            if content.get() is not None:
                item[title3] = content.get()
            else:
                item[title3] = row.css(
                    'div.InformationBoxContents a::text').get()
        yield item
        # Name = response.css('h1.TextHeader::text').get()
        # yield {
        #     'name': Name
        # }
