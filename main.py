"""
main.py: Projekt3 - Elections Scraper

author: Iveta Fridrichová
email: ivet.fridrichova@seznam.cz
"""

import sys
import csv
import requests
from bs4 import BeautifulSoup

def check_args(url, output_file):
    if not (url.startswith("http://") or url.startswith("https://")):
        print("First argument has to be valid url (http/https).")
        sys.exit(1)

    if not output_file.endswith(".csv"):
        print("Second argument has to be CSV file name (e.g. results.csv).")
        sys.exit(1)

    try:
        file = open(output_file, "w")
        file.close()
    except:
        print("Failed to open file.")
        sys.exit(1)

def load_page(url):
  zadana_url = requests.get(url)
  soup = BeautifulSoup(zadana_url.text, "html.parser")
  if zadana_url.ok:
    return soup
  else:
    print("Failed to load page: ", url)
    sys.exit(1)
  
def get_vyber_obce_urls(uzemi_page, url):
    array_a = uzemi_page.find_all("a")
    links = []
    for a in array_a:
        try:
            path = a["href"]
            if path.startswith("ps32"):
                obec_url = url.replace("ps3?xjazyk=CZ", path)
                links.append(obec_url)
        except:
            continue
    
    return links

def get_obec_urls(uzemi_page, url):
    array_a = uzemi_page.find_all("a")
    links = []
    for a in array_a:
        try:
            path = a["href"]
            if path.startswith("ps311"):
                info_url = url.replace("ps3?xjazyk=CZ", path)
                links.append(info_url)
        except:
            continue
        
    return links
        
def get_obce(vyber_obce_page, url):
    obec_list = []
    for tr in vyber_obce_page.select("table tr:nth-of-type(n+3)"):
        tds = tr.select("td")
        if len(tds) > 1 and tds[0].a:
            a = tds[0].a
            key = a.getText()
            name = tds[1].getText()
            obec_path = a["href"]

            parts = url.split("/")
            obec_url = url.replace(parts[-1], obec_path)
            obec_page = load_page(obec_url)

            info_obec = {
                "kod": key,
                "jmeno": name
            }
            info_obec.update(get_obec_info(obec_page))
            obec_list.append(info_obec)
    
    return obec_list

def get_obec_info(info_html):
    obec_info_dict = {}
    tables = info_html.select("table")
    table_1 = tables[0] # volici, obalky, hlasy
    table_2 = tables[1] # strany (1-15)
    table_3 = tables[2] # strany (16-30)

    tr_info = table_1.select("tr")[2]
    td_info = tr_info.select("td")
    obec_info_dict["volici"] = td_info[3].getText().replace('\xa0', ' ')
    obec_info_dict["obalky"] = td_info[4].getText().replace('\xa0', ' ')
    obec_info_dict["hlasy"] = td_info[7].getText().replace('\xa0', ' ')

    tr_strany = table_2.select("tr:nth-of-type(n+3)")
    for tr in tr_strany:
        tds = tr.select("td")
        strana_name  = tds[1].getText()
        strana_hlasy = tds[2].getText().replace('\xa0', ' ')
        obec_info_dict[strana_name] = strana_hlasy
    
    tr_strany_2 = table_3.select("tr:nth-of-type(n+3)")
    for tr in tr_strany_2:
        tds = tr.select("td")
        strana_name  = tds[1].getText()
        strana_hlasy = tds[2].getText().replace('\xa0', ' ')
        if strana_hlasy != "-":
            obec_info_dict[strana_name] = strana_hlasy
    
    return obec_info_dict

def execute_program():
    if len(sys.argv) != 3:
        print("You must enter 2 arguments: [URL] [file.csv]")
        sys.exit(1)

    url = sys.argv[1]
    output_file = sys.argv[2]
    check_args(url, output_file)

    # Process
    vyber_obce_page = load_page(url)
    obec_list = get_obce(vyber_obce_page, url)
    
    # Add missing keys
    obec_list[0].setdefault("Česká národní fronta", "")
    obec_list[0].setdefault("Národ Sobě", "")
    csv_columns = obec_list[0].keys()

    # Write to csv
    csv_soubor = open(output_file, mode="w", encoding="UTF-8")
    writer = csv.DictWriter(csv_soubor, fieldnames=csv_columns, delimiter=";")
    writer.writeheader()
    writer.writerows(obec_list)
    csv_soubor.close()

if __name__ == "__main__":
    execute_program()
