#!/usr/bin/env python3

import json
import pandas as pd
from datetime import datetime, timezone
import pytz

def toExcelDate( d ):
    if d != None:
        return d.strftime('%x %X')
    else:
        return None


def autosize_excel_columns(worksheet, df, cell_format):
  autosize_excel_columns_df(worksheet, df.index.to_frame(), cell_format)
  autosize_excel_columns_df(worksheet, df, cell_format, offset=df.index.nlevels)

def autosize_excel_columns_df(worksheet, df, cell_format, offset=0):
    for idx, col in enumerate(df):
        series = df[col]
        max_len = min(80, max((
            series.astype(str).map(len).max(),
            len(str(series.name)))
        )) + 1

        worksheet.set_column(idx+offset, idx+offset, max_len, cell_format=cell_format)

def bold_favourites(worksheet, df, bold_format):
    #  Bold Favourites
    offset = 1
    ids = df.index[df['Favourite'] == "*"].tolist()

    for row in ids:
        for idx, col in enumerate(df):
            worksheet.set_row(row+offset, None, bold_format)



def addItem( dfs, type, session ):
    df = dfs.get(type, None)
    if df is None:
        df = {
                "Favourite": [],
                "ID": [],
                "SessionLevel": [],
                "Title": [],
                "Description": [],
                "Type": [],
                "Track Name": [],
                "Venue": [],
                "Day": [],
                "StartTime": [],
                "EndTime": [],
        }
        dfs[type] = df

    df["Favourite"].append(session['favourite'])
    df["ID"].append(session['thirdPartyID'])
    df["Title"].append(session['title'])
    df["SessionLevel"].append(session_level)
    df["Description"].append(session['description'])
    df["Type"].append(session['sessionType'])
    df["Track Name"].append(session['trackName'])
    df["Venue"].append(venue)
    df["Day"].append(day)
    df["StartTime"].append(toExcelDate(startTime))
    df["EndTime"].append(toExcelDate(endTime))



try:
    with open( "favourites.txt", "r" ) as f:
        favouritesList = [line.strip() for line in f]
except:
    print( "No favourites list found" )
    favouritesList = []

with open("sessions.json", "r") as f:
    sessions = json.load(f)

    
print( f"There are currently {len(sessions)} sessions" )

items = {}
# Display the sessionType, trackName, thirdPartyID, title, and description for each session
for session in sessions:

    type = session['sessionType']

    startTime = session['startDateTime']
    endTime = session['endDateTime']
    if startTime != "":
        startTime = datetime.fromtimestamp(startTime, timezone.utc).astimezone(pytz.timezone('America/Los_Angeles'))
    else:
        startTime = None
    if endTime != "":
        endTime = datetime.fromtimestamp(endTime, timezone.utc).astimezone(pytz.timezone('America/Los_Angeles'))
    else:
        endTime = None

    session["startTime"] = startTime
    session["endTime"] = endTime

    # Extract session level
    if len(session['thirdPartyID']) >= 4:
        session_level = int(session['thirdPartyID'][3])
    else:
        session_level = 0
    session["sessionLevel"] = session_level

    # Get venue and date from tags
    # each tag has a parentTagName of either Venue or Day
    # and we want the tagName
    venue = ""
    day = ""
    for tag in session['tags']:
        if tag['parentTagName'] == "Venue":
            venue = tag['tagName']
        if tag['parentTagName'] == "Day":
            day = tag['tagName']

    session["venue"] = venue
    session["day"] = day

    # is a favourite?
    session["favourite"] = "*" if session["thirdPartyID"] in favouritesList else ""

    if session["favourite"]:
        addItem( items, "Favourites", session )
    addItem( items, "ALL", session )
    addItem( items, type, session )


with pd.ExcelWriter('reinvent_sessions.xlsx', engine='xlsxwriter') as writer:
    workbook = writer.book
    cell_format = workbook.add_format({'text_wrap': True})
    bold_format = workbook.add_format({'bold': 1, 'text_wrap': True})

    # Get the list of keys and move the ALL and Favourites to the top
    keys = list(items.keys())

    if "ALL" in keys: 
        keys.remove("ALL")
        keys.insert(0, "ALL")
    if "Favourites" in keys: 
        keys.remove("Favourites")
        keys.insert(1, "Favourites")

    for key in keys:
        df = pd.DataFrame(items[key])

        df.to_excel(writer, sheet_name=key, index=False)
        worksheet = writer.sheets[key]

        autosize_excel_columns(worksheet, df, cell_format)
        bold_favourites(worksheet, df, bold_format)
