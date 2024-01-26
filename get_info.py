from get_links import read_links
import requests
from bs4 import BeautifulSoup

def get_info_for_link(link):
    response = requests.get(link, timeout=3)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)

    info = {}
    info["link"] = link

    return info


def get_info_for_all_links():
    links = read_links()[0]
    print(len(links))
