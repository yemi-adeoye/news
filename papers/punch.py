import requests
from bs4 import BeautifulSoup as bs
import json


class Punch():

    def __init__(self, path_to_config, path_to_keywords, path_to_cache):

        self.path_to_config = path_to_config
        self.path_to_keywords = path_to_keywords
        self.path_to_cache = path_to_cache

        try:
            with open(path_to_config) as config_json:
                self.config = json.load(config_json)

            with open(path_to_keywords) as keywords_json:
                self.keywords = json.load(keywords_json)

            with open(path_to_cache) as cache_json:
                self.cache = json.load(cache_json)

        except IOError as io_except:
            print("Error reading file \n", io_except)
        except Exception as ex:
            print("something went wrong")
            print(ex)

    def request(self, urls=None):
        news_accumulator = ''
        if not urls:
            urls = self.config["URLS"]

        for url in urls:
            req = requests.get(url)
            news_accumulator += req.text
        return news_accumulator

    def soupify(self, news_html, parser='html.parser'):
        self.soup = bs(news_html, parser)
        return self.soup

    def find_all_hrefs(self, ):
        self.all_hrefs = set()
        for href in self.soup.select(self.config["TAG"]):
            self.all_hrefs.add(href.attrs['href'])
        return self.all_hrefs

    def subtract_cache(self, ):
        cache = set(self.cache["cache"])
        self.current_hrefs = self.all_hrefs - cache
        return self.current_hrefs

    def update_cache(self, ):
        cache = {"cache": list(self.all_hrefs)}

        try:
            with open(self.path_to_cache, 'w') as cache_json:
                x = json.dump(cache, cache_json)
        except IOError:
            print("Error writing to file")
        except Exception as ex:
            print("Something went wrong" + str(ex))

        return True

    def get_relevant_news(self, ):
        self.relevant_news = set()
        for keyword in self.keywords["keywords"]:
            for headline in self.all_hrefs:
                if headline.lower().find(keyword.lower()) != -1:
                    self.relevant_news.add(headline)
        return self.relevant_news

    def get_full_news(self, ):
        accumulator = ''
        for story in self.relevant_news:
            raw = self.request([story])
            soup = self.soupify(raw)

            headline = soup.select(self.config["HEADLINE"])
            print(headline)
            author = soup.select(
                self.config["AUTHOR"]) if self.config["AUTHOR"] else ''
            published = soup.select(self.config["DATE"])

            author = author[0].getText().strip() if author else ''

            if headline:
                accumulator += self.config["TITLE"] + \
                    ': ' + headline[0].getText() + "\n"

            accumulator += (author.strip() + "\n") if author else ''

            if published:
                accumulator += published[0].getText().strip() + "\n"

            '''unwanted = soup.extract('div.read-also')
            unwanted = soup.extract('p div')
            unwanted = soup.extract('div.ad-container')'''

            # soup.unwanted.extract()  # .exclude(unwanted)

            body = soup.select(self.config["PARAGRAPHS"])

            for p in body:
                accumulator += p.getText() + "\n"
            accumulator = accumulator.strip() + "\n\n"

        return accumulator
