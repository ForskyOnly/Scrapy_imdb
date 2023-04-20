# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImdbData(scrapy.Item):
    titre = scrapy.Field()
    titre_origine = scrapy.Field()
    score = scrapy.Field()
    genre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    public = scrapy.Field()
    pays = scrapy.Field()
    saisons = scrapy.Field()
    episodes = scrapy.Field()
    categorie = scrapy.Field()