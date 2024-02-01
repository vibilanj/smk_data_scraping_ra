import csv
import requests
from math import ceil
from bs4 import BeautifulSoup
from tqdm import tqdm

# SMK_COUNT = 10
# SMK_COUNT = 28892
SMK_COUNT = 14449

SMK_PAGES = ceil(SMK_COUNT / 4)


def read_from_csv(filename):
    with open(filename, newline='') as file:
        rd = csv.reader(file)
        links = list(rd)
    return links[0]


def write_to_csv(ls, filename):
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(ls)


def get_SMK_links_for_page(page):
    url = "https://sekolah.data.kemdikbud.go.id/index.php/Chome/pencarian/"
    payload = {
        'page': str(page),
        'bentuk_pendidikan': 'SMK',
        'status_sekolah': 'semua'
    }
    response = requests.request("POST", url, headers={}, data=payload, files=[])

    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    for elem in soup.find_all('a', href=True):
        if "profil/" in elem.get('href'):
            links.append(elem.get('href'))

    return links


def get_unique_SMK_links():
    all_links = []
    for i in tqdm(range(1, SMK_PAGES + 1)):
        links_for_page = get_SMK_links_for_page(i)
        all_links.extend(links_for_page)

    write_to_csv(all_links, "SMK_links.csv")
    return all_links


def read_links():
    read_from_csv("SMK_links.csv")
