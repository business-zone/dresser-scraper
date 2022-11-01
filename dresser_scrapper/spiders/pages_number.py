import scrapy


class PagesNumberSpider(scrapy.Spider):
    name = "pages_number"

    def start_requests(self):
        MAIN_URL = "https://www.agatameble.pl/meble/przechowywanie/komody"
        yield scrapy.Request(url=MAIN_URL, callback=self.parse)

    def parse(self, response):
        pages_number = response.css("span.m-pagination_count::text").get().replace("z ", "")
        with open("pages_number.txt", "w") as file:
            file.write(pages_number)
