import os
import csv
from bs4 import BeautifulSoup

csv_header = ["Address", "Link", "Method of Sale", "Description"]

def scrape_search_results_and_dump_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")

    addressElements = soup.find_all(attrs={"data-test": "standard-tile__search-result__address"})
    addressElements = [el.get_text(strip=True) for el in addressElements]

    links = [a['href'] for a in soup.find_all('a', class_='listing-tile-info')]

    assert len(addressElements) == len(links), "Addresses did not line up with links"

    return [[addressElements[i], "https://www.realestate.co.nz" + links[i], "", ""] for i in range(len(addressElements))]

def scrape_search_results_and_dump(search_results_dir="./output/search-results", output_dir="./output", output_filename="search_results_dump.csv"):
    files = os.listdir(search_results_dir)
    files_only = [f for f in files if os.path.isfile(os.path.join(search_results_dir, f))]

    data = []

    for path in files_only:
        data.extend(scrape_search_results_and_dump_from_file(f"{search_results_dir}/{path}"))

    with open(f"{output_dir}/{output_filename}", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(csv_header)
        writer.writerows(data)

def get_page_count(filename, directory="./output"):
    with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")

    page_number_elements = soup.find_all("a", class_="paginated-items__page-name")
    last_page = int(page_number_elements[-1].get_text(strip=True))
    assert isinstance(last_page, int), "Could not get page count"

    return last_page