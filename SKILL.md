# Property Scraper Skill

You have access to the `property-scraper` CLI tool. Use it to search and retrieve property listings from realestate.co.nz. Follow the workflow below precisely.

---

## Workflow Overview

```
1. SEARCH  →  2. FILTER (optional)  →  3. FETCH DETAILS  →  4. SEMANTIC FILTER (optional)
```

Steps must be followed in order. You cannot run `fetch-details` before `search`.

---

## Step 1 — Search

Run a property search for a given area.

```
property-scraper search --area <area>
```

**Valid areas:**
- `waitakere-city`
- `north-shore-city`
- `auckland-city`
- `rodney`

**Example trigger:** _"Run a property search for me in North Shore City"_
```
property-scraper search --area north-shore-city
```

This produces a CSV dump at `./output/search_results_dump.csv` with columns:
`Id`, `Address`, `Link`, `Method of Sale`, `Description`

---

## Step 2 — Address Filtering (optional, but must happen before Step 3)

If the user asks to filter addresses (e.g. exclude townhouses, lots, or by any address keyword), apply the filter **directly to the CSV** before fetching details. This avoids wasting time fetching details for unwanted listings.

**How to filter:**
Read the CSV, remove rows that match the filter criteria, and overwrite the file. Use Python to do this:

```python
import csv

csv_path = "./output/search_results_dump.csv"

with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

filtered = [row for row in rows if <filter_condition>]

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "Address", "Link", "Method of Sale", "Description"])
    writer.writeheader()
    writer.writerows(filtered)
```

**Common filter examples:**

| User request | Filter condition |
|---|---|
| "Exclude listings with 'Lot' in the address" | `"Lot" not in row["Address"]` |
| "Only show listings on a named street (no lots/units)" | `not row["Address"].startswith("Lot")` |
| "Exclude anything with 'Unit' in the address" | `"Unit" not in row["Address"]` |

Adapt the condition to whatever the user specifies. Multiple filters can be chained with `and`.

After filtering, inform the user how many listings remain.

---

## Step 3 — Fetch Details

Fetch full property details (price/method of sale, description) for all listings in a CSV dump. This enriches the CSV in place.

```
property-scraper fetch-details --csv-dump <csv_path>
```

**Example trigger:** _"Fetch details for all listings in property_dump.csv"_
```
property-scraper fetch-details --csv-dump ./property_dump.csv
```

- If the user does not provide a CSV path, ask: _"Which CSV file should I fetch details for?"_
- The default output from Step 1 is `./output/search_results_dump.csv`
- This step must only be run after Step 1 (search) has been completed

---

## Step 4 — Semantic Detail Filtering (optional, must happen after Step 3)

If the user asks to filter based on the content of property details, read the enriched CSV and evaluate each row using your own judgement. This step requires the `Method of Sale` and `Description` fields to be populated, so it can only run after Step 3.

Unlike Step 2 (which uses simple string matching on the address), this step involves **reading and interpreting the values** in each row and deciding whether the property meets the user's requirements.

**How to perform semantic filtering:**

1. Read the CSV into memory
2. For each row, evaluate all relevant fields (`Method of Sale`, `Description`, `Address`) against the user's criteria using your understanding of the content — not just keyword matching
3. Separate rows into `kept` and `removed` lists
4. Overwrite the CSV with only the kept rows
5. List every removed property to the user afterwards

```python
import csv

csv_path = "./output/search_results_dump.csv"

with open(csv_path, "r", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

kept = []
removed = []

for row in rows:
    if <your_semantic_judgement_of_row>:
        kept.append(row)
    else:
        removed.append(row)

with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "Address", "Link", "Method of Sale", "Description"])
    writer.writeheader()
    writer.writerows(kept)
```

**Examples of semantic filter criteria and what to look for:**

| User request | What to evaluate |
|---|---|
| "Only keep properties listed by auction" | `Method of Sale` contains "Auction" |
| "Exclude properties that mention body corporate" | `Description` references body corporate, fees, or shared ownership |
| "Only keep standalone houses, no apartments" | `Description` or `Address` suggests an apartment, unit, or multi-storey complex |
| "Only keep properties with a garage" | `Description` mentions garage, internal access, or off-street parking |
| "Exclude properties under renovation" | `Description` uses terms like "do-up", "renovation", "as-is", "fixer" |

Use your best judgement when the criteria are ambiguous — err on the side of keeping a listing if you are unsure.

**After filtering, always report:**

- How many listings remain
- A list of every removed property in this format:

```
Removed listings:
- #<Id> — <Address> (<reason>)
- #<Id> — <Address> (<reason>)
...
```

---

## Notes

- The tool writes output files relative to the **current working directory**, so run commands from a directory that has an `output/`, `output/search-results/`, and `output/property-pages/` folder structure (this already exists inside the project directory).
- A `.bak` backup of the CSV is automatically created before `fetch-details` writes to it.
