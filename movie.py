from util import download_html_for_ids
from util import URLS
from util import get_html_code_from_path
from lxml import html

from settings import *


class API(object):
    def fetch_title(self):
        self.title = self.get_tree().xpath('//div[@class="title_wrapper"][1]/h1/text()[1]')

    def fetch_year(self):
        year = self.get_tree().xpath('//span[@id="titleYear"][1]/a/text()')
        self.year = year

    def fetch_rating(self):
        rating = self.get_tree().xpath('//span[@itemprop="ratingValue"][1]/text()')
        self.rating = rating

    def fetch_number_of_ratings(self):
        number = self.get_tree().xpath('//span[@itemprop="ratingCount"][1]/text()')
        self.number_of_ratings = number.replace(",", "").replace(".", "")

    def fetch_genres(self):
        genres = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Genres:")]/following-sibling::a/text()')
        self.genres = [genre.strip() for genre in genres]
        """
        try:
            with open(CSV_GENRES, 'a') as genre_out:
                genres = self.get_tree().xpath('//span[@itemprop="genre"]')
                for genre in genres:
                    genre_out.write("{},{}\r".format(self.imdb_id, genre.text))
        except:
            pass
        """

    def fetch_countries(self):
        countries = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Country:")]/following-sibling::a/text()')
        self.countries = countries
        """
        with open(CSV_COUNTRIES, 'a') as countries_out:
            countries = self.get_tree().xpath('//div[@id="titleDetails"][1]/div[@class="txt-block"][1]/a')
            for country in countries:
                countries_out.write("{},{}\r".format(self.imdb_id, country.text))
        """

    def fetch_duration(self):
        duration = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Runtime:")]/following-sibling::time/text()')
        self.duration = duration.replace("min", "").strip()

    def fetch_content_rating(self):
        self.content_rating = self.get_tree().xpath('//meta[@itemprop="contentRating"]/@content')

    def fetch_description(self):
        description = self.get_tree().xpath('//div[@itemprop="description"]/p/text()')
        self.description = description.strip().replace("\n", "").replace("\r", "")

    def fetch_metascore(self):
        metascore = self.get_tree().xpath('//div[contains(@class, "metacriticScore")]/span/text()')
        self.metascore = metascore

    def fetch_keywords(self):
        keywords = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Plot Keywords:")]/following-sibling::a/span/text()')
        self.keywords = keywords
        """
        try:
            with open(CSV_KEYWORDS, 'a') as keywords_out:
                xpath_keywords = self.get_tree().xpath('//span[@itemprop="keywords"]')
                keywords = [keyword.text for keyword in xpath_keywords]
                for keyword in keywords:
                    keywords_out.write("{},{}\r".format(self.imdb_id, keyword))
        except:
            pass
        """

    def fetch_number_of_critics(self):
        try:
            links = self.get_tree().xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            self.number_of_critics = int(links[1].text.replace(" critic", "").replace(",", ""))
        except:
            pass

    def fetch_number_of_user_reviews(self):
        try:
            links = self.get_tree().xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            self.number_of_user_review = int(links[0].text.replace(" user", "").replace(",", ""))
        except:
            pass

    def fetch_release_date_us(self):
        release_date_us = self.get_tree().xpath('//div[@class="title_wrapper"]//meta[@itemprop="datePublished"]/@content[1]')
        self.release_date_us = release_date_us

    def fetch_languages(self):
        languages = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Language:")]/following-sibling::a/text()')
        self.languages = languages

    def fetch_budget(self):
        budget = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Budget:")]/following-sibling::text()[1][contains(., "$")]')
        self.budget = budget[0].replace("$", "").replace(".", "").replace(",", "").strip()

    def fetch_opening_weekend(self):
        opening_weekend = self.get_tree().xpath('//h4[@class="inline"][contains(text(), "Opening Weekend:")]/following-sibling::text()[1][contains(., "$")]')
        self.opening_weekend = opening_weekend[0].replace("$", "").replace(".", "").replace(",", "").strip()

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
        'actors',
        'writers',
        'directors',
        'production_companies'
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
        #self.__set_data()

        with open(CSV_MOVIES, 'a') as movies_out:
            movies_out.write(self.csv())


if __name__ == '__main__':
    movie = Movie("tt5974402", "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies", "")
    for attribute in movie.attributes:
        print(getattr(movie, attribute))
