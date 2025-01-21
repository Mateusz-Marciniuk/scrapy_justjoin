import scrapy
import requests
len_link = 1
class LinkSpider(scrapy.Spider):
    name = "link"
    
    start_urls = [
        'https://justjoin.it/job-offers/slask?orderBy=DESC&sortBy=newest&from=500&itemsCount=100',
    ]

    def start_requests(self):
        base_url = 'https://justjoin.it/job-offers/slask?orderBy=DESC&sortBy=newest&from={}&itemsCount=100'
        offset = 0
        
        
        while True and len_link > 0:
            url = base_url.format(offset)
            if requests.get(url).status_code == 200:
                yield scrapy.Request(url=url, callback=self.parse)
                offset += 100
            else:
                break

        
    def parse(self, response):
        global len_link
        len_link = len(response.css('a[target="_parent"]::attr(href)').getall())
        links = response.css('a[target="_parent"]::attr(href)').getall()
        for link in links:
            absolute_url = response.urljoin(link)
            print(absolute_url)
            yield scrapy.Request(url=absolute_url, callback=self.parse_offer)

            # yield {
            #     "link": absolute_url
            # }
    def parse_offer(self, response):
        # Wyciąganie umiejętności z oferty
        skills = response.css('h4.MuiTypography-root.MuiTypography-subtitle2.css-b849nv::text').getall()
        
        print(skills)
        yield {
            'skills': skills,
            
        }