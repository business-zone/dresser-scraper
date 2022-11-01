# Dresser Scrapper

## About

Scraps dresser names and dresser page URLs from [Salony Agata](https://www.agatameble.pl/).

This data is used in a [PrestaShop](https://www.prestashop.com/) website as a part of Electronic Business studies course.

## Prerequisites

You need to install [Scrapy](https://scrapy.org/):
```sh
pip install scrapy
```

## Usage
### Commands
To run the scrapper use:
```sh
scrapy crawl pages_number | scrapy crawl dresser_names
```
### Output
data.csv — contains dresser names and dedicated page URLs.
