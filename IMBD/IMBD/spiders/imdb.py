import scrapy
import re

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/"]

    def start_requests(self):
        url = "https://www.imdb.com/chart/top/"

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
        # Loop through each movie item
        for movie in response.css('li.ipc-metadata-list-summary-item'):
            # Extract data using CSS selectors
            #title = movie.css('h3.ipc-title__text::text').get()
            title_with_number = movie.css('td.titleColumn a::text').get()
            title = re.sub(r'^\d+\.\s+', '', title_with_number)  # Remove numbering
            image_url = movie.css('div.ipc-media--poster-27x40 img::attr(src)').get()
            year = movie.css('span.cli-title-metadata-item::text').get()
            duration = movie.css('span.cli-title-metadata-item::text').getall()[1]
            # Extracting star rating number and vote count
            star_rating = movie.css('span.ipc-rating-star--imdb.ratingGroup--imdb-rating::text').get()
            # Extracting rate count
            rate_count = movie.css('span.ipc-rating-star--voteCount::text').get().strip('() ')
            # Extract product URL
            #product_url = response.urljoin(movie.css('a.ipc-title-link-wrapper::attr(href)').get())
            

            # Yield a dictionary with the scraped data
            yield {
                'title': title,
                'image_url': image_url,
                'year': year,
                'duration': duration,
                'star_rating': star_rating,
                'rate_count': rate_count,
                #'product_url': product_url
            }
        


# import scrapy
# import re

# class ImdbSpider(scrapy.Spider):
#     name = "imdb"
#     allowed_domains = ["www.imdb.com"]
#     start_urls = ["https://www.imdb.com/chart/top/"]

#     def start_requests(self):
#         url = "https://www.imdb.com/chart/top/"
#         # ... [Your existing cookies and headers code] ...
#         self.cookies = {
#             "__zlcmid": "1IcmEsVswE4IEC5",
#             "sucuri_cloudproxy_uuid_ada8ef2a2": "eb7ce14f2e4fa718f19aa0a774751c7a",
#             "PHPSESSID": "9vamo2en014n0uhilfmdcms46k",
#             "form_key": "y0uBYKU1VoPlbRab",
#             "mage-cache-storage": "%7B%7D",
#             "mage-cache-storage-section-invalidation": "%7B%7D",
#             "mage-cache-sessid": "true",
#             "searchsuiteautocomplete": "%7B%7D",
#             "mage-messages": "",
#             "recently_viewed_product": "%7B%7D",
#             "recently_viewed_product_previous": "%7B%7D",
#             "recently_compared_product": "%7B%7D",
#             "recently_compared_product_previous": "%7B%7D",
#             "product_data_storage": "%7B%7D",
#             "section_data_ids": "%7B%22cart%22%3A1698913496%7D",
#             "amp_6e403e": "GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0",
#         }

#         #uncomment the appropraite referer for the set category
#         self.headers = {
#             "authority": "https://www.imdb.com/chart/top/",
#             "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
#             "accept-language": "en-US,en;q=0.9",
#             "cache-control": "no-cache",
#             # 'cookie': '__zlcmid=1IcmEsVswE4IEC5; sucuri_cloudproxy_uuid_ada8ef2a2=eb7ce14f2e4fa718f19aa0a774751c7a; PHPSESSID=9vamo2en014n0uhilfmdcms46k; form_key=y0uBYKU1VoPlbRab; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; searchsuiteautocomplete=%7B%7D; mage-messages=; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; section_data_ids=%7B%22cart%22%3A1698913496%7D; amp_6e403e=GrbSqKvpyV0ybbzub0DTx-...1he7i4jaf.1he7i5cl2.0.0.0',
#             "dnt": "1",
#             "pragma": "no-cache",
#             "referer": "https://www.imdb.com/chart/top/",
#             "sec-ch-ua": '"Not=A?Brand";v="99", "Chromium";v="118"',
#             "sec-ch-ua-mobile": "?0",
#             "sec-ch-ua-platform": '"macOS"',
#             "sec-fetch-dest": "document",
#             "sec-fetch-mode": "navigate",
#             "sec-fetch-site": "same-origin",
#             "sec-fetch-user": "?1",
#             "upgrade-insecure-requests": "1",
#             "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
#         }
#         yield scrapy.Request(
#             url=url,
#             callback=self.parse,
#             headers=self.headers,
#             cookies=self.cookies,
#         )

#     def parse(self, response):
#         # Loop through each movie item
#         for movie in response.css('li.ipc-metadata-list-summary-item'):
#             # Extract data using CSS selectors
#             title_with_number = movie.css('h3.ipc-title__text::text').get()
#             # Use regular expression to remove numbering
#             title = re.sub(r'^\d+\.\s+', '', title_with_number)
#             image_url = movie.css('td.posterColumn img::attr(src)').get()
#             year = movie.css('td.titleColumn span.secondaryInfo::text').get()
#             star_rating = movie.css('td.imdbRating strong::text').get()

#             # Extract movie URL
#             movie_url = response.urljoin(movie.css('td.titleColumn a::attr(href)').get())

#             # Yield a request to the movie page, passing the current extracted data
#             yield scrapy.Request(movie_url, callback=self.parse_movie, meta={
#                 'title': title,
#                 'image_url': image_url,
#                 'year': year,
#                 'star_rating': star_rating
#             })

#     def parse_movie(self, response):
#         # Extract storyline
#         storyline = response.css('div.ipc-overflowText--children div.ipc-html-content-inner-div::text').get()

#         # Extract duration
#         duration = response.css('ul.ipc-inline-list li.ipc-inline-list__item::text').get()

#         # Yield the final data including the storyline and duration
#         yield {
#             'title': response.meta['title'],
#             'image_url': response.meta['image_url'],
#             'year': response.meta['year'],
#             'star_rating': response.meta['star_rating'],
#             'duration': duration,
#             'storyline': storyline
#         }
