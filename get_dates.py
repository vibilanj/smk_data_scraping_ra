import csv
import pickle

import aiohttp
import asyncio
import requests

from bs4 import BeautifulSoup


BASE_URL = "https://referensi.data.kemdikbud.go.id/pendidikan/npsn/"


def read_from_csv(filename):
    rows = []
    with open(filename, newline='\n') as file:
        rd = csv.reader(file)
        header = next(rd)
        for row in rd:
            rows.append(row)
    return header, rows


def read_ids():
    files = ["csv/missing_npsn_dates/missing_SMA.csv",
             "csv/missing_npsn_dates/missing_SMK.csv"]
    _, rows_SMA = read_from_csv(files[0])
    _, rows_SMK = read_from_csv(files[1])
    rows = rows_SMA + rows_SMK
    return rows


def write_to_pickle(list_, part):
    with open(f"dates_{part}.pickle", "wb") as fp:
        pickle.dump(list_, fp)


def read_from_pickle(part):
    with open(f"dates_{part}.pickle", 'rb') as fp:
        return pickle.load(fp)


def get_dates_for_page(page):
    soup = BeautifulSoup(page, "lxml")
    body = soup.body
    tanggal_pendirian = body.text.split("Tanggal SK. Pendirian")[-1].split("\n")[2]
    tanggal_operasional = body.text.split("Tanggal SK Operasional")[-1].split("\n")[2]
    return tanggal_pendirian, tanggal_operasional


async def scrape_page(id, session):
    url = BASE_URL + id
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return [id, None, None]
            result = await response.text()
            dates = get_dates_for_page(result)
            return [id, *dates]
    except Exception as _:
        return [id, None, None]
    

async def scrape_all_pages(part):
    ids = read_ids()

    step = 3000
    start = (part - 1) * step
    end = part * step
    ids = ids[start:end]

    my_conn = aiohttp.TCPConnector(limit = 100, ssl = False)
    async with aiohttp.ClientSession(connector = my_conn) as session:
        tasks = []
        for id in ids:
            task = asyncio.ensure_future(scrape_page(id[0], session))
            tasks.append(task)
        pages = await asyncio.gather(*tasks, return_exceptions = True)

    write_to_pickle(pages, part)
    return pages


def combine_and_save(filename):
    data = []
    for i in range(1, 4):
        data += read_from_pickle(i)

    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(["npsn", "tanggal_pendirian", "tanggal_operasional"])
        wr.writerows(data)
