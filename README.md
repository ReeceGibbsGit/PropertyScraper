# PropertyScraper

A CLI tool for searching and scraping residential property listings from [realestate.co.nz](https://www.realestate.co.nz).

## Requirements

- Python 3.9+
- pip

## Installation

Clone the repo and install in editable mode:

```bash
git clone https://github.com/ReeceGibbsGit/PropertyScraper.git
cd PropertyScraper
pip install -e .
```

Then add the pip scripts directory to your PATH if prompted (one-time setup). On Windows:

```powershell
$scriptsPath = "$(python -m site --user-site | Split-Path)\Scripts"
[Environment]::SetEnvironmentVariable("PATH", $env:PATH + ";$scriptsPath", "User")
```

Open a new terminal after updating PATH.

## Usage

Run all commands from the repo root (the `output/` directories must be present).

### Search for listings

```bash
property-scraper search --area <area>
```

**Valid areas:**

| Argument | Location |
|---|---|
| `auckland-city` | Auckland City |
| `north-shore-city` | North Shore City |
| `waitakere-city` | Waitakere City |
| `rodney` | Rodney |

**Example:**

```bash
property-scraper search --area north-shore-city
```

Outputs a CSV to `./output/search_results_dump.csv` with columns: `Id`, `Address`, `Link`, `Method of Sale`, `Description`.

---

### Fetch property details

Enriches an existing search results CSV with pricing and description data scraped from each listing page.

```bash
property-scraper fetch-details --csv-dump <path-to-csv>
```

**Example:**

```bash
property-scraper fetch-details --csv-dump ./output/search_results_dump.csv
```

A `.bak` backup of the CSV is created automatically before writing.

> **Note:** Run `search` before `fetch-details`. The fetch step uses the links captured during search.

---

## Typical workflow

```bash
# 1. Search an area
property-scraper search --area auckland-city

# 2. (Optional) Manually edit ./output/search_results_dump.csv to remove unwanted listings

# 3. Fetch full details for remaining listings
property-scraper fetch-details --csv-dump ./output/search_results_dump.csv
```

## Agent usage

See [SKILL.md](./SKILL.md) for instructions on how Claude or OpenClaw can operate this tool autonomously.
