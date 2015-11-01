# -*- coding: utf-8 -*-
"""
Creates 3 plots from Microsoft Band DAILY SUMMARY data:
1 - Calories Burned
2 - Steps Taken
3 - Heart Rate (Max, Min, Avg)

Required command line option: filename
Optional command line options: --start StartDate --end EndDate

Examples:

Plot the data in DailySummary.txt from April 3rd, 2015 to July 5th, 2015:
DailySummary_Plot.py DailySummary.txt --start 2015-04-03 --end 2015-07-05

Plot all data in DailySummary.txt:
DailySummary_Plot.py DailySummary.txt

"""

import json
from pprint import pprint
import fileinput
import re
import matplotlib.pyplot as plt
import seaborn as sea
import datetime as dt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("filename", help="filename which contains Microsoft Band Health data in JSON format")
parser.add_argument("-s", "--start", help="start date in the format YYYY-MM-DD")
parser.add_argument("-e", "--end", help="end date in the format YYYY-MM-DD")
args = parser.parse_args()

bandDataFile = args.filename

# For the few oddball cases where there are missing key/pairs
class chkDict(dict):
    def __missing__(self, key):
        return 0
        
# Remove the "nextPage"s so JSON reading doesn't break; save backup file of original
for line in fileinput.input(bandDataFile, inplace=1, backup='.bak'):
    line = re.sub(r'\],\"nextPage\":\"https:.+?(?=\")\",\"itemCount\":[0-9]*\}\{\"[a-z]*\":\[',r',', line.rstrip())
    print(line)
   
# Load our data!
with open(bandDataFile) as data_file:
    data=json.load(data_file, object_pairs_hook=chkDict)
    
# Arrays for data that you tend to plot
caloriesBurned = []
avgHeartRate = []
lowHeartRate = []
peakHeartRate = []
stepsTaken = []
dateRange = []

# Pulling out relevant data from the JSON array 
for i in range(0, len(data['summaries'])):
    caloriesBurned.append(data['summaries'][i]['caloriesBurnedSummary']['totalCalories'])
    avgHeartRate.append(data['summaries'][i]['heartRateSummary']['averageHeartRate'])
    lowHeartRate.append(data['summaries'][i]['heartRateSummary']['lowestHeartRate'])
    peakHeartRate.append(data['summaries'][i]['heartRateSummary']['peakHeartRate'])
    stepsTaken.append(data['summaries'][i]['stepsTaken'])
    dateRange.append(re.sub('T.*','',data['summaries'][i]['startTime']))

# MS Band timestamp form: 2015-10-31T00:00:00.000-07:00
# Strip everything but the YYYY-MM-DD
x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in dateRange]

if args.start:
    startTime = args.start
    lastIndex = dateRange.index(startTime)
else:
    lastIndex = len(dateRange)  
    
if args.end:
    endTime = args.end
    firstIndex = dateRange.index(endTime)
else:
    firstIndex = 0

sea.set_style('darkgrid')
plt.subplot(311)                        # 3 rows, 1 column, plot @1
plt.plot_date(x[firstIndex:lastIndex],caloriesBurned[firstIndex:lastIndex],'r-')    # solid red line
sea.axlabel('','Calories Burned')
plt.subplot(312)                        # 3 rows, 1 column, plot #2
plt.plot_date(x[firstIndex:lastIndex],stepsTaken[firstIndex:lastIndex],'b-')        # solid blue line
sea.axlabel('','Steps Taken')
plt.subplot(313)                        # 3 rows, 1 column, plot #3
plt.plot_date(x[firstIndex:lastIndex],avgHeartRate[firstIndex:lastIndex],'g-')      # solid green line
plt.gcf().autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
plt.suptitle('MS Band Daily Summary',fontsize=16)
