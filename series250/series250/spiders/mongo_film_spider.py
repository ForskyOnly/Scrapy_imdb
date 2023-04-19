from dotenv import load_dotenv
import os 
from pymongo import MongoClient
import scrapy
from ..items import ImdbData

load_dotenv()

MONGODB_PWD = os.environ.get("MONGODB_PWD")
MANGODB_PSEUDO = os.environ.get("MANGODB_PSEUDO")
MONGODB_DB = 'imdb_data'
MONGODB_COLLECTION = 'films_series'

connection_todb = f"mongodb+srv://forskyonly:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_todb)


def hours_to_min(duree):
        if 'h' in duree and 'm' in duree:
            heure, minute = duree.split("h ")
            heure = int(heure)
            minute = int(minute.replace("m", ""))
        elif 'h' in duree:
            heure = int(duree.replace("h", ""))
            minute = 0
        elif 'm' in duree:
            heure = 0
            minute = int(duree.replace("m", ""))
        else:
            raise ValueError()
        duree_minutes = heure * 60 + minute
        return duree_minutes

class ImdbSpider(scrapy.Spider):
    name = "imdbtomongo"
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
        if items['duree'] is not None:
            items['duree'] = hours_to_min(items['duree'])
        
       
        items_data = {
                
                'titre': items['titre'],
                'titre_origine': items['titre_origine'],
                'score': items['score'],
                'genre': items['genre'],
                'annee': items['annee'],
                'duree': items['duree'],
                'description': items['description'],
                'acteurs': items['acteurs'],
                'public': items['public'],
                'pays': items['pays']
        }



        client = MongoClient(f'mongodb+srv://{MANGODB_PSEUDO}:{MONGODB_PWD}@cluster1.rdzhoip.mongodb.net/{MONGODB_DB}')
        db = client[MONGODB_DB]
        collection = db[MONGODB_COLLECTION]
        
        collection.insert_one(items_data)
