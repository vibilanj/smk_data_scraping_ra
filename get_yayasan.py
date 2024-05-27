import csv
import pickle
from io import StringIO

import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd


BASE_URL = "https://referensi.data.kemdikbud.go.id/pendidikan/npsn/"
HEADER_1 = ["npsn", "naungan", "npyp", "link"]
HEADER_2 = [
    "nypy", "name", "address", "pimpinan_yayasan", "operator_yayasan",
    "kode_pos", "no_pendirian_yayasan", "tgl_pendirian_yayasan", "num_schools"
    ]

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


# Yayasan Pages
def get_unique_yayasan_links(filename):
    _, rows = read_from_csv(filename)
    # from 16337 to 11025
    links = set(map(lambda x: x[-1], rows))
    links.remove("")
    write_to_pickle(list(links), "unique_yayasan.pickle")


async def download_yayasan_page(url, session):
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return [url, None]
            result = await response.text()
            return [url, result]
    except Exception as _:
        return [url, None]


async def download_yayasan_pages(part):
    links = read_from_pickle("unique_yayasan.pickle")

    step = 3000
    start = (part - 1) * step
    end = part * step
    links = links[start:end]
    
    my_conn = aiohttp.TCPConnector(limit = 100, ssl = False)
    async with aiohttp.ClientSession(connector = my_conn) as session:
        tasks = []
        for link in links:
            task = asyncio.ensure_future(download_yayasan_page(link, session))
            tasks.append(task)
        pages = await asyncio.gather(*tasks, return_exceptions = True)

    write_to_pickle(pages, f"yayasan_{part}.pickle")
    return pages


def combine_yayasan_pages():
    data = []
    for i in range(1, 5):
        data += read_from_pickle(f"yayasan_{i}.pickle")
    write_to_pickle(data, "yayasan.pickle")


# Parsing pages for information
def get_nypy_and_name(s):
    head, tail = s.split(')', 1)
    nypy = head[1:]
    name = tail.strip()
    return nypy, name


def get_info_from_text(text, label):
    info = text.split(label)[-1].split("\n")[0]
    info = info.replace('\xa0', ' ')
    info = info.replace('\r', '')
    return info.strip()


def scrape_yayasan_page(page):
    soup = BeautifulSoup(page, "lxml")
    body = soup.body
    if body.find("h4") is None: # Checking for empty pages
        return [], pd.DataFrame()
    
    header = body.select_one("h4[class=page-header]").contents
    nypy, name = get_nypy_and_name(header[0])
    address = header[1].text.strip()

    pimpinan = get_info_from_text(body.text, "Pimpinan Yayasan :") 
    operator = get_info_from_text(body.text, "Operator Yayasan :") 
    kode_pos = get_info_from_text(body.text, "Kode Pos :") 
    no_pendirian = get_info_from_text(body.text, "No. Pendirian Yayasan :") 
    tgl_pendirian = get_info_from_text(body.text, "Tgl Pendirian Yayasan :") 

    table = body.select_one("table")
    yayasan_schools = pd.read_html(StringIO(str(table)))[0]
    yayasan_schools.insert(0, "NYPY", nypy, False)
    no_schools = yayasan_schools.shape[0]

    yayasan_info = [
        nypy, name, address, pimpinan, operator, kode_pos,
        no_pendirian, tgl_pendirian, no_schools
    ]
    return yayasan_info, yayasan_schools


def scrape_yayasan_pages():
    pages = read_from_pickle("yayasan.pickle")

    yayasan_info = []
    yayasan_schools = pd.DataFrame()

    for l, page in pages:
        try:
            info, schools = scrape_yayasan_page(page)
        except:
            print(l)
            break
        yayasan_info.append(info)
        yayasan_schools = yayasan_schools._append(schools)
    yayasan_schools = yayasan_schools.reset_index()
    yayasan_schools = yayasan_schools.drop("index", axis = 1)

    write_to_csv(HEADER_2, yayasan_info, "yayasan_info.csv")
    yayasan_schools.to_csv("yayasan_schools.csv", index=False)


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

    # GETTING YAYASAN LINKS AND PAGES
    # get_unique_yayasan_links("npsn_to_yayasan.csv")
    # asyncio.run(download_yayasan_pages(1))
    # asyncio.run(download_yayasan_pages(2))
    # asyncio.run(download_yayasan_pages(3))
    # asyncio.run(download_yayasan_pages(4))
    # combine_yayasan_pages()
    scrape_yayasan_pages()