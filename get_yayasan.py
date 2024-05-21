import csv

import aiohttp
import asyncio

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


def write_to_csv(header, data, filename):
    with open(filename, 'w') as file:
        wr = csv.writer(file, quoting=csv.QUOTE_ALL)
        wr.writerow(header)
        wr.writerows(data)


def get_yayasan_info(page):
    soup = BeautifulSoup(page, "lxml")
    body = soup.body

    naungan = body.text.split("Naungan")[-1].split("\n")[2]
    npyp = body.text.split("NPYP")[-1].split("\n")[2].strip()
    a = soup.select_one("a[href*=vervalyayasan]")
    link = "" if a is None else a.get("href")
    return naungan, npyp, link


async def scrape_page(id, session):
    url = BASE_URL + id
    try:
        async with session.get(url) as response:
            if response.status != 200:
                return [id, None, None, None]
            result = await response.text()
            info = get_yayasan_info(result)
            return [id, *info]
    except Exception as _:
        return [id, None, None, None]
    

async def scrape_all_pages(part):
    _, schools = read_from_csv("csv/yayasan/private_foundation_owned.csv")

    step = 3000
    start = (part - 1) * step
    end = part * step
    ids = ids[start:end]

    my_conn = aiohttp.TCPConnector(limit = 100, ssl = False)
    async with aiohttp.ClientSession(connector = my_conn) as session:
        tasks = []
        for school in schools:
            task = asyncio.ensure_future(scrape_page(school[0], session))
            tasks.append(task)
        info = await asyncio.gather(*tasks, return_exceptions = True)

    header = ["npsn", "naungan", "npyp", "link"]
    write_to_csv(header, info, f"yayasan_{part}.csv")
    return info


def run():
    import requests
    
    # link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=69988051"
    # link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=10200410"
    link = "https://referensi.data.kemdikbud.go.id/tabs.php?npsn=10703149"

    page = requests.get(link, timeout=5, verify = False)
    info = get_yayasan_info(page.text)
    print(info)