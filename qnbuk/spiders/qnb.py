import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from qnbuk.items import Article


class QnbSpider(scrapy.Spider):
    name = 'qnb'
    start_urls = ['https://www.qnb.com/sites/qnb/qnbglobal/page/en/ennews.html']

    def parse(self, response):
        links = response.xpath('//div[@class="title"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="page-subpage-content"]//text()').getall()
        content = [text for text in content if text.strip()]
        date = " ".join(content.pop(0).strip().split()[-3:])
        if date:
            date = datetime.strptime(date, '%d %b %Y')
            date = date.strftime('%Y/%m/%d')

        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
