import scrapy
# from scrapy import Spider
# from scrapy import Request
# from scrapy.crawler import CrawlerProcess

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css('article.product_pod')

        for book in books:
            yield {  # Yield is like a return function
                'name': book.css('h3 a::text').get(),  # .class::type
                'price': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href'],
            }

        next_page = response.css('li.next a ::attr(href)').get()  # Going through all the next pages

        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_page_url, callback=self.parse)

    
    def parse_book_page(self, response):
    
        table_rows = response.css('table tr')  # Getting the table information for a given book

        yield {
            'url': response.url,
            'title': response.css('.product_main h1::text').get(),
            'product_type': table_rows[1].css("td ::text").get(),
            'price_excl_tax': table_rows[2].css("td ::text").get(),
            'price_incl_tax': table_rows[3].css("td ::text").get(),
            'tax': table_rows[4].css("td ::text").get(),
            'availability': table_rows[5].css("td ::text").get(),
            'num_reviews': table_rows[6].css("td ::text").get(),
            'stars': response.css("p.star-rating").attrib['class'],
            'category': response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
            'description': response.xpath("//div[@id='product_description']/following-sibling::p/text()").get(),
            'price': response.css('p.price_color ::text').get(),
        }

# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(BookspiderSpider)
#     process.start()