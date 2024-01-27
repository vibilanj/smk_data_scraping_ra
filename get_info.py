from get_links import read_links
import requests
from bs4 import BeautifulSoup

def convert_to_int(num_str):
    return int(num_str.replace(",", ""))

def get_npsn_name_address(data):
    first = data[0]
    npsn, name = first.split(") ")
    npsn = convert_to_int(npsn[1:])

    second = str(data[1])
    address = second.split("</i> ")[1].split(" <a ")[0]
    return npsn, name, address


def get_detail_dapodik(data):
    li_list = data.find_all('li')[1:]
    akreditasi = li_list[0].text.split("Akreditasi : ")[-1]
    kepala_sekolah = li_list[1].text.split("Kepala Sekolah : ")[-1]
    operator = li_list[2].a.text

    if operator == "-":
        operator = ""
    return akreditasi, kepala_sekolah, operator


def get_summary_1(data):
    font_list = data.find_all('font')
    guru = convert_to_int(font_list[0].text)
    siswa_l = convert_to_int(font_list[1].text)
    siswa_p = convert_to_int(font_list[2].text)
    rombongan_belajar = convert_to_int(font_list[3].text)
    return guru, siswa_l, siswa_p, rombongan_belajar


def get_summary_2(data):
    font_list = data.find_all('font')
    kurikulum = font_list[0].text.replace('\xa0', ' ')
    penyelenggaraan = data.text.split("Penyelenggaraan : ")[-1].split("\n")[0]
    
    mbs_icon = data.find('i', class_="glyphicon-check")
    mbs = str(mbs_icon is not None)

    semester_data = font_list[1].text
    return kurikulum, penyelenggaraan, mbs, semester_data


def get_summary_3(data):
    akses_internet = data.text.split("Akses Internet : ")[-1].split("\n")[0]
    sumber_listrik = data.text.split("Sumber Listrik : ")[-1].split("\n")[0]

    font_list = data.find_all('font')
    daya_listrik = convert_to_int(font_list[0].text)
    luas_tanah_m2 = convert_to_int(font_list[1].text)
    return akses_internet, sumber_listrik, daya_listrik, luas_tanah_m2


def get_summary_4(data):
    font_list = data.find_all('font')
    ruang_kelas  = convert_to_int(font_list[0].text)
    laboratorium = convert_to_int(font_list[2].text)
    perpustakaan = convert_to_int(font_list[4].text)
    sanitasi_siswa = convert_to_int(font_list[6].text)
    return ruang_kelas, laboratorium, perpustakaan, sanitasi_siswa

def get_info_for_link(link):
    # response = requests.get(link)
    # response = requests.get(link, timeout=5)

    while True:
        try:
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                break
            # If 404, then add to list of failed links
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

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

    summary_divs = body.find_all('div', class_ = "row")[2].find_all('div')
    
    guru, siswa_l, siswa_p, rombongan_belajar = get_summary_1(summary_divs[0])
    info["guru"] = guru
    info["siswa_l"] = siswa_l
    info["siswa_p"] = siswa_p
    info["rombongan_belajar"] = rombongan_belajar

    kurikulum, penyelenggaraan, mbs, semester_data = get_summary_2(summary_divs[1])
    info["kurikulum"] = kurikulum
    info["penyelenggaraan"] = penyelenggaraan
    info["mbs"] = mbs 
    info["semester_data"] = semester_data

    akses_internet, sumber_listrik, daya_listrik, luas_tanah_m2 = get_summary_3(summary_divs[2])
    info["akses_internet"] = akses_internet
    info["sumber_listrik"] = sumber_listrik
    info["daya_listrik"] = daya_listrik
    info["luas_tanah_m2"] = luas_tanah_m2

    ruang_kelas, laboratorium, perpustakaan, sanitasi_siswa = get_summary_4(summary_divs[3])
    info["ruang_kelas"] = ruang_kelas
    info["laboratorium"] = laboratorium
    info["perpustakaan"] = perpustakaan
    info["sanitasi_siswa"] = sanitasi_siswa

    print(info)
    return info


def get_info_for_all_links():
    links = read_links()[0]
    print(len(links))
