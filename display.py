#!/usr/bin/env python3

import json
import xlsxwriter

from datetime import datetime, timezone
import pytz

sessions = []
favouritesList = []
items = {}

def toExcelDate( d ):
    if d != None:
        return d.strftime('%x %X')
    else:
        return None

def addItem( dfs, type, session ):

    category = dfs.get(type, None)
    if category is None:
        category = []
        dfs[type] = category

    item = {}
    item["Favourite"] = session['favourite']
    item["FavoriteAWS"] = session['isFavorite']
    item["ID"] = session['thirdPartyID']
    item["Title"] = session['title']
    item["SessionLevel"] = session['sessionLevel']
    item["Description"] = session['description']
    item["Type"] = session['sessionType']
    item["TrackName"] = session['trackName']
    item["Venue"] = session['venue']
    item["Day"] = session['day']
    item["StartTime"] = toExcelDate(session['startTime'])
    item["EndTime"] = toExcelDate(session['endTime'])
    
    simple_tag_name = ""
    for t in session['tags']:
        simple_tag_name = simple_tag_name + t['parentTagName'].replace(" ", "_").lower() + ": " + t['tagName'] + ", "
    item["Tags"] = simple_tag_name
    
    category.append(item)

def loadFavourites():
    global sessions, favouritesList
    try:
        with open( "favourites.txt", "r" ) as f:
            favouritesList = [line.strip() for line in f]
    except:
        print( "No favourites list found" )
        favouritesList = []

    with open("sessions.json", "r") as f:
        sessions = json.load(f)

    
def parseSessions():
    global items
    print( f"There are currently {len(sessions)} sessions" )

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

def writeExcel():
    global items

    workbook = xlsxwriter.Workbook("reinvent.xlsx")
    workbook.set_size(1400, 1000)

    cell_format = workbook.add_format({'text_wrap': True, "font_size": 14})
    bold_format = workbook.add_format({'bold': 1, 'text_wrap': True, "font_size": 14})

    # Get the list of keys and move the ALL and Favourites to the top
    keys = list(items.keys())

    if "ALL" in keys: 
        keys.remove("ALL")
        keys.insert(0, "ALL")
    if "Favourites" in keys: 
        keys.remove("Favourites")
        keys.insert(1, "Favourites")

    for key in keys:
        category = items[key]
        worksheet = workbook.add_worksheet(key)

        # Write the header row
        worksheet.write(0, 0, "Favourite", bold_format)
        worksheet.write(0, 1, "FavoriteAWS", bold_format)
        worksheet.write(0, 2, "ID", bold_format)
        worksheet.write(0, 3, "SessionLevel", bold_format)
        worksheet.write(0, 4, "Title", bold_format)
        worksheet.write(0, 5, "Description", bold_format)
        worksheet.write(0, 6, "Type", bold_format)
        worksheet.write(0, 7, "TrackName", bold_format)
        worksheet.write(0, 8, "Venue", bold_format)
        worksheet.write(0, 9, "Day", bold_format)
        worksheet.write(0, 10, "StartTime", bold_format)
        worksheet.write(0, 11, "EndTime", bold_format)
        worksheet.write(0, 12, "Tags", bold_format)

        row = 1
        for item in category:
            format = bold_format if item["Favourite"] == "*" else cell_format 

            worksheet.write(row, 0, item["Favourite"], format)
            worksheet.write(row, 1, item["FavoriteAWS"], format)
            worksheet.write(row, 2, item["ID"], format)
            worksheet.write(row, 3, item["SessionLevel"], format)
            worksheet.write(row, 4, item["Title"], format)
            worksheet.write(row, 5, item["Description"], format)
            worksheet.write(row, 6, item["Type"], format)
            worksheet.write(row, 7, item["TrackName"], format)
            worksheet.write(row, 8, item["Venue"], format)
            worksheet.write(row, 9, item["Day"], format)
            worksheet.write(row, 10, item["StartTime"], format)
            worksheet.write(row, 11, item["EndTime"], format)
            worksheet.write(row, 12, item["Tags"], format)

            row += 1

        columns = [
            {"index": 0, "width": 12},
            {"index": 1, "width": 16},
            {"index": 2, "width": 20},
            {"index": 3, "width": 15},
            {"index": 4, "width": 80},
            {"index": 5, "width": 110},
            {"index": 6, "width": 20},
            {"index": 7, "width": 20},
            {"index": 8, "width": 20},
            {"index": 9, "width": 20},
            {"index": 10, "width": 20},
            {"index": 11, "width": 20},
            {"index": 12, "width": 110},
        ]
        for column in columns:
            worksheet.set_column(column["index"], column["index"], column["width"], column.get("options"))
    workbook.close()

        # df.to_excel(writer, sheet_name=key, index=False)
        # worksheet = writer.sheets[key]

        # autosize_excel_columns(worksheet, df, cell_format)
        # bold_favourites(worksheet, df, bold_format)


if __name__ == "__main__":
    loadFavourites()
    parseSessions()
    writeExcel()
