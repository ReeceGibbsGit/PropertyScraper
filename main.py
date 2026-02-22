import argparse
import os
from fetch_pages import valid_areas, buildUrls, buildUrl, fetch_and_dump_html
from scrape_and_dump import scrape_all_and_dump, get_page_count

parser = argparse.ArgumentParser(description="Fetch and scrape property listings from realestate.co.nz")
parser.add_argument("--area", required=True, choices=valid_areas, help="Target area to search")

args = parser.parse_args()

print("Clearing output directory...")
for f in os.listdir("./output"):
    file_path = os.path.join("./output", f)
    if os.path.isfile(file_path):
        os.remove(file_path)

print(f"Fetching initial page for area: {args.area}")
initial_url = buildUrl(args.area, 1)
output_filenames = fetch_and_dump_html([initial_url])

print(f"Getting page count for area: {args.area}")
page_count = get_page_count(output_filenames[0])

print(f"Page count: {page_count}")
print(f"Building subsequent urls...")
subsequent_urls = buildUrls(args.area, page_count)[1:]

print(f"Fetching all pages for area: {args.area}")
fetch_and_dump_html(subsequent_urls)

print("Scraping fetched pages and writing to CSV...")
scrape_all_and_dump()

print("Done.")
