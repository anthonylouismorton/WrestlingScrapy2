import scrapy
from wrestlingterritories.items import WrestlingEventItem


class EventSpider(scrapy.Spider):
    name = 'event'
    start_urls = [
        'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&status=&name=&location=&minRating=&maxRating=&minVotes=&maxVotes=']

    def parse(self, response):
        # commented out lines 14 - 23 for testing purposes
        for promotion in response.css('tr.TRow1, tr.TRow2'):
            URL = promotion.css('td.TCol.TColSeparator a::attr(href)').get()
            yield response.follow(URL, callback=self.parse2, meta={'URL': URL})
        pageNumber = 100
        next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        while pageNumber < 2500:
            yield response.follow(next_page_link, callback=self.parse)
            pageNumber += 100
            next_page_link = f'https://www.cagematch.net/en/?id=8&view=promotions&region=Amerika&s={pageNumber}'
        # yield response.follow('https://www.cagematch.net/en/?id=8&nr=64&page=4', callback=self.parse2, meta={'URL': URL})

    def parse2(self, response):
        URL = response.meta.get('URL')
        header = response.css('ul.ContentNavigator')
        eventsPage = ''
        for li in header.css('li'):
            if li.css('a::text').get() == 'Events':
                eventsPage = li.css('a::attr(href)').get()
        yield response.follow(eventsPage, callback=self.parse3, meta={'URL': URL})

    def parse3(self, response):
        URL = response.meta.get('URL')
        table = response.css('table.TBase.TableBorderColor')
        rows = table.css('tr')
        rows = table.css('tr.TRow1, tr.TRow2')
        for row in rows:
            matchPage = row.css('td.TCol.TColSeparator a::attr(href)').getall()
            for column in row.css('td.TCol.TColSeparator'):
                columnInfo = column.css(
                    'td.TCol.TColSeparator a::attr(href)').getall()
                if len(columnInfo) > 0 and 'page' not in columnInfo[0] and 'id=1' in columnInfo[0]:
                    matchPage = columnInfo[0]
            yield response.follow(matchPage, callback=self.parse4)
        eventPage = 100
        next_page_link = f'https://www.cagematch.net/en/{URL}&page=4&s={eventPage},'
        while eventPage < 24000:
            yield response.follow(next_page_link, callback=self.parse3, meta={'URL': URL})
            eventPage += 100
            next_page_link = f'https://www.cagematch.net/en/{URL}&page=4&s={eventPage}'

    def parse4(self, response):
        item = WrestlingEventItem()
        eventInfo = response.css('div.InformationBoxTable')
        itemList = ['Promotion', 'EventName', 'Date', 'Type', 'Location', 'Arena', 'Broadcasttype', 'Broadcastdate', 'TVStation', 'Commentators', 'Attendance',
                    'Wrestlers']
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
        yield item
