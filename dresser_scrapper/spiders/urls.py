import scrapy


class URLsSpider(scrapy.Spider):
    name = "urls"

    def start_requests(self):
        PAGE_URL = "https://www.agatameble.pl/meble/przechowywanie/komody?page={}"
        with open("pages_number.txt", "r") as file:
            pages_number = file.read()
        for page in range(int(pages_number)):
            yield scrapy.Request(url=PAGE_URL.format(str(page)), callback=self.parse)

    def parse(self, response):
        for dresser in response.css("div.m-offerBox_name"):
            dresser_url = f"https://www.agatameble.pl{dresser.css('a').attrib['href']}"
            with open("urls.txt", "a") as file:
                file.write(f"{dresser_url}\n")
