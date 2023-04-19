import scrapy
from ..items import ImdbData
import csv


class ImdbSpider(scrapy.Spider):
    name = "IMDBfilm"
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

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
        with open('best250movies.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['titre', 'titre_origine', 'score', 'genre', 'annee', 'duree', 'description', 'acteurs', 'public', 'pays']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'titre': item['titre'],
                'titre_origine': item['titre_origine'],
                'score': item['score'],
                'genre': item['genre'],
                'annee': item['annee'],
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
        items['annee'] = response.css('.sc-afe43def-4 li:nth-of-type(1) a::text').get()
        items['duree'] = response.css('.sc-afe43def-4 li:nth-of-type(3)::text').get()
        items['description'] = response.xpath('//section/p/span[2]/text()').get()
        items['acteurs'] = response.css('.sc-52d569c6-3 .ipc-metadata-list-item--link a.ipc-metadata-list-item__list-content-item::text').getall()
        items['public'] = response.css('.sc-afe43def-4 li:nth-of-type(2) a::text').get()
        items['pays'] = response.css("[data-testid='title-details-origin'] a::text").get()
        self.write_csv(items)



            
