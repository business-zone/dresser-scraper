import scrapy


class DressersSpider(scrapy.Spider):
    name = "dressers"

    def start_requests(self):
        with open("urls.txt", "r") as file:
            urls = [url.rstrip() for url in file]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        name = response.css("h1.m-typo.m-typo_primary.is-full::text").get()
        if not name:
            name = response.css("h1.m-typo.m-typo_primary::text").get()
        yield {
            "name": name,
            "price": response.css("div.m-priceBox_price.m-priceBox_promo::text").get().replace(",-", "")
        }
