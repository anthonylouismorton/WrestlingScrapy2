import scrapy
from wrestlingterritories.items import WrestlingEventItem


class EventSpider(scrapy.Spider):
    name = 'territoryEvent'
    start_urls = ['https://www.cagematch.net/']

    def parse(self, response):
        # commented out lines 14 - 23 for testing purposes

        territories = ['https://www.cagematch.net/?id=8&nr=2105&page=4', 'https://www.cagematch.net/?id=8&nr=442&page=4', 'https://www.cagematch.net/?id=8&nr=66&page=4', 'https://www.cagematch.net/?id=8&nr=2&page=4', 'https://www.cagematch.net/?id=8&nr=41&page=4', 'https://www.cagematch.net/?id=8&nr=739&page=4',
                       'https://www.cagematch.net/?id=8&nr=115&page=4', 'https://www.cagematch.net/?id=8&nr=293&page=4',
                       'https://www.cagematch.net/?id=8&nr=677&page=4', 'https://www.cagematch.net/?id=8&nr=1835&page=4',
                       'https://www.cagematch.net/?id=8&nr=62&page=4', 'https://www.cagematch.net/?id=8&nr=537&page=4',
                       'https://www.cagematch.net/?id=8&nr=499&page=4', 'https://www.cagematch.net/?id=8&nr=2693&page=4',
                       'https://www.cagematch.net/?id=8&nr=674&page=4', 'https://www.cagematch.net/?id=8&nr=408&page=4',
                       'https://www.cagematch.net/?id=8&nr=2018&page=4', 'https://www.cagematch.net/?id=8&nr=720&page=4', 'https://www.cagematch.net/?id=8&nr=373&page=4',
                       'https://www.cagematch.net/?id=8&nr=483&page=4', 'https://www.cagematch.net/?id=8&nr=465&page=4', 'https://www.cagematch.net/?id=8&nr=208&page=4',
                       'https://www.cagematch.net/?id=8&nr=103&page=4', 'https://www.cagematch.net/?id=8&nr=2173&page=4',
                       'https://www.cagematch.net/?id=8&nr=2113&page=4', 'https://www.cagematch.net/?id=8&nr=1831&page=4',
                       'https://www.cagematch.net/?id=8&nr=2017&page=4', 'https://www.cagematch.net/?id=8&nr=2114&page=4',
                       'https://www.cagematch.net/?id=8&nr=1678&page=4', 'https://www.cagematch.net/?id=8&nr=52&page=4',
                       'https://www.cagematch.net/?id=8&nr=67&page=4', 'https://www.cagematch.net/?id=8&nr=98&page=4',
                       'https://www.cagematch.net/?id=8&nr=64&page=4', 'https://www.cagematch.net/?id=8&nr=1044&page=4',
                       'https://www.cagematch.net/?id=8&nr=744&page=4',
                       'https://www.cagematch.net/?id=8&nr=1852&page=4', 'https://www.cagematch.net/?id=8&nr=1936&page=4',
                       'https://www.cagematch.net/?id=8&nr=682&page=4']
        # territories = ['https://www.cagematch.net/?id=8&nr=9&page=4']
        # territories = ['https://www.cagematch.net/?id=8&nr=1&page=4']

        for territory in territories:
            yield response.follow(territory, callback=self.parse2, meta={'territory': territory})

    def parse2(self, response):
        territory = response.meta.get('territory')
        table = response.css('table.TBase.TableBorderColor')
        rows = table.css('tr')
        rows = table.css('tr.TRow1, tr.TRow2')
        for row in rows:
            eventNumber = row.css(
                'td.TCol.AlignCenter.TextLowlight::text').get()
            matchPage = row.css('td.TCol.TColSeparator a::attr(href)').getall()
            for column in row.css('td.TCol.TColSeparator'):
                columnInfo = column.css(
                    'td.TCol.TColSeparator a::attr(href)').getall()
                if len(columnInfo) > 0 and 'page' not in columnInfo[0] and 'id=1' in columnInfo[0]:
                    matchPage = columnInfo[0]
            yield response.follow(matchPage, callback=self.parse3, meta={'eventNumber': eventNumber})
        eventPage = 100
        next_page_link = f'{territory}&s={eventPage}'
        while eventPage < 9000:
            yield response.follow(next_page_link, callback=self.parse2, meta={'territory': territory})
            eventPage += 100
            next_page_link = f'{territory}&s={eventPage}'

    def parse3(self, response):
        item = WrestlingEventItem()
        eventInfo = response.css('div.InformationBoxTable')
        itemList = ['Promotion', 'EventName', 'Date', 'Type', 'Location', 'Arena', 'Broadcasttype', 'Broadcastdate', 'TVStation', 'Commentators', 'Attendance',
                    'Wrestlers']
        eventNumber = response.meta.get('eventNumber')
        item['EventNumber'] = eventNumber
        for row in eventInfo.css('div.InformationBoxRow'):
            title = row.css(
                'div.InformationBoxTitle::text').get().replace(':', '')
            title2 = title.replace(' ', '')
            title3 = title2.replace('-', '')
            content = row.css(
                'div.InformationBoxContents a::text, div.InformationBoxContents::text')
            if title3 == 'Nameoftheevent':
                title3 = 'EventName'
                item[title3] = content.get()
                continue
            if title3 == 'Date':
                oldDate = content.get()
                newDate = oldDate.split(".")
                joinDate = '-'.join(newDate)
                item[title3] = joinDate
                continue
            if title3 == 'Broadcastdate':
                oldDate = content.get()
                newDate = oldDate.split(".")
                joinDate = '-'.join(newDate)
                item[title3] = joinDate
                continue
            if title3 == 'TVstation/network':
                title3 = 'TVStation'
                item[title3] = content.get()
                continue
            if title3 == 'Commentaryby':
                title3 = 'Commentators'
                item[title3] = content.get()
                continue
            if title3 == 'Promotion':
                simplifiedList = content.getall()
                item[title3] = simplifiedList
                continue
            if title3 not in itemList:
                continue
            if content.get() is not None:
                item[title3] = content.get()
        allWrestlers = response.css(
            'div.Comments.Font9 a::text, div.Comments.Font9::text').getall()
        if len(allWrestlers) > 0:
            item['Wrestlers'] = allWrestlers
        if eventInfo.get() is not None:
            yield item
