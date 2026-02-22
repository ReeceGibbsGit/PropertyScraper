import httpx
import random
import time 
import os

valid_areas = ["waitakere-city", "north-shore-city", "auckland-city", "rodney"]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/122.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0"
]

def fetch_and_dump_html(urls, output_directory="./output"):
    output_filenames = []

    with httpx.Client(timeout=10.0) as client:
        for i, url in enumerate(urls):
            print(f"Fetching: {url}...")
            
            current_headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Referer": "https://www.google.com/"
            }

            try:
                response = client.get(url, headers=current_headers, follow_redirects=True)
                
                response.raise_for_status()

                print(f"Success: {url}")

                output_filename = f"property_data_{i+1}.html"
                output_filenames.append(output_filename)

                with open(os.path.join(output_directory, output_filename), "w", encoding="utf-8") as f:
                    f.write(response.text)
                
                time.sleep(random.uniform(1.5, 3.0))

            except httpx.HTTPStatusError as e:
                print(f"Error: {e.response.status_code} for {url}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            
    return output_filenames

def buildUrl(area, page):
    return f"https://www.realestate.co.nz/residential/sale/auckland/{area}?by=latest&maxp=950000&minba=1&minbe=2&mincp=1&minp=850000&pm=1%2C2%2C6%2C7&scat=1%2C7&page={page}"

def buildUrls(area, numOfPages):
    return [buildUrl(area, i) for i in range(1, numOfPages + 1)]

