from util import download_html_for_ids
from util import URLS
from util import get_html_code_from_path
from lxml import html


class Movie:
    def __init__(self, movie_id, path_movies, path_ratings=None):
        self.__path_movies = path_movies
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
        self.title = self.fetch_title()
        self.year = self.fetch_year()
        self.rating = self.fetch_rating()
        self.number_of_ratings = self.fetch_number_ratings()
        self.genres = self.fetch_genre()
        self.countries = self.fetch_countries()
        self.duration = self.fetch_duration()
        self.content_rating = self.fetch_content_rating()
        self.description = self.fetch_description()
        self.metascore = self.fetch_metascore()
        self.storyline = self.fetch_storyline()
        self.keywords = self.fetch_keywords()
        self.number_of_critics = self.fetch_number_of_critics()
        self.number_of_user_reviews = self.fetch_number_of_user_reviews()

    def fetch_title(self):
        """ Returns title of the movie. """
        try:
            return self.__tree.xpath('//div[@class="title_wrapper"][1]/h1')[0].text
        except:
            return None

    def fetch_year(self):
        """ Returns year of the movie. """
        try:
            spans = self.__tree.xpath('//span[@id="titleYear"]')
            year = spans[0].xpath('a')[0].text
            return int(year)
        except:
            return None

    def fetch_rating(self):
        """ Returns the IMDb rating. """
        try:
            rating = self.__tree.xpath('//span[@itemprop="ratingValue"]')[0].text
            return float(rating)
        except:
            return None

    def fetch_number_ratings(self):
        """ Returns the number of ratings. """
        try:
            number = self.__tree.xpath('//span[@itemprop="ratingCount"]')[0].text
            return int(number.replace(",", ""))
        except:
            return None

    def fetch_genre(self):
        """ Returns list of genres of the movie. """
        try:
            result = list()
            genres = self.__tree.xpath('//span[@itemprop="genre"]')
            for genre in genres:
                result.append(genre.text)
            return result
        except:
            return None

    def fetch_countries(self):
        try:
            result = list()
            countries = self.__tree.xpath('//div[@id="titleDetails"][1]/div[@class="txt-block"][1]/a')
            for country in countries:
                result.append(country.text)
            return result
        except:
            return None

    def fetch_duration(self):
        try:
            duration = self.__tree.xpath('//time[@itemprop="duration"]')[0].text
            hours = duration.strip().split(" ")[0].replace("h", "")
            minutes = duration.strip().split(" ")[1].replace("min", "")
            return float(hours) * 60.0 + float(minutes)
        except:
            return None

    def fetch_content_rating(self):
        try:
            content_rating = self.__tree.xpath('//meta[@itemprop="contentRating"]')[0].text
            return content_rating
        except:
            return None

    def fetch_description(self):
        try:
            description = self.__tree.xpath('//div[@itemprop="description"]')[0].text
            return description
        except:
            return None

    def fetch_metascore(self):
        try:
            metascore = self.__tree.xpath('//div[contains(@class, "metacriticScore")]/span')[0].text
            return float(metascore)
        except Exception as e:
            return None

    def fetch_storyline(self):
        try:
            storyline = self.__tree.xpath('//div[@id="titleStoryLine"]//div[@itemprop="description"]')[0].text
            return storyline
        except:
            return None

    def fetch_keywords(self):
        try:
            xpath_keywords = self.__tree.xpath('//span[@itemprop="keywords"]')
            keywords = [keyword.text for keyword in xpath_keywords]
            return ",".join(keywords)
        except:
            return None

    def fetch_number_of_critics(self):
        try:
            links = self.__tree.xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            return int(links[1].text.replace(" critic", "").replace(",", ""))
        except:
            return None

    def fetch_number_of_user_reviews(self):
        try:
            links = self.__tree.xpath('// div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a')
            return int(links[0].text.replace(" user", "").replace(",", ""))
        except:
            return None



    def save(self):
        return 'asdf,\r'


if __name__ == '__main__':
    movie = Movie("tt5974402", "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies", "")
    print(movie.title)
    print(movie.year)
    print(movie.rating)
    print(movie.number_of_ratings)
    print(movie.genres)
    print(movie.countries)