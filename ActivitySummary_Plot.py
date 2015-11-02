# -*- coding: utf-8 -*-
"""
WORK IN PROGRESS!

Creates plots from Microsoft Band ACTIVITY SUMMARY data:

"""
import json
from pprint import pprint
import fileinput
import re
import matplotlib.pyplot as plt
import seaborn as sea
import datetime as dt
import matplotlib.dates as dates
import argparse

parser = argparse.ArgumentParser()
#parser.add_argument("filename", help="filename which contains Microsoft Band Health data in JSON format")
parser.add_argument("-a", "--activity", type=str, help="activity type (run, bike, guidedworkout, freeworkout, golf, sleep)")
args = parser.parse_args()

#bandDataFile = args.filename
bandDataFile = "GetActivitySummary.txt"

# For the few oddball cases where there are missing key/pairs
class chkDict(dict):
    def __missing__(self, key):
        return 0
        
# Remove the "nextPage"s so JSON reading doesn't break; save backup file of original
for line in fileinput.input(bandDataFile, inplace=1, backup='.bak'):
    line = re.sub(r'\],\"nextPage\":\"https:.+?(?=\")\",\"itemCount\":[0-9]*\}\{\"[a-zA-Z]*\":\[',r',', line.rstrip())
    print(line)
   
# Load our data!
with open(bandDataFile) as data_file:
    data=json.load(data_file, object_pairs_hook=chkDict)

# Arrays for data that you tend to plot
activityDate = []
caloriesBurned = []
avgHeartRate = []
lowHeartRate = []
peakHeartRate = []
zoneHeartRate = []
totalDistance = []
actDuration = []

# Pulling out relevant data from the JSON array 
if args.activity == "bike":  
    for i in range(0, len(data['bikeActivities'])):
        activityDate.append(re.sub('T.*','',data['bikeActivities'][i]['startTime']))
        caloriesBurned.append(data['bikeActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        totalDistance.append(data['bikeActivities'][i]['distanceSummary']['totalDistance'])
        actDuration.append(data['bikeActivities'][i]['duration'])
        avgHeartRate.append(data['bikeActivities'][i]['heartRateSummary']['averageHeartRate'])
        lowHeartRate.append(data['bikeActivities'][i]['heartRateSummary']['lowestHeartRate'])
        peakHeartRate.append(data['bikeActivities'][i]['heartRateSummary']['peakHeartRate'])
        zoneHeartRate.append(data['bikeActivities'][i]['performanceSummary']['heartRateZones'])

    x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDate]
    
    #if args.start:
    #    startTime = args.start
    #    lastIndex = dateRange.index(startTime)
    #else:
    lastIndex = len(activityDate)  
        
    #if args.end:
    #    endTime = args.end
    #    firstIndex = dateRange.index(endTime)
    #else:
    firstIndex = 0
        
    fig = plt.figure()
    sea.set_style('darkgrid')
    ax1 = fig.add_subplot(311)
    ax1.plot_date(x[firstIndex:lastIndex],caloriesBurned[firstIndex:lastIndex],'r.')    # solid red line
    sea.axlabel('','Calories Burned')
    
    ax2 = fig.add_subplot(312)                        # 3 rows, 1 column, plot #2
    ax2.plot_date(x[firstIndex:lastIndex],totalDistance[firstIndex:lastIndex],'b.')        # solid blue line
    sea.axlabel('','Total Distance')
    
    ax3 = fig.add_subplot(313)                        # 3 rows, 1 column, plot #3
    ax3.plot_date(x[firstIndex:lastIndex],avgHeartRate[firstIndex:lastIndex],'g.')      # solid green line
    ax3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y %H:%M'))
    fig.autofmt_xdate()               # angle the dates for easier reading
    sea.axlabel('Date','Heart Rate')
    fig.suptitle('MS Band Bike Summary',fontsize=16)

elif args.activity == "guidedworkout":
    workoutID = []
    for j in range(0, len(data['guidedWorkoutActivities'])):
        activityDate.append(re.sub('T.*','',data['guidedWorkoutActivities'][j]['startTime']))
        caloriesBurned.append(data['guidedWorkoutActivities'][j]['caloriesBurnedSummary']['totalCalories'])
        actDuration.append(data['guidedWorkoutActivities'][j]['duration'])
        avgHeartRate.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['averageHeartRate'])
        lowHeartRate.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['lowestHeartRate'])
        peakHeartRate.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['peakHeartRate'])
        zoneHeartRate.append(data['guidedWorkoutActivities'][j]['performanceSummary']['heartRateZones'])
        workoutID.append(data['guidedWorkoutActivities'][j]['workoutPlanId'])

    x = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDate]
    
    #if args.start:
    #    startTime = args.start
    #    lastIndex = dateRange.index(startTime)
    #else:
    lastIndex = len(activityDate)  
        
    #if args.end:
    #    endTime = args.end
    #    firstIndex = dateRange.index(endTime)
    #else:
    firstIndex = 0
        
    fig = plt.figure()
    sea.set_style('darkgrid')
    ax1 = fig.add_subplot(311)
    ax1.plot_date(x[firstIndex:lastIndex],caloriesBurned[firstIndex:lastIndex],'r.')    # solid red line
    sea.axlabel('','Calories Burned')
    
    ax2 = fig.add_subplot(312)                        # 3 rows, 1 column, plot #2
    ax2.plot_date(x[firstIndex:lastIndex],actDuration[firstIndex:lastIndex],'b.')        # solid blue line
    sea.axlabel('','Workout Duration')
    
    ax3 = fig.add_subplot(313)                        # 3 rows, 1 column, plot #3
    ax3.plot_date(x[firstIndex:lastIndex],avgHeartRate[firstIndex:lastIndex],'g.')      # solid green line
    ax3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y %H:%M'))
    fig.autofmt_xdate()               # angle the dates for easier reading
    sea.axlabel('Date','Heart Rate')
    fig.suptitle('MS Band Guided Workout Summary',fontsize=16)


'''
if args.activity == "run":
    runningPace = []
    for k in range(0, len(data['runActivities'])):
        activityDate.append(re.sub('T.*','',data['runActivities'][i]['startTime']))
        caloriesBurned.append(data['runActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        totalDistance.append(data['runActivities'][i]['distanceSummary']['totalDistance'])
        actDuration.append(data['runActivities'][i]['duration'])
        avgHeartRate.append(data['runActivities'][i]['heartRateSummary']['averageHeartRate'])
        lowHeartRate.append(data['runActivities'][i]['heartRateSummary']['lowestHeartRate'])
        peakHeartRate.append(data['runActivities'][i]['heartRateSummary']['peakHeartRate'])
        zoneHeartRate.append(data['runActivities'][i]['performanceSummary']['heartRateZones'])
        runningPace.append(data['runActivities'][i]['distanceSummary']['pace'])

if args.activity == "freeworkout":
    for n in range(0, len(data['freePlayActivities'])):
        activityDate.append(re.sub('T.*','',data['freePlayActivities'][i]['startTime']))
        caloriesBurned.append(data['freePlayActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        actDuration.append(data['freePlayActivities'][i]['duration'])
        avgHeartRate.append(data['freePlayActivities'][i]['heartRateSummary']['averageHeartRate'])
        lowHeartRate.append(data['freePlayActivities'][i]['heartRateSummary']['lowestHeartRate'])
        peakHeartRate.append(data['freePlayActivities'][i]['heartRateSummary']['peakHeartRate'])
        zoneHeartRate.append(data['freePlayActivities'][i]['performanceSummary']['heartRateZones'])

if args.activity == "golf":
    golfParOrBetter = []
    for p in range(0, len(data['golfActivities'])):
        activityDate.append(re.sub('T.*','',data['golfActivities'][i]['startTime']))
        caloriesBurned.append(data['golfActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        actDuration.append(data['golfActivities'][i]['duration'])
        totalDistance.append(data['golfActivities'][i]['totalDistanceWalked'])
        golfParOrBetter.append(data['golfActivities'][i]['parOrBetterCount'])

if args.activity == "sleep":
    sleepNumWakeup = []
    fallAsleepTime = []
    wakeupTime = []
    sleepEfficiency = []
    restfulSleep = []
    restlessSleep = []
    awakeDuration = []
    sleepDuration = []
    fallAsleepDuration = []
    for m in range(0, len(data['sleepActivities'])):
        activityDate.append(re.sub('T.*','',data['sleepActivities'][i]['startTime']))
        caloriesBurned.append(data['sleepActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        sleepDuration.append(data['sleepActivities'][i]['sleepDuration'])
        actDuration.append(data['sleepActivities'][i]['duration'])
        avgHeartRate.append(data['sleepActivities'][i]['heartRateSummary']['averageHeartRate'])
        lowHeartRate.append(data['sleepActivities'][i]['heartRateSummary']['lowestHeartRate'])
        peakHeartRate.append(data['sleepActivities'][i]['heartRateSummary']['peakHeartRate'])
        sleepNumWakeup.append(data['sleepActivities'][i]['numberOfWakeups'])
        fallAsleepTime.append(data['sleepActivities'][i]['fallAsleepTime'])
        wakeupTime.append(data['sleepActivities'][i]['wakeupTime'])
        sleepEfficiency.append(data['sleepActivities'][i]['sleepEfficiencyPercentage'])
        restfulSleep.append(data['sleepActivities'][i]['totalRestfulSLeepDuration'])
        restlessSleep.append(data['sleepActivities'][i]['totalRestlessSleepDuration'])
        awakeDuration.append(data['sleepActivities'][i]['awakeDuration'])
        fallAsleepDuration.append(data['sleepActivities'][i]['fallAsleepDuration'])
'''