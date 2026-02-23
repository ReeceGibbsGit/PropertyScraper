import argparse
import os
from fetch_pages import valid_areas, buildUrls, buildUrl, fetch_and_dump_html
from scrape_and_dump import scrape_search_results_and_dump, get_page_count

parser = argparse.ArgumentParser(description="Fetch and scrape property listings from realestate.co.nz")
subparsers = parser.add_subparsers(dest="command")

search_parser = subparsers.add_parser("search", help="Search for property listings")
search_parser.add_argument("--area", required=True, choices=valid_areas, help="Target area to search")

fetch_details_parser = subparsers.add_parser("fetch-details", help="Fetch details for properties in a CSV dump")
fetch_details_parser.add_argument("--csv-dump", required=True, help="Path to the target property CSV dump")

args = parser.parse_args()

if args.command == "fetch-details":
    pass
elif args.command != "search":
    parser.print_help()
    exit(1)

print("Clearing output directory...")
for f in os.listdir("./output"):
    file_path = os.path.join("./output", f)
    if os.path.isfile(file_path):
        os.remove(file_path)

for f in os.listdir("./output/search-results"):
    file_path = os.path.join("./output/search-results", f)
    if os.path.isfile(file_path):
        os.remove(file_path)

print(f"Fetching initial page for area: {args.area}")
initial_url = buildUrl(args.area, 1)
output_filenames = fetch_and_dump_html([initial_url], "search_results", "./output/search-results")

print(f"Getting page count for area: {args.area}")
page_count = get_page_count(output_filenames[0], "./output/search-results")

print(f"Page count: {page_count}")
print(f"Building subsequent urls...")
subsequent_urls = buildUrls(args.area, page_count)[1:]

print(f"Fetching all pages for area: {args.area}")
fetch_and_dump_html(subsequent_urls, "search_results", "./output/search-results", 2)

print("Scraping fetched pages and writing to CSV...")
scrape_search_results_and_dump()

print("Done.")
