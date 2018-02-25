# timesfeature.py
# get the prayer times for today or any given day (times are for this calendar year)

import datetime
import pytz
import subprocess
import os
import json
import pandas as pd

# converts a three letter month code and converts it into it's respective number, e.g. Jan = 1
# used for the date in the text message
def monthToNum(monthCode):
    return{
                'jan' : 1,
                'feb' : 2,
                'mar' : 3,
                'apr' : 4,
                'may' : 5,
                'jun' : 6,
                'jul' : 7,
                'aug' : 8,
                'sep' : 9, 
                'oct' : 10,
                'nov' : 11,
                'dec' : 12
        }[monthCode]

# given the monthCode (1 to 12)
# get the filename to look into for the prayer times
def fileNameLookup(month, strYear):
    monthCode = None
    
    if month == 1:
        monthCode = "jan-" + strYear
    elif month == 2:
        monthCode = "feb-" + strYear
    elif month == 3:
        monthCode = "mar-" + strYear
    elif month == 4:
        monthCode = "apr-" + strYear
    elif month == 5:
        monthCode = "may-" + strYear
    elif month == 6:
        monthCode = "jun-" + strYear
    elif month == 7:
        monthCode = "jul-" + strYear
    elif month == 8:
        monthCode = "aug-" + strYear
    elif month == 9: 
        monthCode = "sep-" + strYear
    elif month == 10:
        monthCode = "oct-" + strYear
    elif month == 11:
        monthCode = "nov-" + strYear
    else:
        monthCode = "dec-" + strYear
        
    return monthCode

def checkUserInputDate(date, year):
    
    now = None
    day = None
    month = None
    date_today = None
    
    if date:
        # split and store input arguments
        day = date[0]
        month = date[1]

        # get number of month for further calculations
        month = monthToNum(month.lower())
        
        dateString = str(year) + "-" + str(month) + "-" + str(day)
        prayerDate = datetime.datetime.strptime(dateString, '%Y-%m-%d')

        day = prayerDate.day
        month = prayerDate.month
        date_today = str(day) + "/" + str(month) + "/" + str(year)

    else:
        now = datetime.datetime.now(pytz.timezone('Europe/London'))
        day = now.day
        month = now.month
        date_today = str(day) + "/" + str(month) + "/" + str(year)
    
    return [day, month, date_today]

# get the cell position for the given date
def getCellNumber(day):
    dayCell = str(day)
    return dayCell

# get prayer times given the cellRange
def getPrayerTimes(filename, cellNumber):
    filepath = "times\elm-" + filename + ".csv"
    times_data = pd.read_csv(filepath, encoding = "latin1")
    
    times_data = times_data.iloc[[cellNumber]]
    times_data = times_data.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12]].values.tolist()
    
    return times_data

# compose the message which will have the prayer times
def composeMessage(prayerTimes, date_today):
    
    times = prayerTimes[[0][0]]
    
    intro = "Prayer Times for (" + date_today + ") are:" + "\n\n"

    fajr_begins = "Fajr Begins - " + times[0] + "\n"
    fajr_jamaah = "Fajr Jama'ah - " + times[1] + "\n"

    sunrise = "Sunrise - " + times[2] + "\n"

    zuhr_begins = "Zuhr Begins - " + times[3] + "\n"
    zuhr_jamaah = "Zuhr Jama'ah - " + times[4] + "\n"

    asr_mithl1 = "Asr Mithl 1 - " + times[5] + "\n"
    asr_mithl2 = "Asr Mithl 2 - " + times[6] + "\n"
    asr_jamaah = "Asr Jama'ah - " + times[7] + "\n"

    maghrib_begins = "Maghrib Begins - " + times[8] + "\n"
    maghrib_jamaah = "Maghrib Jama'ah - "  + times[9] + "\n"

    isha_begins = "Isha Begins - " + times[10] + "\n"
    isha_jamaah = "Isha Jama'ah - " + times[11]

    msg = intro + fajr_begins + fajr_jamaah + sunrise + zuhr_begins + zuhr_jamaah + asr_mithl1 + asr_mithl2 + asr_jamaah + maghrib_begins + maghrib_jamaah + isha_begins + isha_jamaah
    
    return(msg)

# create the message contents of the prayer times message
# incoming 'date' variable will have something like ['25', 'Jan']
def construct_schedule(date):

    # GLOBAL VARIABLES
    # to be changed at the start of a new year
    year = 2018
    strYear = str(year)[2:4]

    #now = None
    day = None
    month = None
    date_today = None
    monthCode = ""
    cellRange = ""

    # call checkUserInputDate() here
    # check if user gave date or not
    [day, month, date_today] = checkUserInputDate(date, year)

    # call fileNameLookup() here
    filename = fileNameLookup(month, strYear)
    
    # get cell position
    cellNumber = getCellNumber(day)
    
    # get prayer times
    prayerTimes = getPrayerTimes(filename, cellNumber)
    
    # create prayer message
    message = composeMessage(prayerTimes, date_today)
    
    return message