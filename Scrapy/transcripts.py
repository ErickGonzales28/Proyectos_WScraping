from typing import Iterable

import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    #start_urls = ["https://subslikescript.com/movies_letter-X"]

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    def start_requests(self):
        yield scrapy.Request(url='https://subslikescript.com/movies_letter-X', headers={
            'user-agent':self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]/li/a')), callback="parse_item", follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths=('(//a[@rel="next"])[1]')),process_request='set_user_agent')
    )

    def set_user_agent(self,request, spider):
        request.headers['User-Agent']=self.user_agent
        return request

    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        transcript_lista = article.xpath('./div[@class="full-script"]/text()').getall()
        transcript_string = ' '.join(transcript_lista)
        yield {
            'title': article.xpath("./h1/text()").get(),
            'plot': article.xpath("./p/text()").get(),
            'transcript': transcript_string,
            'url': response.url,
            #'User-Agent': response.request.headers['User-Agent']
        }