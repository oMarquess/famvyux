import scrapy
import re

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?groups=top_1000&count=250&sort=user_rating,asc"]

    def start_requests(self):
        """
        Generates the initial request to scrape the IMDb top chart page.

        Returns:
            scrapy.Request: The initial request object with the specified URL, callback function, headers, and cookies.
        """
        url = "https://www.imdb.com/search/title/?groups=top_1000&count=250&sort=user_rating,asc"

        self.cookies = {
            "__zlcmid": "1IcmEsVswE4IEC5",
            "sucuri_cloudproxy_uuid_ada8ef2a2": "eb7ce14f2e4fa718f19aa0a774751c7a",
            "PHPSESSID": "9vamo2en014n0uhilfmdcms46k",
            "form_key": "y0uBYKU1VoPlbRab",
            "mage-cache-storage": "%7B%7D",
            "mage-cache-storage-section-invalidation": "%7B%7D",
            "mage-cache-sessid": "true",
            "searchsuiteautocomplete": "%7B%7D",
            "mage-messages": "",
            "recently_viewed_product": "%7B%7D",
            "recently_viewed_product_previous": "%7B%7D",
            "recently_compared_product": "%7B%7D",
            "recently_compared_product_previous": "%7B%7D",
            "product_data_storage": "%7B%7D",
            "section_data_ids": "%7B%22cart%22%3A1698913496%7D",
            "amp_6e403e": "GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0",
        }

        #uncomment the appropraite referer for the set category
        self.headers = {
            "authority": "https://www.imdb.com/chart/top/",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            # 'cookie': '__zlcmid=1IcmEsVswE4IEC5; sucuri_cloudproxy_uuid_ada8ef2a2=eb7ce14f2e4fa718f19aa0a774751c7a; PHPSESSID=9vamo2en014n0uhilfmdcms46k; form_key=y0uBYKU1VoPlbRab; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; searchsuiteautocomplete=%7B%7D; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22cart%22%3A1698913496%7D; amp_6e403e=GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0',
            "dnt": "1",
            "pragma": "no-cache",
            "referer": "https://www.imdb.com/chart/top/",
            "sec-ch-ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"macOS"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        }
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            headers=self.headers,
            cookies=self.cookies,
        )     
    def parse(self, response):
        for movie in response.css("li.ipc-metadata-list-summary-item"):
            yield {
                #"title": movie.css(".ipc-title__text::text").get().strip("."),
                "title": re.sub(r"^\d+\.\s*", "", movie.css(".ipc-title__text::text").get()).strip("."),
                "year": movie.css(".dli-title-metadata-item::text").get(),
                "imdb_rating": self.extract_rating(movie, "IMDb rating: (\d+.\d+)"),
                #"rating_count": self.extract_rating(movie, r"\((\d+[.,]?\d*)\)"),
                "metascore": movie.css(".metacritic-score-box::text").get(),
                "image_url": movie.css(".ipc-image::attr(src)").get(),
                "description": movie.css(".ipc-html-content-inner-div::text").get().strip(),
            }

    @staticmethod
    def extract_rating(movie, pattern):
        match = re.search(pattern, movie.css(".dli-ratings-container").get())
        return match.group(1) if match else None
