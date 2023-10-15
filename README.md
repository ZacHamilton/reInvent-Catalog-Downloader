# 2023 AWS re:Invent Catalog List Downloader

A Couple of python scripts to download the AWS re:Invent Sessions Catalog and convert to an Excel spreadsheet

Based off: https://github.com/donkersgoed/reinvent-2023-session-fetcher

Forked from: https://github.com/AndyQ/reInvent-Catalog-Downloader

## Prerequisites
Python 3.10

## Setup
- Check out code

- Create python virtual environment
```
python -m venv venv
```

- Install dependancies
```
pip install -r requirements.txt
```

## Usage

There are two scripts:

download.py - downloads the current session catalog to sessions.json
display.py - converts the sessions json file to an Excep Spreadsheet - marking Favourites (if present - see below)

### Downloading the catalog

Run this by entering:
```
python3 download.py
```

You can specify your AWS re:Invent Portal username and password as parameters (see `python download.py --help` for more details)
If not specified you will be prompted to enter them.

### Converting the catalog

For first time - Run this by entering:
```
python3 display.py
```
This will create a reinvent.xlsx
Update the selected and favourites columns as needed.

### After redownloading the catalog and using previous xlsx save
To get updates from AWS and bring over your previous "selected" and "favourites" columns set in your last xlsx
1. Save your reinvent.xlsx to something like so "reinvent_20231015.xlsx"
2. Open "reinvent_20231015.xlsx", then remove filters and re-save

3.  Rerun by entering:
```
python3 display.py reinvent_20231015.xlsx
```

This will create a reinvent.xlsx





