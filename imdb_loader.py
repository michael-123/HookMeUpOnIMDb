from hook_me_up_on_imdb import (
    get_watchlist_from_csv_file,
    get_ratings_from_csv_file,
    save_to_file
)

CSV_DIR = '/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/tables/'


def save_csv_from_ratings(csv):
    ratings = get_ratings_from_csv_file(csv)
    save_to_file(ratings, CSV_DIR + 'my_ratings.csv')
    return ratings


def save_csv_from_watchlist(csv):
    watchlist = get_watchlist_from_csv_file(csv)
    save_to_file(watchlist, CSV_DIR + 'watchlist.csv')
    return watchlist


def main():
    ratings = save_csv_from_ratings('/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/ratings.csv')
    rating_ids = [i[0] for i in ratings]
    watchlist = save_csv_from_watchlist('/home/michael-123/PycharmProjects/HookMeUpOnIMDb-Data/watchlist.csv')
    watchlist_ids = [i[0] for i in watchlist]

if __name__ == '__main__':
    main()
