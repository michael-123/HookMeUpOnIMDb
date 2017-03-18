from util import get_watchlist_from_csv_file
from util import get_ratings_from_csv_file
from util import save_to_file
from util import download_html_for_ids
from util import URLS
from util import get_recommendation_ids_from_html_file
from util import download_soundtrack_for_ids
from movie import Movie


CSV_DIR = '/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/tables/'
MOVIE_HTML_DIR = '/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/movies/'
SOUNDTRACK_HTML_DIR = '/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/soundtracks'


def save_csv_from_ratings(csv):
    ratings = get_ratings_from_csv_file(csv)
    save_to_file(ratings, CSV_DIR + 'my_ratings.csv')
    return ratings


def save_csv_from_watchlist(csv):
    watchlist = get_watchlist_from_csv_file(csv)
    save_to_file(watchlist, CSV_DIR + 'watchlist.csv')
    return watchlist


def save_csv_for_recommendations_from_ids(ids):
    result = []
    with open(CSV_DIR + 'recommendations.csv', 'w+') as out:
        for movie_id in ids:
            recommendation_ids = get_recommendation_ids_from_html_file('{}{}.html'.format(MOVIE_HTML_DIR, movie_id))
            result.extend(recommendation_ids)
            for recommendation_id in recommendation_ids:
                out.write('{},{},\r'.format(movie_id, recommendation_id))
    return list(set(result))


def save_movie_information_csvs(ids, html_dir):
    # for all ids load movie html and create csv
    with open(CSV_DIR + 'movies.csv', 'w+') as out:
        for id in ids:
            movie = Movie(id, html_dir)
            # TODO save all csv files


def main():
    # Create ratings table
    ratings = save_csv_from_ratings('/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/ratings.csv')
    rating_ids = [i[0] for i in ratings]

    # Create watchlist table
    watchlist = save_csv_from_watchlist('/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/watchlist.csv')
    watchlist_ids = [i[0] for i in watchlist]

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
    save_movie_information_csvs(ids, MOVIE_HTML_DIR)


if __name__ == '__main__':
    main()
