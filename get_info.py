from get_links import read_links
import requests
from bs4 import BeautifulSoup

def get_npsn_name_address(data):
    first = data[0]
    npsn, name = first.split(") ")

    second = str(data[1])
    address = second.split("</i> ")[1].split(" <a ")[0]
    return npsn[1:], name, address


def get_info_for_link(link):
    response = requests.get(link, timeout=3)
    soup = BeautifulSoup(response.content, 'html.parser')
    body = soup.body

    info = {}
    info["link"] = link

    npsn, name, address = get_npsn_name_address(body.h4.contents)
    info["npsn"] = npsn 
    info["name"] = name 
    info["address"] = address 

    

    return info


def get_info_for_all_links():
    links = read_links()[0]
    print(len(links))
