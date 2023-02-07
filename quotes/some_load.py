import json

import scrapy
from itemadapter import ItemAdapter
from scrapy.item import Item, Field
from scrapy.crawler import CrawlerProcess


class QuoteItem(Item):
	author = Field()
	text = Field()
	tags = Field()


class TagItem(Item):
	tag = Field()


class AuthorItem(Item):
	fullname = Field()
	born = Field()
	description = Field()


class SpiderPipline(object):
	quotes = []
	authors = []
	tags = []

	def process_item(self, item, spider):
		adapter = ItemAdapter(item)
		if 'author' in adapter.keys():
			self.quotes.append({
				"model": "quote_app.quote",
				"pk": len(self.quotes) + 1,
				"fields": {
					"text": adapter["text"],
					"author": adapter["author"],
					"tags": adapter["tags"]
				}
			})
		if 'fullname' in adapter.keys():
			self.authors.append({
				"model": "quote_app.author",
				"pk": len(self.authors) + 1,
				"fields": {
					"fullname": adapter["fullname"],
					"born": adapter["born"],
					"description": adapter["description"]
				}
			})
		if 'tag' in adapter.keys():
			self.tags.append(adapter["tag"])
		return item

	def close_spider(self, spider):
		with open('quotes.json', 'w', encoding='utf-8') as fd:
			json.dump(self.quotes, fd, ensure_ascii=False)

		with open('authors.json', 'w', encoding='utf-8') as fd:
			json.dump(self.authors, fd, ensure_ascii=False)

		# clear_tags = [dict(t) for t in {tuple(d.items()) for d in self.tags}]
		clear_tags = list(set(self.tags))
		self.tags = []
		for tag in clear_tags:
			self.tags.append({
				"model": "quote_app.tag",
				"pk": len(self.tags) + 1,
				"fields": {
					"name": tag
				}})

		with open('tags.json', 'w', encoding='utf-8') as fd:
			json.dump(self.tags, fd, ensure_ascii=False)


class Spider(scrapy.Spider):
	name = "my_spider"
	allowed_domains = ['quotes.toscrape.com']
	start_urls = ['http://quotes.toscrape.com/']
	custom_settings = {
		"ITEM_PIPELINES": {
			SpiderPipline: 300,
		}
	}

	def parse(self, response):
		for q in response.xpath('/html//div[@class="quote"]'):
			text = q.xpath('span[@class="text"]/text()').get().strip()
			author = q.xpath('span/small[@class="author"]/text()').get().strip()
			tags = q.xpath('div[@class="tags"]/a[@class="tag"]/text()').extract()
			yield QuoteItem(author=author, text=text, tags=tags)
			yield response.follow(url=self.start_urls[0] + q.xpath('span/a/@href').get(), callback=self.parse_author)
			for tag in tags:
				yield TagItem(tag=tag)

		next_link = response.xpath('/html//li[@class="next"]/a/@href').get()
		if next_link:
			yield scrapy.Request(url=self.start_urls[0] + next_link)

	def parse_author(self, response):
		body = response.xpath('/html//div[@class="author-details"]')
		fullname = body.xpath('h3[@class="author-title"]/text()').get().strip()
		born_date = body.xpath('p/span[@class="author-born-date"]/text()').get().strip()
		born_location = body.xpath('p/span[@class="author-born-location"]/text()').get().strip()
		description = body.xpath('div[@class="author-description"]/text()').get().strip()
		yield AuthorItem(fullname=fullname, born=born_date + " " + born_location, description=description)


def index_tags():
	with open('tags.json', 'r') as f:
		load_tags = json.load(f)
	data_tags = {}
	for item in load_tags:
		data_tags.update({item.get('fields').get('name'): item.get('pk')})
	return data_tags


def index_authors():
	with open('authors.json', 'r') as f:
		load_authors = json.load(f)
	data_authors = {}
	for item in load_authors:
		data_authors.update({item.get('fields').get('fullname'): item.get('pk')})
	return data_authors


def index_quotes():
	with open('quotes.json', 'r') as f:
		data = json.load(f)
	data_authors = index_authors()
	data_tags = index_tags()
	for item in data:
		author = item.get('fields').get('author')
		author = data_authors.get(author)
		item.get('fields')['author'] = author
		tags = item.get('fields').get('tags')
		new_tags = []
		for tag in tags:
			tag = data_tags.get(tag)
			new_tags.append(tag)
		item.get('fields')['tags'] = new_tags
	with open('quotes.json', 'w', encoding='utf-8') as fd:
		json.dump(data, fd, ensure_ascii=False)


if __name__ == '__main__':
	process = CrawlerProcess()
	process.crawl(Spider)
	process.start()
	index_quotes()


