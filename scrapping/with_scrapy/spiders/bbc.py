import scrapy
import re

class scrape_bbc(scrapy.Spider):
    name = "extract"

    start_urls = ['https://www.bbc.com']

    def parse(self, response):
        url = response.css("a.media__link::attr(href)").getall()
        tag = response.css("a.media__tag::text").getall()
        title = response.css("a.media__link::text").getall()

        title = [re.sub(r'\s+', ' ', t.strip()) for t in title]
        image_urls = response.css('img::attr(src)').getall()


       
        for url, tag, title, image_url in zip(url, tag, title, image_urls):

            if not url.startswith("https://"):
                url = "https://" + url
                
            yield{
                'URL' : url,
                'Tag' : tag,
                'Title' : title,
                'image_url' : image_url
            }     
