# 🔗 URL Wildcard Filter Tool

A Python utility that reads a list of URLs from an Excel file, converts them into wildcard-formatted domain entries, deduplicates them, and exports the results to a structured text file — ideal for use in firewall rules, proxy configurations, or network allowlists.

---

## 📋 Features

- Reads URLs from an `.xlsx` Excel file
- Handles a wide variety of URL formats:
  - Full URLs with or without `http://` / `https://` scheme
  - Subdomains (e.g., `blog.example.com` → `*.example.com/`)
  - Bare domains (e.g., `example.com` → `example.com/`)
  - IP addresses with optional ports (e.g., `192.168.1.1:8080`)
- Automatically deduplicates wildcard entries
- Groups original URLs by their converted wildcard result
- Exports sorted results with a detailed conversion log to `wildcard_urls.txt`
- Prints a summary and grouped results to the terminal

---

## 📁 Project Structure

```
.
├── Tools-URL-Filter.py   # Main script (English version)
├── list_urls.xlsx           # Input file (Excel with URLs in the first column)
└── wildcard_urls.txt        # Output file (auto-generated after running the script)
```

---

## ⚙️ Requirements

- Python 3.7+
- Required libraries:

```bash
pip install pandas tldextract openpyxl
```

| Library       | Purpose                                      |
|---------------|----------------------------------------------|
| `pandas`      | Reading the Excel input file                 |
| `tldextract`  | Accurately parsing domain and TLD components |
| `openpyxl`    | Excel file support (required by pandas)      |

---

## 🚀 Usage

1. **Prepare your input file**

   Create an Excel file named `list_urls.xlsx` in the same directory as the script. Place all URLs in the **first column** with a **header row** in the first row (e.g. `URLs`). The script treats the first row as a header, so any URL placed there will be skipped.

   Example:

   | URLs                              |
   |-----------------------------------|
   | python.org/                       |
   | https://mail.google.com/mail      |
   | api.example.com                   |
   | 192.168.1.100:8080                |
   | https://www.github.com/user/repo  |

   > ⚠️ **Important:** Always include a header in the first row. If you place a URL in row 1 without a header, it will be treated as the column name and **will not be processed**.

2. **Run the script**

   ```bash
   python Tools-URL-Filter.py
   ```

3. **Check the output**

   - Terminal: displays a grouped summary of all conversions
   - File: `wildcard_urls.txt` is created/overwritten with a full log

---

## 📤 Output Example

### Terminal output

```
Total URLs read: 4
Total wildcards generated: 3

Conversion results (Grouped):

*.github.com/:
  https://www.github.com/user/repo

*.google.com/:
  https://mail.google.com/mail

192.168.1.100:8080/:
  192.168.1.100:8080

example.com/:
  api.example.com
```

### `wildcard_urls.txt` structure

```
Process Log (2025-01-01 12:00:00):
Successfully read file: list_urls.xlsx
Total rows of data: 4
Total URLs read: 4
Total wildcards generated: 3

Wildcard URL List:
*.github.com/
*.google.com/
192.168.1.100:8080/
example.com/

--------------------------------------------------

Detailed Conversion Log (Grouped):

*.github.com/:
  https://www.github.com/user/repo

*.google.com/:
  https://mail.google.com/mail
...
```

---

## 🔄 Conversion Logic

| Input URL                         | Output Wildcard       |
|-----------------------------------|-----------------------|
| `https://mail.google.com`         | `*.google.com/`       |
| `https://www.example.com/page`    | `*.example.com/`      |
| `example.com`                     | `example.com/`        |
| `api.example.com`                 | `*.example.com/`      |
| `192.168.1.1`                     | `192.168.1.1/`        |
| `192.168.1.1:8080`                | `192.168.1.1:8080/`   |

**Rules:**
- If the URL has a subdomain → prefix with `*.`
- If the URL has no subdomain → use bare domain
- IP addresses are kept as-is (no wildcard)
- Port numbers are preserved when present
- All results end with a trailing `/`
- Duplicate wildcard results are removed automatically

---

## 📝 Notes

- The script expects URLs to be in the **first column** of the Excel file, starting from **row 2** (row 1 is treated as the header). To use a different column, modify the `df.iloc[:, 0]` line in the script.
- The output file `wildcard_urls.txt` is **overwritten** on each run.
- URLs without a scheme (`http://`, `https://`) are handled automatically — a dummy `http://` is prepended for parsing purposes only.

---

## 📄 License

This project is open-source. Feel free to use, modify, and distribute it as needed.
