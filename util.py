import os
import csv
import requests
from lxml import html
from settings import DO_LOG

URLS = {
    "movies": "http://www.imdb.com/title/{0}/",
    "soundtrack": "http://www.imdb.com/title/{0}/soundtrack",
    "top250": "http://www.imdb.com/chart/top"
}


def log(message):
    if DO_LOG:
        print(message)


def save_to_file(list_of_lists, to_file):
    with open(to_file, 'w+') as out:
        for entry in list_of_lists:
            out.write(str(entry).replace('[', '').replace(']', '') + ',\r')


def get_html_code_from_path(path):
    with open(path, "r", encoding="utf8") as f:
        return f.read()


def get_html_code_from_url(url):
    return requests.get(url).text


def get_ids_from_top_250():
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
    result = list()
    with open(csv_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        for row in rows:
            if row[column].startswith('tt'):
                result.append(row[column])
    return result


def get_ratings_from_csv_file(csv_path, user_name):
    result = list()
    with open(csv_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        for row in rows:
            if row[1].startswith('tt'):
                result.append([row[1], row[8], row[5], user_name, row[2]])
    return result


def get_watchlist_from_csv_file(csv_path, user_name):
    result = list()
    with open(csv_path, 'r') as file:
        rows = csv.reader(file, delimiter=',', quotechar='"')
        for row in rows:
            if row[1].startswith('tt'):
                result.append([row[1], row[5], user_name])
    return result


def write_html_file(path, file_name, html_code):
    os.makedirs(path, exist_ok=True)
    out = "{0}/{1}.html".format(path, file_name)
    try:
        with open(out, "x", encoding="utf8") as file:
            file.write(html_code)
    except FileExistsError:
        log("{0} skipped. Already there.".format(out))


def download_html_for_ids(ids_to_download, repository_path, url):
    for download_id in ids_to_download:
        if not os.path.isfile("{0}/{1}.html".format(repository_path, download_id)):
            html_code = get_html_code_from_url(url.format(download_id))
            write_html_file(repository_path, download_id, html_code)
        else:
            log("Download {0} skipped. Already there.".format(download_id))


def download_soundtrack_for_ids(id_list, to_path):
    log("Downloading {0} soundtracks.".format(len(id_list)))
    download_html_for_ids(id_list, to_path, URLS["soundtrack"])


def download_movies_for_ids(id_list, to_path):
    log("Downloading {0} movies.".format(len(id_list)))
    download_html_for_ids(id_list, to_path, URLS["movies"])


def get_all_ids_from_directory(from_path):
    result = list()
    for file in os.listdir(from_path):
        result.append(file[:-5])
    log("{0} ids found.".format(len(result)))
    return result


def save_ids_as_csv(id_list, to_path):
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, "w") as out:
        for id in id_list:
            out.write("{0},\n".format(id))


def main():
    pass


if __name__ == '__main__':
    main()
