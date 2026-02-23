import os
import csv
import shutil
from bs4 import BeautifulSoup

csv_header = ["Id", "Address", "Link", "Method of Sale", "Description"]

def scrape_search_results_and_dump_from_file(path, auto_assign_ids=False):
    with open(path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "lxml")

    addressElements = soup.find_all(attrs={"data-test": "standard-tile__search-result__address"})
    addressElements = [el.get_text(strip=True) for el in addressElements]

    links = [a['href'] for a in soup.find_all('a', class_='listing-tile-info')]

    assert len(addressElements) == len(links), "Addresses did not line up with links"

    return [[i+1 if auto_assign_ids else 0, addressElements[i], "https://www.realestate.co.nz" + links[i], "", ""] for i in range(len(addressElements))]

def scrape_search_results_and_dump(search_results_dir="./output/search-results", output_dir="./output", output_filename="search_results_dump.csv"):
    files = os.listdir(search_results_dir)
    files_only = [f for f in files if os.path.isfile(os.path.join(search_results_dir, f))]

    data = []

    for path in files_only:
        data.extend(scrape_search_results_and_dump_from_file(f"{search_results_dir}/{path}"))

    for i, row in enumerate(data):
        row[0] = i+1

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

def scrape_property_details(property_pages_dir="./output/property-pages", csv_path="./output/search_results_dump.csv"):
    files = os.listdir(property_pages_dir)
    files_only = [f for f in files if os.path.isfile(os.path.join(property_pages_dir, f))]

    with open(csv_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    rows_by_id = {row["Id"]: row for row in rows}

    for filename in files_only:
        # Extract suffix from filename, e.g. "property_page_42.html" -> "42"
        name, _ = os.path.splitext(filename)
        suffix = name.split("_")[-1]

        with open(os.path.join(property_pages_dir, filename), "r", encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "lxml")

        price_el = soup.find(attrs={"data-test": "pricing-method__price"})
        desc_el = soup.find(attrs={"data-test": "description-content__description"})

        price = price_el.get_text(strip=True) if price_el else ""
        description = desc_el.get_text(strip=True) if desc_el else ""

        if suffix in rows_by_id:
            rows_by_id[suffix]["Method of Sale"] = price
            rows_by_id[suffix]["Description"] = description

    backup_path = csv_path + ".bak"
    shutil.copy2(csv_path, backup_path)
    print(f"CSV backed up to {backup_path}")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_header)
        writer.writeheader()
        writer.writerows(rows)