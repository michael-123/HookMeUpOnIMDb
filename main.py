import os

import requests
from lxml import html

DO_LOG = True


def log_me(message):
    if DO_LOG:
        print(message)


def get_ratings(user):
    """
    Gets you all movie ids from the ratings list (must be public) for a given user.
    :param user: IMDb User ID
    :return: List of movie ids
    """

    def get_counter_list():
        """
        Get list of counters
        :return:
        """
        xpath = '//div[@id="main"][1]//div[@class="header"][1]/div[@class="nav"][1]/div[@class="desc"][1]/span'
        r = requests.get(url.format(user, 1))
        tree = html.fromstring(r.content)

        # Gets you '(774 Titles)'
        s = tree.xpath(xpath)[0].text
        number = int(s[1:-8])
        my_range = range(0, int(number / 100) + 1)
        res = map(lambda x: x * 100 + 1, my_range)
        return list(res)

    rating_ids = []
    url = 'http://www.imdb.com/user/{0}/ratings?start={1}&view=detail&sort=ratings_date:desc'.format(user, "{0}")
    counter_list = get_counter_list()

    # Get all movie ids from rating list
    for counter in counter_list:
        log_me("Request {0}".format(counter))
        r = requests.get(url.format(counter))
        tree = html.fromstring(r.content)

        movie_ids = tree.xpath('//div[@class="info"]/b/a/@href')
        reduced_ids = map(lambda id: id[7:-1], movie_ids)
        rating_ids.extend(list(reduced_ids))

    return rating_ids


def write_html_file(path, rating, content):
    """
    Writes html file
    """
    os.makedirs(path, exist_ok=True)

    out = path + "/" + rating + ".html"
    log_me("Writing {0}".format(out))
    with open(out, "w") as file:
        file.write(content)


def download_html_for_movie_ids(movie_ids, path):
    # url = 'http://www.imdb.com/list/export?list_id=ratings&author_id=ur24735567'
    """
    Downloads for a list of movie ids the html code and saves it to the local disk.
    :param movie_ids:
    :param path:
    :return:
    """
    movie_url = "http://www.imdb.com/title/{0}/"
    for id in movie_ids:
        log_me("Downloading {0}".format(movie_url.format(id)))

        r = requests.get(movie_url.format(id))
        write_html_file(path, id, r.text)


def get_watchlist(user_id, watchlist_id):
    url = 'http://www.imdb.com/list/export?list_id={0}&author_id=ur{1}'
    # TODO download watchlist (CSV)
    pass


def download_imdb_data(user_id, path, watchlist_id):
    # Get Ratings
    #rating_ids = get_ratings(user_id)

    # Download HTML code
    download_html_for_movie_ids(rating_ids, path+"/ratings")

    # Get Watchlist
    watchlist_ids = get_watchlist(user_id, watchlist_id)


    # Download HTML code

    # Get Reccomendations for Watchlist/Ratings
    # Download HTML code


if __name__ == '__main__':
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("-user", "--user", required=True)
    p.add_argument("-path", "--path", required=True)
    p.add_argument("-wlid", "--wlid", required=True)
    args = p.parse_args()

    user = args.user
    path = args.path
    watchlist_id = args.wlid

    download_imdb_data(user, path, watchlist_id)
