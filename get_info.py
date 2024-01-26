from get_links import read_links
import requests
from bs4 import BeautifulSoup

def get_npsn_name_address(data):
    first = data[0]
    npsn, name = first.split(") ")

    second = str(data[1])
    address = second.split("</i> ")[1].split(" <a ")[0]
    return npsn[1:], name, address


def get_detail_dapodik(data):
    li_list = data.find_all('li')[1:]
    akreditasi = li_list[0].text.split("Akreditasi : ")[-1]
    kepala_sekolah = li_list[1].text.split("Kepala Sekolah : ")[-1]
    operator = li_list[2].a.text

    if operator == "-":
        operator = ""
    return akreditasi, kepala_sekolah, operator


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

    ul_list = body.find_all('ul', class_="list-group list-group")
    
    akreditasi, kepala_sekolah, operator = get_detail_dapodik(ul_list[0])
    info["akreditasi"] = akreditasi
    info["kepala_sekolah"] = kepala_sekolah
    info["operator"] = operator

    print(info)
    return info


def get_info_for_all_links():
    links = read_links()[0]
    print(len(links))
