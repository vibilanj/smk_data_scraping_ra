# from get_links import *
# from get_info import *
from get_dates import *

import asyncio
import time

if __name__ == "__main__":
    # print(get_unique_SMK_links())
    # get_unique_SMK_links()

    # links = read_links()
    # links_unique = list(set(links))
    # print(len(links))
    # print(len(links_unique))
    # write_to_csv(links_unique, "SMK_links_unique.csv")

    # get_info_for_all_links()
    
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/F2587991-4A7E-4885-ABF3-205321AB493C")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/075648AC-69AA-4554-8A27-539890314311")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/7BDFC19E-DEAE-45E9-ADBE-B61F755ED4F9")

    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/8F4C4C40-20C1-4A30-BCF3-4C50C6578192")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/AE6D9911-C5BA-467A-B187-B9962B3FBC96")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/BB86AC1D-BD71-4CBF-B711-ED6B83D3E8E3")
    # info = get_info_for_link("https://sekolah.data.kemdikbud.go.id/index.php/Chome/profil/C2190AF1-6420-4554-9171-6D1591662BF7")

    # info = get_info_for_link("")
    # print(info)

    # start = time.time()
    # results = asyncio.run(get_all_html_pages())
    # end = time.time()
    # print(end - start)

    # asyncio.run(get_all_html_pages())
    # pages = read_list_from_pickle()
    # print(get_info_from_page(pages[0][0], pages[0][1]))

    # part = 1

    # start = time.time()
    # asyncio.run(get_all_html_pages(part))
    # end = time.time()
    # print(f"Downloading pages finished: {end - start}s \n")

    # get_info_for_all_links(part)

    # combine_info_csvs()
    # combine_broken_links_csvs()

    # links = read_from_csv("broken_links_combined.csv")
    # print(links)
    # get_info_for_all_links_with_scraping()

    # links = read_from_csv("broken_links_second.csv")
    # link = links[0]
    # response = requests.get(link, timeout = 5)
    # info = get_info_from_broken_page(link, response.content)
    # print(info)

    # get_info_for_broken_links()
    # get_info_for_scrape_error_links()

    # combine_info_csvs()
    
    # New variables needed
    start = time.time()
    results = asyncio.run(scrape_all_pages(1))
    end = time.time()
    print(end - start)

    # combine_and_save("dates.csv")