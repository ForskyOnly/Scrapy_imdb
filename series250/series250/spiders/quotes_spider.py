import scrapy


class QuotesSpiderSpider(scrapy.Spider):
    name = "quotes_spider"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        pass


def get_urls():
    urls = []
    url = "https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"
    response = scrapy.Request(url)
    links = response.xpath('//td[@class="titleColumn"]/a/@href')
    for link in links:
        urls.append("https://www.imdb.com" + link.get())
    return urls
