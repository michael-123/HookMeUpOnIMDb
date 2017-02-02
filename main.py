import os
import csv
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
    with open(out, "w", encoding="utf8") as file:
        file.write(content)


def download_html_for_movie_ids(movie_ids, path):
    # url = 'http://www.imdb.com/list/export?list_id=ratings&author_id={0}
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


def get_ids_from_csv_file(file_path):
    result = []
    with open(file_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        for row in rows:
            if row is not 'const':
                result.append(row[1])
    return result

def get_recommendation_ids_for_movies(path, subfolder):

    def get_recomendation_ids_from_html_file(open_path, html_file):
        result = []

        print(open_path+"/"+html_file)
        with open(open_path+"/"+html_file, "r", encoding="utf8") as f:
            html_code = f.read()
            tree = html.fromstring(html_code)
            recommendations = tree.xpath('//div[@class="rec_item"]')

            for rec in recommendations:
                s = rec.xpath("a/@href")[0]
                id = s[7:-17]
                result.append(id)

        return result

    sub_path = path+"/"+subfolder
    movie_ids = []

    for filename in os.listdir(sub_path):
        if filename.endswith(".html"):
            ids = get_recomendation_ids_from_html_file(sub_path, filename)
            movie_ids.extend(ids)
            continue
        else:
            continue

    return movie_ids


def get_already_there(path):
    result = []
    for filename in os.listdir(path):
        result.append(filename[:-5])
    return result


def download_imdb_data(user_id, path, watchlist_id):
    # Get Ratings
    # rating_ids = get_ratings(user_id)
    # download_html_for_movie_ids(rating_ids, path+"/ratings")

    # Get Watchlist
    # watchlist_ids = get_ids_from_csv_file(path+"/watchlist.csv")
    # download_html_for_movie_ids(watchlist_ids, path+"/watchlist")

    # Get Reccomendations for Watchlist/Ratings
    watchlist_ids = get_recommendation_ids_for_movies(path, "watchlist")
    rating_ids = get_recommendation_ids_for_movies(path, "ratings")

#    2787
#    7935

    already_loaded = get_already_there("imdb")

    filtered_wids = list(filter(lambda x: x not in already_loaded, watchlist_ids))
    filtered_rids = list(filter(lambda x: x not in already_loaded, rating_ids))

    #download_html_for_movie_ids(watchlist_ids, "imdb")
    download_html_for_movie_ids(filtered_rids, "imdb")

def download_relationships_as_csv(path):
    def get_recommendation_ids_for_movies(path, subfolder):
        def get_recomendation_ids_from_html_file(open_path, html_file):
            result = []
            with open(open_path + "/" + html_file, "r", encoding="utf8") as f:
                html_code = f.read()
                tree = html.fromstring(html_code)
                recommendations = tree.xpath('//div[@class="rec_item"]')

                for rec in recommendations:
                    s = rec.xpath("a/@href")[0]
                    id = s[7:-17]
                    result.append(id)

            return result

        sub_path = path + "/" + subfolder

        for filename in os.listdir(sub_path):
            if filename.endswith(".html"):
                ids = get_recomendation_ids_from_html_file(sub_path, filename)
                result_dict[filename[:-5]] = ids
                continue
            else:
                continue

    result_dict = {}
    get_recommendation_ids_for_movies(path, "ratings")
    get_recommendation_ids_for_movies(path, "watchlist")

    with open("imdb/recommendations.csv", "w") as out:
        for key, value in result_dict.items():
            out.write(key+";"+"|".join(value)+"\n")


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

    path = "/home/michael-123/PyCharmProjects/HookMeUpOnIMDb-Data"
    path = "/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data"

    download_relationships_as_csv(path)
