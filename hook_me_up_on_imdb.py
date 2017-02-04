import os
import csv
import requests
from lxml import html

URLS = {
    "movies": "http://www.imdb.com/title/{0}/",
    "soundtrack": "http://www.imdb.com/title/{0}/soundtrack",
    "top250": "http://www.imdb.com/chart/top"
}

DO_LOG = True


def log_me(message):
    """ Log functionality """
    if DO_LOG:
        print(message)


def get_html_code_from_url(url):
    """ Gets you the HTML code of given URL. """
    return requests.get(url).text


def get_ids_from_top_250():
    """ Gets you the ids from the Top 250"""
    result = list()
    html_code = get_html_code_from_url(URLS["top250"])
    tree = html.fromstring(html_code)
    columns = tree.xpath('//td[@class="titleColumn"]')

    for column in columns:
        href = column.xpath("a/@href")[0]
        id = href[7:16]
        result.append(id)

    return result


def get_recommendation_ids_from_html_file(html_file):
    """ Gets you all movie ids for a movie's (html_file) recommendations. """
    result = list()

    with open(html_file, "r", encoding="utf8") as f:
        html_code = f.read()
        tree = html.fromstring(html_code)
        recs = tree.xpath('//div[@class="rec_item"]')

        for rec in recs:
            href = rec.xpath("a/@href")[0]
            id = href[7:16]
            result.append(id)

    return result


def get_ids_from_csv_file(csv_path, column=1):
    """ Gets you all movie ids from a CSV file at csv_path. """
    result = list()
    with open(csv_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        for row in rows:
            if row.startswith('tt'):
                result.append(row[column])
    return result


def write_html_file(path, file_name, html_code):
    """ Writes html file """
    os.makedirs(path, exist_ok=True)
    out = "{0}/{1}.html".format(path, file_name)
    try:
        with open(out, "x", encoding="utf8") as file:
            file.write(html_code)
    except FileExistsError:
        log_me("{0} skipped. Already there.".format(out))


def download_html_for_ids(download_ids, path, url):
    """ Downloads for a list of movie ids the html code and saves it to the local disk. """
    for download_id in download_ids:
        if not os.path.isfile("{0]/{1}.html".format(path, download_id)):
            html_code = get_html_code_from_url(url.format(download_id))
            write_html_file(path, download_id, html_code)
        else:
            log_me("Download {0} skipped. Already there.".format(download_id))


def download_soundtrack_for_ids(id_list, to_path):
    """ Downloading soundtracks with given ids to path. """
    log_me("Downloading {0} soundtracks.".format(len(id_list)))
    download_html_for_ids(id_list, to_path, URLS["soundtrack"])


def download_movies_for_ids(id_list, to_path):
    """ Downloading movies with given ids to path. """
    log_me("Downloading {0} movies.".format(len(id_list)))
    download_html_for_ids(id_list, to_path, URLS["movies"])


def get_all_ids_from_directory(from_path):
    """ Gets you all ids from a given directory. """
    result = list()
    for file in os.listdir(from_path):
        result.append(file[:-5])
    log_me("{0} ids found.".format(len(result)))
    return result


def save_ids_as_csv(id_list, to_path):
    """ Saves a list of ids to a CSV file. """
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, "w") as out:
        for id in id_list:
            out.write("{0},\n".format(id))


def main():
    """ Do what you want to do. """


if __name__ == '__main__':
    main()
