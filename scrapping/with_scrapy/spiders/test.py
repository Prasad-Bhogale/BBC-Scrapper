#BBC.com scrapping using Scrapy
import scrapy
import re


class scrape_bbc(scrapy.Spider):
    name = "test"

    start_urls = ['https://www.bbc.com']

    def parse(self, response):
        urls = response.css("a.media__link::attr(href)").getall()
        tags = response.css("a.media__tag::text").getall()
        titles = response.css("a.media__link::text").getall()

        titles = [re.sub(r'\s+', ' ', t.strip()) for t in titles]
       
        for url, tag, title in zip(urls, tags, titles):
            if not url.startswith("https://"):
                url = "https://www.bbc.com" + url

            yield Request(url, callback=self.parse_article, cb_kwargs={'url': url, 'tag': tag, 'title': title})

    def parse_article(self, response, url, tag, title):
        image = response.css("meta[property='og:image']::attr(content)").get()

        yield {
            'URL': url,
            'Tag': tag,
            'Title': title,
            'Image': image if "live" not in url else "LIVE" 
        }
