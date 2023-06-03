import scrapy
import pandas as pd

class MySpider(scrapy.Spider):
    name = "UNSpider"
    start_urls = [
        "https://repositorio.unal.edu.co/handle/unal/1/browse?type=subject&value=0+Generalidades+%2F+Computer+science%2C+information++and++general+works"
    ]
    
    texts=[]
    links=[]
    
   

    def parse(self, response):

    
        urlNextPage = "https://repositorio.unal.edu.co/handle/unal/1/"
        button = response.css('a.next-page-link::attr(href)').get()
        nextUrl = urlNextPage+button

        texts_response = response.css('h4 a::text').getall()
        links_response = response.css('h4 a::attr(href)').getall()
        
        for i in texts_response:
            self.texts.append(i)
        for i in links_response:
            self.links.append('https://repositorio.unal.edu.co'+ i)
        
        request = scrapy.Request(
        nextUrl,
        callback=self.parse_page2,
        errback=self.errback_page2,
        cb_kwargs=dict(main_url=response.url))
        
        yield request
        
        
    def parse_page2(self, response, main_url):
        
        urlNextPage = "https://repositorio.unal.edu.co/handle/unal/1/"
        button = response.css('a.next-page-link::attr(href)').get()
        
        texts_response = response.css('h4 a::text').getall()
        links_response = response.css('h4 a::attr(href)').getall()
        
        for i in texts_response:
            self.texts.append(i)
        for i in links_response:
            self.links.append('https://repositorio.unal.edu.co' + i)
        
        
        if button != '':
            nextUrl = urlNextPage+button
            
            request = scrapy.Request(
            nextUrl,
            callback=self.parse_page2,
            errback=self.errback_page2,
            cb_kwargs=dict(main_url=response.url))
            
            
            yield request
        else:
            
            data = {'Link': self.links, "Title": self.texts}
            df = pd.DataFrame(data)
            df.to_excel('datos.xlsx', index=False)



    def errback_page2(self, failure):
        yield dict(
            main_url=failure.request.cb_kwargs["main_url"],
        )
        