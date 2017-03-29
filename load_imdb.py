from util import get_watchlist_from_csv_file
from util import get_ratings_from_csv_file
from util import save_to_file
from util import download_html_for_ids
from util import get_recommendation_ids_from_html_file
from util import download_soundtrack_for_ids

from movie import Movie

from settings import CSV_MOVIES
from settings import CSV_RATINGS
from settings import CSV_RECOMMENDATIONS
from settings import CSV_WATCHLIST
from settings import MOVIE_HTML_DIR
from settings import SOUNDTRACK_HTML_DIR
from settings import IMDB_USER_ID
from settings import RATINGS_FILE_PATH
from settings import WATCHLIST_FILE_PATH
from settings import DO_LOG

URLS = {
    "movies": "http://www.imdb.com/title/{0}/",
    "soundtrack": "http://www.imdb.com/title/{0}/soundtrack",
    "top250": "http://www.imdb.com/chart/top"
}


def log(message):
    """ Log functionality """
    if DO_LOG:
        print(message)


def save_csv_from_ratings(csv, user_name, out_file_name=CSV_RATINGS):
    log("Create CSV file {} for user {}.".format(out_file_name, user_name))
    ratings = get_ratings_from_csv_file(csv, user_name)
    save_to_file(ratings, out_file_name)
    return [i[0] for i in ratings]


def save_csv_from_watchlist(csv, user_name, out_file_name=CSV_WATCHLIST):
    log("Create watchlist file {} for user {}.".format(out_file_name, user_name))
    watchlist = get_watchlist_from_csv_file(csv, user_name)
    save_to_file(watchlist, out_file_name)
    return [i[0] for i in watchlist]


def save_csv_for_recommendations_from_ids(ids):
    result = []
    with open(CSV_RECOMMENDATIONS, 'w+') as out:
        for movie_id in ids:
            recommendation_ids = get_recommendation_ids_from_html_file('{}/{}.html'.format(MOVIE_HTML_DIR, movie_id))
            result.extend(recommendation_ids)
            for recommendation_id in recommendation_ids:
                out.write('{},{},\r'.format(movie_id, recommendation_id))
    return list(set(result))


def save_movie_information_csv_files(ids, html_dir):
    # for all ids load movie html and create csv
    with open(CSV_MOVIES, 'w+') as out:
        for id in ids:
            log("Fetch movie information for movie id {}.".format(id))
            movie = Movie(id, html_dir)
            print(movie.title)
            # TODO save all csv files


def main():
    # Create ratings table
    rating_ids = save_csv_from_ratings(RATINGS_FILE_PATH, IMDB_USER_ID)

    # Create watchlist table
    watchlist_ids = save_csv_from_watchlist(WATCHLIST_FILE_PATH, IMDB_USER_ID)

    # Download all movies
    ids = []
    ids.extend(rating_ids)
    ids.extend(watchlist_ids)
    download_html_for_ids(ids, MOVIE_HTML_DIR, URLS['movies'])

    # Create recommendations table
    recommendation_ids = save_csv_for_recommendations_from_ids(ids)
    download_html_for_ids(recommendation_ids, MOVIE_HTML_DIR, URLS['movies'])

    # Download soundtrack
    ids.extend(recommendation_ids)
    ids = list(set(ids))
    download_soundtrack_for_ids(ids, SOUNDTRACK_HTML_DIR)

    # Create movie table
    save_movie_information_csv_files(ids, MOVIE_HTML_DIR)


if __name__ == '__main__':
    main()
