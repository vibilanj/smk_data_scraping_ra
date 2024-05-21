import csv
import pickle

import aiohttp
import asyncio

from bs4 import BeautifulSoup


BASE_URL = "https://referensi.data.kemdikbud.go.id/pendidikan/npsn/"
HEADER_1 = ["npsn", "naungan", "npyp", "link"]


# IO
def read_from_csv(filename):
    rows = []
    with open(filename, newline='\n') as file:
        rd = csv.reader(file)
        header = next(rd)
        for row in rd:
            rows.append(row)
    return header, rows


def write_to_csv(header, data, filename):
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        wr.writerows(data)


def write_to_pickle(list_, filename):
    with open(filename, "wb") as fp:
        pickle.dump(list_, fp)


def read_from_pickle(filename):
    with open(filename, 'rb') as fp:
        return pickle.load(fp)


# NPSN -> Yayasan
def get_yayasan_for_school(page):
    soup = BeautifulSoup(page, "lxml")
    body = soup.body

    naungan = body.text.split("Naungan")[-1].split("\n")[2]
    npyp = body.text.split("NPYP")[-1].split("\n")[2].strip()
    a = soup.select_one("a[href*=vervalyayasan]")
    link = "" if a is None else a.get("href")
    return naungan, npyp, link


async def scrape_school(id, session):
    url = BASE_URL + id
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return [id, None, None, None]
            result = await response.text()
            info = get_yayasan_for_school(result)
            return [id, *info]
    except Exception as _:
        return [id, None, None, None]
    

async def scrape_all_schools(part):
    _, schools = read_from_csv("csv/yayasan/private_foundation_owned.csv")

    step = 3000
    start = (part - 1) * step
    end = part * step
    schools = schools[start:end]

    my_conn = aiohttp.TCPConnector(limit = 100, ssl = False)
    async with aiohttp.ClientSession(connector = my_conn) as session:
        tasks = []
        for school in schools:
            task = asyncio.ensure_future(scrape_school(school[0], session))
            tasks.append(task)
        info = await asyncio.gather(*tasks, return_exceptions = True)

    write_to_pickle(info, f"school_{part}.pickle")
    return info


def combine_npsn_to_yayasan(filename):
    data = []
    for i in range(1, 7):
        data += read_from_pickle(f"school_{i}.pickle")
    write_to_csv(HEADER_1, data, filename)


# TODO: 
# Download all yayasan pages into pickles
# Scrape yayasan info 
# Scrape yayasan owned school info

def run():
    # TESTING INDIVIDUAL PAGES FOR SCHOOL
    # import requests
    # link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=69988051"
    # link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=10200410"
    # link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=10703149"
    # page = requests.get(link, timeout=5, verify = False)
    # info = get_yayasan_info(page.text)
    # print(info)

    # GETTING SCHOOL INFO
    # asyncio.run(scrape_all_schools(1))
    # asyncio.run(scrape_all_schools(2))
    # asyncio.run(scrape_all_schools(3))
    # asyncio.run(scrape_all_schools(4))
    # asyncio.run(scrape_all_schools(5))
    # asyncio.run(scrape_all_schools(6))
    # combine_npsn_to_yayasan("npsn_to_yayasan.csv")

    # TESTING INDIVIDUAL PAGES FOR YAYASAN
    pass