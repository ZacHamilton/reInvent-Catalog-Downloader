# AWS re:Invent Catalog List Downloader

A Couple of python scripts to download the AWS re:Invent Sessions Catalog and convert to an Excel spreadsheet

Based off: https://github.com/donkersgoed/reinvent-2023-session-fetcher

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

Run this by entering:
```
python3 display.py
```

This will create a reinvent_sessions.xlsx

### Adding favourites
The display script will highlight any favourites you have marked if you create a file favourites.txt containing a list of favourite session ids (one per line).

e.g.
```
ANT329
DOP310
BOA307
CMP324
```



