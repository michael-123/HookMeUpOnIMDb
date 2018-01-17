import os
import requests
import csv

from lxml import html


DATA_FOLDER = 'data'


class IMDbHTMLMixin(object):

    def fetch_title(self):
        xpath = '//h1[@itemprop="name"][1]'
        title = self.get_tree().xpath(xpath)[0].text
        return title.strip()

    def fetch_year(self):
        xpath = '//span[@id="titleYear"][1]/a/text()'
        try:
            return int(self.get_tree().xpath(xpath)[0])
        except IndexError:
            print(self.movie_id, self.title, "has no year")
            pass

    def fetch_rating(self):
        xpath = '//span[@itemprop="ratingValue"][1]/text()'
        rating = self.get_tree().xpath(xpath)[0]
        return float(rating.replace(",", "."))

    def fetch_number_of_ratings(self):
        xpath = '//span[@itemprop="ratingCount"][1]/text()'
        number = self.get_tree().xpath(xpath)[0]
        return int(number.replace(",", "").replace(".", "").strip())

    def fetch_movie_or_show(self):
        xpath = '//div[@class="bp_heading"]/text()'
        s = self.get_tree().xpath(xpath)
        return 'show' if 'Episode Guide' == s else 'movie'


    def fetch_genres(self):
        xpath = '//h4[@class="inline"][contains(text(), "Genres:")]/following-sibling::a/text()'
        genres = self.get_tree().xpath(xpath)
        return [genre.strip() for genre in genres]

    def fetch_countries(self):
        xpath = '//h4[@class="inline"][contains(text(), "Country:")]/following-sibling::a/text()'
        return self.get_tree().xpath(xpath)

    def fetch_duration(self):
        xpath = '//h4[@class="inline"][contains(text(), "Runtime:")]/following-sibling::time/text()'
        try:
            duration = self.get_tree().xpath(xpath)[0]
            return int(duration.replace("min", "").strip())
        except IndexError:
            pass

    def fetch_content_rating(self):
        xpath = '//meta[@itemprop="contentRating"]/@content'
        return self.get_tree().xpath(xpath)[0]

    def fetch_metascore(self):
        xpath = '//div[contains(@class, "metacriticScore")]/span/text()'
        try:
            metascore = self.get_tree().xpath(xpath)[0]
            return metascore
        except IndexError:
            pass

    def fetch_number_of_critics(self):
        xpath = '//div[@class ="titleReviewBarItem titleReviewbarItemBorder"]//a/text()[contains(., "critic")]'
        try:
            critics = self.get_tree().xpath(xpath)[0]
            return int(critics.replace(" critic", "").replace(",", "").strip())
        except IndexError:
            pass

    def fetch_languages(self):
        xpath = '//h4[@class="inline"][contains(text(), "Language:")]/following-sibling::a/text()'
        languages = self.get_tree().xpath(xpath)
        return languages

    def fetch_budget(self):
        xpath = '//h4[@class="inline"][contains(text(), "Budget:")]/following-sibling::text()[contains(., "$")][1]'
        budget = self.get_tree().xpath(xpath)
        try:
            budget = budget[0].replace("$", "").replace(".", "").replace(",", "").strip()
            return int(budget)
        except IndexError:
            pass


class Movie(IMDbHTMLMixin):

    def __init__(self, movie_id, user_rating=None):
        self.data_path = '{}/{}.html'.format(DATA_FOLDER, movie_id)
        self.movie_id = movie_id
        self.user_rating = user_rating
        self.load_movie_attributes()

    def get_tree(self):
        return self.__tree

    def check(self):
        from pprint import pprint
        pprint({
            'Title': self.title,
            'Year': self.year,
            'IMDB rating': self.imdb_rating,
            'User rating': self.user_rating,
            'Number of ratings': self.number_of_ratings,
            'Genres': self.genres,
            'Countries': self.countries,
            'Duration': self.duration,
            'Metascore': self.metascore,
            'Number of critics': self.number_of_critics,
            'Languages': self.languages,
            'Budget': self.budget,
            'Movie or Show': self.movie_or_show,
        })

    def load_movie_attributes(self):
        # If HTML file is not there already
        if not os.path.isfile(self.data_path):
            with open(self.data_path, 'w', encoding='utf8') as html_out:
                url = 'http://www.imdb.com/title/{}'.format(self.movie_id)
                html_out.write(requests.get(url).text)

        # Load HTML code
        with open(self.data_path, 'r', encoding='utf8') as html_in:
            self.html = html_in.read()

        # Parse file and set attributes
        self.__tree = html.fromstring(self.html)
        self.title = self.fetch_title()
        self.year = self.fetch_year()
        self.imdb_rating = self.fetch_rating()
        self.number_of_ratings = self.fetch_number_of_ratings()
        self.genres = self.fetch_genres()
        self.countries = self.fetch_countries()
        self.duration = self.fetch_duration()
        self.metascore = self.fetch_metascore()
        self.number_of_critics = self.fetch_number_of_critics()
        self.languages = self.fetch_languages()
        self.budget = self.fetch_budget()
        self.movie_or_show = self.fetch_movie_or_show()


def retrieve_movie_id_and_rating_from_ratings_csv(csv_path):
    with open(csv_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        return [(r[1], int(r[8])) for r in rows if r[1].startswith('tt')]


def build_knowledge(path_to_ratings_csv):
    movie_id_rating_tuples = retrieve_movie_id_and_rating_from_ratings_csv(path)
    movies = [Movie(movie_id, rating) for movie_id, rating in movie_id_rating_tuples]
    pass


if __name__ == '__main__':
    build_knowledge()
