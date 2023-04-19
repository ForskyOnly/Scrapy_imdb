import scrapy
from ..items import ImdbData
import csv


class ImdbSpider(scrapy.Spider):
    name = "IMDB"
    start_urls = ["https://www.imdb.com/chart/toptv/?ref_=nv_tvv_250"]

    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

    def get_urls(self, response):
        urls = []
        links = response.xpath('//td[@class="titleColumn"]/a/@href')
        for link in links:
            urls.append("https://www.imdb.com" + link.get())
        return urls

    def parse(self, response):
        urls = self.get_urls(response)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_item)

    def write_csv(self, item):
        with open('best250tvshow.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['titre', 'titre_origine', 'score', 'genre', 'annee', 'saisons', 'episodes', 'duree', 'description', 'acteurs', 'public', 'pays']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'titre': item['titre'],
                'titre_origine': item['titre_origine'],
                'score': item['score'],
                'genre': item['genre'],
                'annee': item['annee'],
                'saisons': item['saisons'],
                'episodes': item['episodes'],
                'duree': item['duree'],
                'description': item['description'],
                'acteurs': item['acteurs'],
                'public': item['public'],
                'pays': item['pays']
            })



    def parse_item(self, response):
        items = ImdbData()
        items['titre'] = response.xpath('//section/section/div[2]/div[1]/h1/span/text()').get()
        items['titre_origine'] = response.xpath('//section/section/div[2]/div[1]/div/text()').get()
        items['score'] = response.xpath('//span/div/div[2]/div[1]/span[1]/text()').get()
        items['genre'] = response.xpath('//a[@class="ipc-chip ipc-chip--on-baseAlt"]/span/text()').getall()
        items['saisons'] = response.xpath("//label[@for='browse-episodes-season']/text()").get()
        items['saisons'] = items["saisons"][:-8] if items['saisons'] else '1'
        items['episodes'] = response.css("[data-testid='episodes-header'] span.ipc-title__subtext::text").get()
        items['annee'] = response.xpath('//section/section/div[2]/div[1]/ul/li[2]/a/text()').get()
        items['duree'] = response.xpath('//section/div[3]/section/section/div[2]/div[1]/ul/li[4]/text()').get()
        items['description'] = response.xpath('//section/p/span[2]/text()').get()
        items['acteurs'] = response.css('.sc-52d569c6-3 .ipc-metadata-list-item--link a.ipc-metadata-list-item__list-content-item::text').getall()
        items['public'] = response.xpath('//section/div[3]/section/section/div[2]/div[1]/ul/li[3]/a/text()').get()
        items['pays'] = response.css("[data-testid='title-details-origin'] a::text").get()
        self.write_csv(items)



            
