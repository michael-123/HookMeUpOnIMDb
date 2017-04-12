from util import download_html_for_ids
from util import URLS
from util import get_html_code_from_path
from lxml import html

from settings import *


class API(object):
    def fetch_title(self):
        xpath = '//div[@class="title_wrapper"][1]/h1/text()[1]'
        title = self.get_tree().xpath(xpath)[0]
        self.title = title.replace("\r", "").replace("\n", "").strip()

    def fetch_year(self):
        xpath = '//span[@id="titleYear"][1]/a/text()'
        year = self.get_tree().xpath(xpath)[0]
        self.year = year

    def fetch_rating(self):
        xpath = '//span[@itemprop="ratingValue"][1]/text()'
        rating = self.get_tree().xpath(xpath)[0]
        self.rating = rating.replace(",", ".")

    def fetch_number_of_ratings(self):
        xpath = '//span[@itemprop="ratingCount"][1]/text()'
        number = self.get_tree().xpath(xpath)[0]
        self.number_of_ratings = number.replace(",", "").replace(".", "").strip()

    def fetch_genres(self):
        xpath = '//h4[@class="inline"][contains(text(), "Genres:")]/following-sibling::a/text()'
        genres = self.get_tree().xpath(xpath)
        self.genres = [genre.strip() for genre in genres]

    def fetch_countries(self):
        xpath = '//h4[@class="inline"][contains(text(), "Country:")]/following-sibling::a/text()'
        countries = self.get_tree().xpath(xpath)
        self.countries = countries

    def fetch_duration(self):
        xpath = '//h4[@class="inline"][contains(text(), "Runtime:")]/following-sibling::time/text()'
        duration = self.get_tree().xpath(xpath)[0]
        self.duration = duration.replace("min", "").strip()

    def fetch_content_rating(self):
        xpath = '//meta[@itemprop="contentRating"]/@content'
        self.content_rating = self.get_tree().xpath(xpath)[0]

    def fetch_description(self):
        xpath = '//div[@itemprop="description"]/p/text()'
        description = self.get_tree().xpath(xpath)[0]
        self.description = description.strip().replace("\n", "").replace("\r", "")

    def fetch_metascore(self):
        xpath = '//div[contains(@class, "metacriticScore")]/span/text()'
        metascore = self.get_tree().xpath(xpath)[0]
        self.metascore = metascore

    def fetch_keywords(self):
        xpath = '//h4[@class="inline"][contains(text(), "Plot Keywords:")]/following-sibling::a/span/text()'
        keywords = self.get_tree().xpath(xpath)
        self.keywords = keywords

    def fetch_number_of_critics(self):
        xpath = '//div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a/text()[contains(., "critic")]'
        critics = self.get_tree().xpath(xpath)[0]
        self.number_of_critics = critics.replace(" critic", "").replace(",", "").strip()

    def fetch_number_of_user_reviews(self):
        xpath = '//div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a/text()[contains(., "user")]'
        user_reviews = self.get_tree().xpath(xpath)[0]
        self.number_of_user_reviews = user_reviews.replace(" user", "").replace(",", "").strip()

    def fetch_release_date_us(self):
        xpath = '//div[@class="title_wrapper"][1]//meta[@itemprop="datePublished"][1]/@content[1]'
        release_date_us = self.get_tree().xpath(xpath)
        self.release_date_us = release_date_us[0]

    def fetch_languages(self):
        xpath = '//h4[@class="inline"][contains(text(), "Language:")]/following-sibling::a/text()'
        languages = self.get_tree().xpath(xpath)
        self.languages = languages

    def fetch_budget(self):
        xpath = '//h4[@class="inline"][contains(text(), "Budget:")]/following-sibling::text()[contains(., "$")][1]'
        budget = self.get_tree().xpath(xpath)
        self.budget = budget[0].replace("$", "").replace(".", "").replace(",", "").strip()

    def fetch_opening_weekend(self):
        opening_weekend = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Opening Weekend:")]/following-sibling::text()[1][contains(., "$")]')
        self.opening_weekend = opening_weekend[0].replace("$", "").replace(".", "").replace(",", "").replace("(USA)", "").strip()

    def fetch_gross(self):
        gross = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Gross:")]/following-sibling::text()[1][contains(., "$")]')
        self.gross = gross[0].replace("$", "").replace(".", "").replace(",", "").strip()
    def fetch_aspect_ratio(self):
        aspect_ratio = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Aspect Ratio:")]/following-sibling::text()[1][contains(., ":")]')
        self.aspect_ratio = aspect_ratio[0].strip()

class Movie(API):
    attributes = [
        # imdb_id already set in __init__(),
        'title',
        'year',
        'rating',
        'number_of_ratings',
        'genres',
        'countries',
        'duration',
        'content_rating',
        'description',
        'metascore',
        'keywords',
        'number_of_critics',
        'number_of_user_reviews',
        'release_date_us',
        'languages',
        'budget',
        'opening_weekend',
        'gross',
        'aspect_ratio',
        #'actors',  # TODO
        #'writers',  # TODO
        #'directors',  # TODO
        #'production_companies'  # TODO
    ]

    def get_tree(self):
        return self.__tree

    def __set_data(self):
        for attr in self.attributes:
            getattr(self, 'fetch_{}'.format(attr))()

    def csv(self):
        result = list()
        for attr in self.attributes:
            try:
                result.append(getattr(self, attr))
            except AttributeError as e:
                pass
        print(result)
        return "{}\r".format(",".join(str(item) for item in result))

    def __init__(self, imdb_id, path_movies, path_ratings=None):
        try:
            html_code = get_html_code_from_path("{}/{}.html".format(path_movies, imdb_id))
        except:
            download_html_for_ids([imdb_id], path_movies, URLS["movies"].format(imdb_id))
            html_code = get_html_code_from_path("{}/{}.html".format(path_movies, imdb_id))

        self.__tree = html.fromstring(html_code)
        self.__path = path_movies
        self.__path_movies = path_movies

        # Set IMDb data
        self.imdb_id = imdb_id
        self.__set_data()

        with open(CSV_MOVIES, 'a') as movies_out:
            movies_out.write(self.csv())


if __name__ == '__main__':
    movie = Movie("tt4226388", "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies", "")
    for attribute in movie.attributes:
        print(getattr(movie, attribute))
