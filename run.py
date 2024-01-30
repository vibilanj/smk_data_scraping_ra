from get_links import *
from get_info import *

if __name__ == "__main__":
    # print(get_unique_SMK_links())
    # get_unique_SMK_links()

    # links = read_links()
    # links_unique = list(set(links))
    # print(len(links))
    # print(len(links_unique))
    # write_to_csv(links_unique, "SMK_links_unique.csv")

    get_info_for_all_links()
    
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/F2587991-4A7E-4885-ABF3-205321AB493C")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/075648AC-69AA-4554-8A27-539890314311")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/7BDFC19E-DEAE-45E9-ADBE-B61F755ED4F9")

    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/8F4C4C40-20C1-4A30-BCF3-4C50C6578192")
    # print(info)