# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 20:31:37 2019

@author: Bryce
"""
import sqlite3
import datetime
import pytz
import os

filename = "diary"
con = sqlite3.connect(filename)
cur = con.cursor()

# Categories currently aren't working :'(
""" categories = {}
cur.execute("SELECT * FROM tableCategoryDiary")
for line in cur.fetchall():
    categories[line[2]] = line[1]
         """

# Datetime stuff
    
    
timezone = pytz.timezone(input("What timezone are you in? Please use tz database name (see github page): \n"))         
print("Thanks :)")

filename_fmt = "%Y-%m-%d"
infile_fmt = "%d/%m/%Y: %H:%M"

    
print("Extracting diary entries")


try:
    os.mkdir("txt_out")

except FileExistsError:
    pass

os.chdir("txt_out")
cwd = os.getcwd()


cur.execute("SELECT entryCategory, entryContent, entryCreatedDate, entryModifiedDate FROM tableDiary ORDER BY entryCreatedDate DESC;")
for row in cur:
    created_utc_time = datetime.datetime.fromtimestamp(row[2]/1000)
    edited_utc_time = datetime.datetime.fromtimestamp(row[3]/1000)
    created_local_time = timezone.localize(created_utc_time)
    edited_local_time = timezone.localize(edited_utc_time)
    
    f = open(created_local_time.strftime(filename_fmt) + ".txt", "w+") #+ " ({}).txt".format(categories[row[0]]), "w+") since categories aren't current working
    string = created_local_time.strftime(infile_fmt)
    if row[2] != row[3]:
        string += " (Last edited: {})".format(edited_local_time.strftime(infile_fmt))
    string += ":\n"
    f.write(string)
    f.write(row[1])
    f.close()
    