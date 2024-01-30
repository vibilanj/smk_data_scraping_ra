from get_links import read_links, write_to_csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

def convert_to_int(num_str):
    if num_str == "":
        return None
    return int(num_str.replace(",", ""))

def convert_to_float(num_str):
    return float(num_str.replace(",", ""))

def get_npsn_name_address(data):
    first = data[0]
    npsn, name = first.split(") ")
    npsn = convert_to_int(npsn[1:])

    second = str(data[1])
    address = second.split("</i> ")[1].split(" <a ")[0]
    return npsn, name, address


def get_detail_dapodik(data):
    text = data.text
    akreditasi = text.split("Akreditasi : ")[-1].split("\n")[0]
    kepala_sekolah = text.split("Kepala Sekolah : ")[-1].split("\n")[0]
    operator = text.split("Operator : ")[-1].split("\n")[0]

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
    text = data.text
    akses_internet = text.split("Akses Internet : ")[-1].split("\n")[0]
    sumber_listrik = text.split("Sumber Listrik : ")[-1].split("\n")[0]
    daya_listrik = convert_to_int(text.split("Daya Listrik : ")[-1].split("\n")[0])
    luas_tanah_m2 = convert_to_int(text.split("Luas Tanah : ")[-1].split(" M")[0])
    return akses_internet, sumber_listrik, daya_listrik, luas_tanah_m2


def get_summary_4(data):
    font_list = data.find_all('font')
    ruang_kelas  = convert_to_int(font_list[0].text)
    laboratorium = convert_to_int(font_list[2].text)
    perpustakaan = convert_to_int(font_list[4].text)
    sanitasi_siswa = convert_to_int(font_list[6].text)
    return ruang_kelas, laboratorium, perpustakaan, sanitasi_siswa


def get_proses_pembelajaran(data):
    span_list = data.find_all('span')
    r_siswa_rombel = convert_to_float(span_list[0].text)
    r_siswa_ruang_kelas = convert_to_float(span_list[1].text)
    r_siswa_guru = convert_to_float(span_list[2].text)
    p_guru_kualifikasi = convert_to_float(span_list[3].text)
    p_guru_sertifikasi = convert_to_float(span_list[4].text)
    p_guru_pns = convert_to_float(span_list[5].text)
    p_ruang_kelas_layak = convert_to_float(span_list[6].text)
    return (r_siswa_rombel, r_siswa_ruang_kelas, r_siswa_guru,
            p_guru_kualifikasi, p_guru_sertifikasi, p_guru_pns, p_ruang_kelas_layak)


def get_guru_status(data):
    td_list = data.find_all('td', class_ = "text-right")
    guru_status_pns = convert_to_int(td_list[1].text)
    guru_status_gtt = convert_to_int(td_list[2].text)
    guru_status_gty = convert_to_int(td_list[3].text)
    guru_status_honor = convert_to_int(td_list[4].text)
    return guru_status_pns, guru_status_gtt, guru_status_gty, guru_status_honor


def get_guru_sertifikasi(data):
    td_list = data.find_all('td', class_ = "text-right")
    guru_sertifikasi_sudah = convert_to_int(td_list[1].text)
    guru_sertifikasi_belum = convert_to_int(td_list[2].text)
    return guru_sertifikasi_sudah, guru_sertifikasi_belum


def get_guru_ijazah(data):
    td_list = data.find_all('td', class_ = "text-right")
    guru_ijazah_kurang_dari_S1 = convert_to_int(td_list[1].text)
    guru_ijazah_S1_atau_lebih = convert_to_int(td_list[2].text)
    guru_ijazah_data_kosong = convert_to_int(td_list[3].text)
    return guru_ijazah_kurang_dari_S1, guru_ijazah_S1_atau_lebih, guru_ijazah_data_kosong


def get_guru_jenis_kelamin(data):
    td_list = data.find_all('td', class_ = "text-right")
    guru_jk_laki_laki = convert_to_int(td_list[1].text)
    guru_jk_perempuan = convert_to_int(td_list[2].text)
    return guru_jk_laki_laki, guru_jk_perempuan 


def get_tk_status(data):
    td_list = data.find_all('td', class_ = "text-right")
    tk_status_pns = convert_to_int(td_list[1].text)
    tk_status_honor = convert_to_int(td_list[2].text)
    return tk_status_pns, tk_status_honor


def get_tk_ijazah(data):
    td_list = data.find_all('td', class_ = "text-right")
    tk_total = convert_to_int(td_list[0].text)
    tk_ijazah_kurang_dari_S1 = convert_to_int(td_list[1].text)
    tk_ijazah_S1_atau_lebih = convert_to_int(td_list[2].text)
    tk_ijazah_data_kosong = convert_to_int(td_list[3].text)
    return tk_total, tk_ijazah_kurang_dari_S1, tk_ijazah_S1_atau_lebih, tk_ijazah_data_kosong


def get_tk_jenis_kelamin(data):
    td_list = data.find_all('td', class_ = "text-right")
    tk_jk_laki_laki = convert_to_int(td_list[1].text)
    tk_jk_perempuan = convert_to_int(td_list[2].text)
    return tk_jk_laki_laki, tk_jk_perempuan


def get_nilai_akreditasi(data):
    nilai_akreditasi_tahun = data.text.split("Tahun : ")[-1].split("\n")[0]
    nilai_akreditasi_akhir = convert_to_int(data.text.split("Nilai Akhir : ")[-1].split("\n")[0])
    return nilai_akreditasi_tahun, nilai_akreditasi_akhir

def get_info_for_link(link):
    # response = requests.get(link)
    # response = requests.get(link, timeout=5)
    while True:
        try:
            response = requests.get(link, timeout=5)
            if response.status_code == 200:
                break
            elif response.status_code == 404 or response.status_code == 500:
                return None
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

    r_siswa_rombel, r_siswa_ruang_kelas, r_siswa_guru, p_guru_kualifikasi,\
        p_guru_sertifikasi, p_guru_pns, p_ruang_kelas_layak= get_proses_pembelajaran(ul_list[1])
    info["r_siswa_rombel"] = r_siswa_rombel
    info["r_siswa_ruang_kelas"] = r_siswa_ruang_kelas
    info["r_siswa_guru"] = r_siswa_guru
    info["p_guru_kualifikasi"] = p_guru_kualifikasi
    info["p_guru_sertifikasi"] = p_guru_sertifikasi
    info["p_guru_pns"] = p_guru_pns
    info["p_ruang_kelas_layak"] = p_ruang_kelas_layak

    guru_status_pns, guru_status_gtt, guru_status_gty, guru_status_honor \
        = get_guru_status(body.find('div', id="gurustatus"))
    info["guru_status_pns"] = guru_status_pns
    info["guru_status_gtt"] = guru_status_gtt
    info["guru_status_gty"] = guru_status_gty
    info["guru_status_honor"] = guru_status_honor

    guru_sertifikasi_sudah, guru_sertifikasi_belum = get_guru_sertifikasi(body.find('div', id="gurusertifikasi"))
    info["guru_sertifikasi"] = guru_sertifikasi_sudah
    info["guru_belum_sertifikasi"] = guru_sertifikasi_belum

    guru_ijazah_kurang_dari_S1, guru_ijazah_S1_atau_lebih, guru_ijazah_data_kosong \
        = get_guru_ijazah(body.find('div', id="guruijazah"))
    info["guru_ijazah_kurang_dari_S1"] = guru_ijazah_kurang_dari_S1
    info["guru_ijazah_S1_atau_lebih"] = guru_ijazah_S1_atau_lebih
    info["guru_ijazah_data_kosong"] = guru_ijazah_data_kosong

    guru_jk_laki_laki, guru_jk_perempuan = get_guru_jenis_kelamin(body.find('div', id="gurujeniskelamin"))
    info["guru_jk_laki_laki"] = guru_jk_laki_laki
    info["guru_jk_perempuan"] = guru_jk_perempuan

    tk_status_pns, tk_status_honor = get_tk_status(body.find('div', id="ptkstatus"))
    info["tk_status_pns"] = tk_status_pns
    info["tk_status_honor"] = tk_status_honor

    tk_total, tk_ijazah_kurang_dari_S1, tk_ijazah_S1_atau_lebih, tk_ijazah_data_kosong \
        = get_tk_ijazah(body.find('div', id="ptkijazah"))
    info["tk_total"] = tk_total
    info["tk_ijazah_kurang_dari_S1"] = tk_ijazah_kurang_dari_S1
    info["tk_ijazah_S1_atau_lebih"] = tk_ijazah_S1_atau_lebih
    info["tk_ijazah_data_kosong"] = tk_ijazah_data_kosong

    tk_jk_laki_laki, tk_jk_perempuan = get_tk_jenis_kelamin(body.find('div', id="ptkjeniskelamin"))
    info["tk_jk_laki_laki"] = tk_jk_laki_laki
    info["tk_jk_perempuan"] = tk_jk_perempuan

    nilai_akreditasi_tahun, nilai_akreditasi_akhir = get_nilai_akreditasi(body.find('div', id="dataakreditasi"))
    info["nilai_akreditasi_tahun"] = nilai_akreditasi_tahun
    info["nilai_akreditasi_akhir"] = nilai_akreditasi_akhir

    return info


def get_info_for_all_links():
    df = pd.DataFrame()

    links = read_links()
    broken_links = []
    
    for link in tqdm(links):
        print(link)
        info = get_info_for_link(link)

        if info is None:
            broken_links.append(link)
            continue
        df = pd.concat([df, pd.DataFrame([info])], ignore_index=True)

    df.to_csv("SMK_full_info.csv", index=False)
    write_to_csv(broken_links, "broken_links.csv")
    return df
