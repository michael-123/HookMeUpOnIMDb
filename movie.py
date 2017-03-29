from util import download_html_for_ids
from util import URLS
from util import get_html_code_from_path
from lxml import html

from settings import *

class API():

    def fetch_title(self):
        try:
            self.title = self.get_tree().xpath('//div[@class="title_wrapper"][1]/h1')[0].text
        except:
            pass

    def fetch_year(self):
        try:
            spans = self.get_tree().xpath('//span[@id="titleYear"]')
            year = spans[0].xpath('a')[0].text
            self.year =  int(year)
        except:
            pass

    def fetch_rating(self):
        try:
            rating = self.get_tree().xpath('//span[@itemprop="ratingValue"]')[0].text
            self.rating = float(rating)
        except:
            pass

    def fetch_number_of_ratings(self):
        try:
            number = self.get_tree().xpath('//span[@itemprop="ratingCount"]')[0].text
            self.number_of_ratings = int(number.replace(",", ""))
        except:
            pass

    def fetch_genre(self):
        try:
            result = list()
            genres = self.get_tree().xpath('//span[@itemprop="genre"]')
            for genre in genres:
                result.append(genre.text)
            return result
        except:
            pass

    def fetch_countries(self):
        try:
            result = list()
            countries = self.get_tree().xpath('//div[@id="titleDetails"][1]/div[@class="txt-block"][1]/a')
            for country in countries:
                result.append(country.text)
            return result
        except:
            pass

    def fetch_duration(self):
        try:
            duration = self.get_tree().xpath('//time[@itemprop="duration"]')[0].text
            hours = duration.strip().split(" ")[0].replace("h", "")
            minutes = duration.strip().split(" ")[1].replace("min", "")
            self.duration =  float(hours) * 60.0 + float(minutes)
        except:
            pass

    def fetch_content_rating(self):
        try:
            self.content_rating = self.get_tree().xpath('//meta[@itemprop="contentRating"]')[0].text
        except:
            pass

    def fetch_description(self):
        try:
            self.description = self.get_tree().xpath('//div[@itemprop="description"]')[0].text
        except:
            pass

    def fetch_metascore(self):
        try:
            metascore = self.get_tree().xpath('//div[contains(@class, "metacriticScore")]/span')[0].text
            self.metascore = float(metascore)
        except:
            pass

    def fetch_storyline(self):
        try:
            self.storyline = self.get_tree().xpath('//div[@id="titleStoryLine"]//div[@itemprop="description"]')[0].text
        except:
            pass

    def fetch_keywords(self):
        try:
            xpath_keywords = self.get_tree().xpath('//span[@itemprop="keywords"]')
            keywords = [keyword.text for keyword in xpath_keywords]
            return ",".join(keywords)
        except:
            pass

    def fetch_number_of_critics(self):
        try:
            links = self.get_tree().xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            self.number_of_critics = int(links[1].text.replace(" critic", "").replace(",", ""))
        except:
            pass

    def fetch_number_of_user_reviews(self):
        try:
            links = self.get_tree().xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            self.number_of_user_review =  int(links[0].text.replace(" user", "").replace(",", ""))
        except:
            pass


class Movie(API):
    attributes = [
        # imdb_id already set in __init__(),
        'title',
        'year',
        'rating',
        'number_of_ratings',
#        'genres',
#        'countries',
        'duration',
        'content_rating',
        'description',
        'metascore',
        'storyline',
#        'keywords',
        'number_of_critics',
        'number_of_user_reviews',  
    ]

    def get_tree(self):
        return self.__tree

    def __set_data(self):
        for attribute in self.attributes:
            getattr(self, 'fetch_{}'.format(attribute))()
            
    def __init__(self, imdb_id, path_movies, path_ratings=None):
        try:
            html_code = get_html_code_from_path("{0}/{1}.html".format(path_movies, imdb_id))
        except:
            download_html_for_ids([imdb_id], path_movies, URLS["movies"].format(imdb_id))
            html_code = get_html_code_from_path("{0}/{1}.html".format(path_movies, imdb_id))

        self.__tree = html.fromstring(html_code)
        self.__path = path_movies
        self.__path_movies = path_movies

        # Set IMDb data
        self.imdb_id = imdb_id
        self.__set_data()

    
if __name__ == '__main__':
    movie = Movie("tt5974402", "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies", "")
    for attribute in movie.attributes:
        print(getattr(movie, attribute))
