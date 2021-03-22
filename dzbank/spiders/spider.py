import scrapy

from scrapy.loader import ItemLoader

from ..items import DzbankItem
from itemloaders.processors import TakeFirst


class DzbankSpider(scrapy.Spider):
	name = 'dzbank'
	start_urls = ['https://www.dzbank.com/content/dzbank_com/en/home/DZ_BANK/press/News_Archive.html']

	def parse(self, response):
		post_links = response.xpath('//a[@class="btn--link btn--inline"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//section[@class="MCopyText ParBase comp"]/h2[@class="hd"]/text()').get()
		description = response.xpath('//div[@class="rte"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="MNewsPreview tabs comp"]/div/text()').get()

		item = ItemLoader(item=DzbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
