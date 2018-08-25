import scrapy


class BookSpider(scrapy.Spider):
    name = 'bookt'

    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        # follow links to author pages
        for href in response.xpath('//a[@title]'):
             yield response.follow(href, self.parse_deal)

        # follow pagination links
        for href in response.css('li.next a::attr(href)'):
                yield response.follow(href, self.parse)

    def parse_deal(self, response):
        def extract_with_css(query):
            return response.xpath(query).extract_first().strip()
        stock=(extract_with_css('/html/body/div[1]/div/div[2]/div[2]/article/div[1]/div[2]/p[2]')[84:86])

        if int(stock) < 12 :
            yield {
            'name' : extract_with_css('//a[@title]/text()'),
            'stock': stock,
            }
