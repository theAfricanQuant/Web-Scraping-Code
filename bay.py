# -*- coding: utf-8 -*-
import scrapy

n = 3
#identifying the website that is gonna be scraped
class BaySpider(scrapy.Spider):
    name = 'bay'
    allowed_domains = ['www.thebay.com']
    start_urls = ['https://www.thebay.com/search/EndecaSearch.jsp?N=1553+302023689']

    #loop through every item grabbing the data we want
    def parse(self, response):
        global n
        i = 3
        ii = str(i)
        box = response.xpath("//div[@id = 'product-container']/div[@id]/div[@class = 'product-text']")
        for boxes in box:
            link = boxes.xpath(
                f"(//div[@id = 'product-container']/div[@id]/div)[{ii}]/a/@href"
            ).get()
            price = boxes.xpath(
                f"(//div[@id = 'product-container']/div[@id]/div)[{ii}]/a/span[@class = 'product-price line-through']/text()"
            ).get()
            sale = boxes.xpath(
                f"((//div[@id = 'product-container']/div[@id]/div)[{ii}]/a/span)[2]/span[@class = 'product-sale-price']/text()"
            ).get()
            brand = boxes.xpath(
                f"(//div[@id = 'product-container']/div[@id]/div)[{ii}]/a/p/span/text()"
            ).get()
            clothing = boxes.xpath(
                f"((//div[@id = 'product-container']/div[@id]/div)[{ii}]/a/p)[2]/text()"
            ).get()
            i  = i + 3
            ii = str(i)

            if len(price) <10 and len(sale) <10:
                price_int = price.replace('$', '')
                price_int = float(price_int)
                sale_int = sale.replace('$','')
                sale_int = float(sale_int)
                discount = ((price_int - sale_int)/price_int)*100
                discount = str(discount)
            else:
                discount = 'Unknown'

            yield {
                'link': link,
                'Brand': brand,
                'clothing': clothing,
                'Original Price': price,
                'Sale Price': sale,
                'discount': f'{discount}%',
            }

        n+= 1
        nn = str(n)
        print (n)
        next_page = response.xpath(f"((//ol)[2]/li)[{nn}]/a/@href").get()
        print(next_page)
        #go to the next page when done with the current one
        if next_page:
            yield scrapy.Request(
                url=f'https://thebay.com{next_page}',
                callback=self.parse,
                dont_filter=True,
            )
            
    
b = '2800.00'
c = float(b)
len(b)
