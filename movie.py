from util import download_html_for_ids
from util import URLS
from util import get_html_code_from_path
from lxml import html


class Movie:
    def __init__(self, movie_id, path_movies, path_ratings=None):
        try:
            html_code = get_html_code_from_path("{0}/{1}.html".format(path_movies, movie_id))
        except:
            download_html_for_ids([movie_id], path_movies, URLS["movies"].format(movie_id))
            html_code = get_html_code_from_path("{0}/{1}.html".format(path_movies, movie_id))
        self.__tree = html.fromstring(html_code)
        self.__id = movie_id
        self.__path = path_movies
        self.__set_data()

    def __set_data(self):
        """ Sets data from HTML file. """
        self.title = self.get_title()
        self.year = self.get_year()
        self.rating = self.get_rating()
        self.number_of_ratings = self.get_number_ratings()
        self.genres = self.get_genre()
        self.countries = self.get_countries()

    def get_title(self):
        """ Returns title of the movie. """
        try:
            return self.__tree.xpath('//div[@class="title_wrapper"][1]/h1')[0].text
        except:
            return None

    def get_year(self):
        """ Returns year of the movie. """
        try:
            spans = self.__tree.xpath('//span[@id="titleYear"]')
            year = spans[0].xpath('a')[0].text
            return int(year)
        except:
            return None

    def get_rating(self):
        """ Returns the IMDb rating. """
        try:
            rating = self.__tree.xpath('//span[@itemprop="ratingValue"]')[0].text
            return float(rating)
        except:
            return None

    def get_number_ratings(self):
        """ Returns the number of ratings. """
        try:
            number = self.__tree.xpath('//span[@itemprop="ratingCount"]')[0].text
            return int(number.replace(",", ""))
        except:
            return None

    def get_genre(self):
        """ Returns list of genres of the movie. """
        try:
            result = list()
            genres = self.__tree.xpath('//span[@itemprop="genre"]')
            for genre in genres:
                result.append(genre.text)
            return result
        except:
            return None

    def get_countries(self):
        try:
            result = list()
            countries = self.__tree.xpath('//div[@id="titleDetails"][1]/div[@class="txt-block"][1]/a')
            for country in countries:
                result.append(country.text)
            return result
        except:
            return None

    def to_csv_line(self):
        return 'asdf,\r'


if __name__ == '__main__':
    movie = Movie("tt5974402", "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies", "")
    print(movie.title)
    print(movie.year)
    print(movie.rating)
    print(movie.number_of_ratings)
    print(movie.genres)
    print(movie.countries)