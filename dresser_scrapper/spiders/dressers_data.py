import scrapy
import random
import re


class DressersSpider(scrapy.Spider):
    name = "dressers"

    def start_requests(self):
        MAIN_URL = "https://www.agatameble.pl/meble/przechowywanie/komody"
        yield scrapy.Request(url=MAIN_URL, callback=self.parse)

    def parse(self, response):
        style_filter = response.css("div.m-filters_singleWrapper.is-TEXT.is-filterList_1").css('#js-filters_list3-1')
        for style in style_filter.css('span.m-filters_txt.is-customCheckbox_inp.js-checkSubmit::text'):
            style_name = style.get().lower().replace(" ", "").replace("ł", "l")
            style_url = f"https://www.agatameble.pl/meble/przechowywanie/komody/styl:{style_name}"
            yield scrapy.Request(url=style_url, callback=self.parse_style, meta={'category': style_name})

    def parse_style(self, response):
        pages_number = response.css("span.m-pagination_count::text").get().replace("z ", "")
        for page in range(1, int(pages_number) + 1):
            page_url = response.request.url + f"?page={str(page)}"
            yield scrapy.Request(url=page_url, callback=self.parse_urls, meta={'category': response.meta["category"]})

    def parse_urls(self, response):
        for dresser in response.css("div.m-offerBox_name"):
            dresser_url = f"https://www.agatameble.pl{dresser.css('a').attrib['href']}"
            yield scrapy.Request(url=dresser_url, callback=self.parse_dresser,
                                 meta={'category': response.meta["category"]})

    def parse_dresser(self, response):
        if name := response.css("h1.m-typo.m-typo_primary.is-full::text"):
            name = name.get().replace('"', "").strip()
        else:
            name = response.css("h1.m-typo.m-typo_primary::text").get().replace('"', "").strip()
        price = response.css("div.m-priceBox_price.m-priceBox_promo::text").get().replace("-", "").replace('"', "").strip()
        category = f"Styl {response.meta['category']}"
        description = response.css("div.widget.text_editor").getall()[1]
        # if description := response.css("div.widget.text_editor.clearfix2").getall():
        #     description = description[1] if len(description) == 2 else description[0]
        tagless_description = re.sub("<[^>]+>", " ", description)
        description = ' '.join(tagless_description.split()).strip().replace('"', "")
        img_urls = ""
        for img in response.css("div#js-offerGallery.m-offerGallery_wrap").css("div.m-offerGallery_item.js-thumbs"):
            img_url_part = img.css("img.m-offerGallery_picture").attrib['src']
            img_urls += f"https://www.agatameble.pl{img_url_part}, "
        img_urls = re.sub(", $", "", img_urls)
        active = 1
        tax_rule_id = 1
        quantity = random.randint(1, 100)
        yield {
            "Active (0/1)": active,
            "Name": name,
            "Categories (x,y,z...)": category,
            "Price tax included": price,
            "Tax rule ID": tax_rule_id,
            "Quantity": quantity,
            "Description": description,
            "Image URLs (x,y,z...)": img_urls
        }
