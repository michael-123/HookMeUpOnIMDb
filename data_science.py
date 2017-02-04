import hook_me_up_on_imdb
from data_access_objects import Movie


def get_watch_count_per_year(path_to_ratings_csv, movies_path):
    movie_ids = hook_me_up_on_imdb.get_ids_from_csv_file(path_to_ratings_csv)
    movies = list()
    for movie_id in movie_ids:
        movies.append(Movie(movie_id, movies_path))

    year_counter = dict()
    for movie in movies:
        if movie.year not in year_counter:
            year_counter[movie.year] = 0

        year_counter[movie.year] += 1

    for year, count in year_counter.items():
        print("{0},{1}".format(year, count))
