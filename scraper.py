
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
import os
import requests


# Spider class
class ImageSpider(scrapy.Spider):
    name = "image_spider"

    def __init__(self, urls=None, *args, **kwargs):
        super(ImageSpider, self).__init__(*args, **kwargs)
        self.start_urls = urls if urls else []

    def parse(self, response):
        image_urls = response.css('img::attr(src)').getall()
        image_urls = [response.urljoin(url) for url in image_urls]

        # Extract chapter number and pad to 3 digits
        chapter_number = response.url.rstrip('/').split('-')[-1].zfill(3)

        # Manual download
        download_images(image_urls, chapter_number)

        # Yield items for Scrapy pipeline
        for idx, image_url in enumerate(image_urls, start=1):
            yield {
                'image_urls': [image_url],
                'chapter': chapter_number,
                'page': str(idx).zfill(3)
            }


# Image pipeline
class ImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            request = scrapy.Request(image_url)
            request.meta['chapter'] = item.get('chapter')
            request.meta['page'] = item.get('page')
            yield request

    def file_path(self, request, response=None, info=None, *, item=None):
        chapter = request.meta['chapter']
        page = request.meta['page']
        filename = f"{page}{chapter}.png"
        return f'downloaded_images/{filename}'


# Manual image download function
def download_images(image_urls, chapter_number):
    save_dir = os.path.join(os.getcwd(), 'downloaded_images')
    os.makedirs(save_dir, exist_ok=True)
    for idx, url in enumerate(image_urls, start=1):
        try:
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                page_number = str(idx).zfill(3)
                filename = f"{chapter_number}{page_number}.png"
                image_path = os.path.join(save_dir, filename)
                with open(image_path, 'wb') as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                print(f"Downloaded: {image_path}")
            else:
                print(f"Failed to download: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {e}")


# Scrapy settings
settings = get_project_settings()
settings.set('ITEM_PIPELINES', {'__main__.ImageDownloadPipeline': 1})
settings.set('IMAGES_STORE', os.path.join(os.getcwd(), 'downloaded_images'))


# Run spider on multiple chapters
def run_spider_multiple_chapters(base_url, start_chapter=1, end_chapter=200):
    urls = [f"{base_url}{i}/" for i in range(start_chapter, end_chapter + 1)]
    process = CrawlerProcess(settings)
    process.crawl(ImageSpider, urls=urls)
    process.start()


# Start the spider
if __name__ == "__main__":
    run_spider_multiple_chapters("https://www.manwha-sololeveling.com/manga/solo-leveling-chapter-")
