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
import isodate
import itertools as it

parser = argparse.ArgumentParser()
#parser.add_argument("filename", help="filename which contains Microsoft Band Health data in JSON format")
args = parser.parse_args()

#bandDataFile = args.filename
bandDataFile = "GetActBasic.txt"

# For the few oddball cases where there are missing key/pairs
class chkDict(dict):
    def __missing__(self, key):
        return 0
        
newDataFile = "Formatted_" + bandDataFile
f = open(bandDataFile)
contents = f.read()
f.close()
contents = contents.replace('\n','')
#contents = re.sub(r'\],\"nextPage\":\"https:.+?(?=\")\",\"itemCount\":[0-9]*\}[\r\n]*\{\"[a-zA-Z]*\":\[',r',',contents.rstrip())
contents = re.sub(r',\"nextPage\":\"https:.+?(?=\")\",\"itemCount\":[0-9]*\}\{',r',',contents.rstrip())
pprint("subbed nextpage")
countFixRun = it.count()
countFixBike =  it.count()
countFixSleep = it.count()
countFixGolf = it.count()
countFixGWo = it.count()
countFixFWo = it.count()
#print re.sub(r"</?\w+>", lambda x: '{{{}}}'.format(next(cnt)), text)
contents = re.sub(r'bikeActivities', lambda x: 'bikeActivities{{{}}}'.format(next(countFixBike)),contents)
contents = re.sub(r'runActivities', lambda x: 'runActivities{{{}}}'.format(next(countFixRun)),contents)
contents = re.sub(r'sleepActivities', lambda x: 'sleepActivities{{{}}}'.format(next(countFixSleep)),contents)
contents = re.sub(r'golfActivities', lambda x: 'golfActivities{{{}}}'.format(next(countFixGolf)),contents)
contents = re.sub(r'guidedWorkoutActivities', lambda x: 'guidedWorkoutActivities{{{}}}'.format(next(countFixGWo)),contents)
contents = re.sub(r'freePlayActivities', lambda x: 'freePlayActivities{{{}}}'.format(next(countFixFWo)),contents)
pprint("added counts")

f = open(newDataFile, 'w')
f.write(contents)
f.close()
pprint("closed file")
       
# Remove the "nextPage"s so JSON reading doesn't break; save backup file of original
#for line in fileinput.input(bandDataFile, inplace=1, backup='.bak'):
#    line = re.sub(r'\],\"nextPage\":\"https:.+?(?=\")\",\"itemCount\":[0-9]*\}\{\"[a-z]*\":\[',r',', line.rstrip())
#    print(line)
   
# Load our data!
with open(newDataFile) as data_file:
    data=json.load(data_file, object_pairs_hook=chkDict)

# Arrays for data that you tend to plot
activityDateB = []
caloriesBurnedB = []
avgHeartRateB = []
lowHeartRateB = []
peakHeartRateB = []
zoneHeartRateB = []
totalDistanceB = []
actDurationB = []

# Pulling out relevant data from the JSON array 
for i in range(0, len(data['bikeActivities'])):
    activityDateB.append(re.sub('T.*','',data['bikeActivities'][i]['startTime']))
    caloriesBurnedB.append(data['bikeActivities'][i]['caloriesBurnedSummary']['totalCalories'])
    totalDistanceB.append(data['bikeActivities'][i]['distanceSummary']['totalDistance'])
    actDurationB.append(data['bikeActivities'][i]['duration'])
    avgHeartRateB.append(data['bikeActivities'][i]['heartRateSummary']['averageHeartRate'])
    lowHeartRateB.append(data['bikeActivities'][i]['heartRateSummary']['lowestHeartRate'])
    peakHeartRateB.append(data['bikeActivities'][i]['heartRateSummary']['peakHeartRate'])
    zoneHeartRateB.append(data['bikeActivities'][i]['performanceSummary']['heartRateZones'])

xB = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDateB]

#if args.start:
#    startTime = args.start
#    lastIndex = dateRange.index(startTime)
#else:
lastIndexB = len(activityDateB)  
    
#if args.end:
#    endTime = args.end
#    firstIndex = dateRange.index(endTime)
#else:
firstIndexB = 0
    
fig = plt.figure()
sea.set_style('darkgrid')
ax1 = fig.add_subplot(311)
ax1.plot_date(xB[firstIndexB:lastIndexB],caloriesBurnedB[firstIndexB:lastIndexB],'r.')    # solid red line
sea.axlabel('','Calories Burned')

ax2 = fig.add_subplot(312)                        # 3 rows, 1 column, plot #2
ax2.plot_date(xB[firstIndexB:lastIndexB],totalDistanceB[firstIndexB:lastIndexB],'b.')        # solid blue line
sea.axlabel('','Total Distance')

ax3 = fig.add_subplot(313)                        # 3 rows, 1 column, plot #3
ax3.plot_date(xB[firstIndexB:lastIndexB],avgHeartRateB[firstIndexB:lastIndexB],'g.')      # solid green line
ax3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
fig.autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
fig.suptitle('MS Band Bike Summary',fontsize=16)

activityDateWG = []
caloriesBurnedWG = []
avgHeartRateWG = []
lowHeartRateWG = []
peakHeartRateWG = []
zoneHeartRateWG = []
actDurationWG = []
workoutIDWG = []


for j in range(0, len(data['guidedWorkoutActivities'])):
    activityDateWG.append(re.sub('T.*','',data['guidedWorkoutActivities'][j]['startTime']))
    caloriesBurnedWG.append(data['guidedWorkoutActivities'][j]['caloriesBurnedSummary']['totalCalories'])
    actDurationWG.append((isodate.parse_duration(data['guidedWorkoutActivities'][j]['duration'])).total_seconds())
    avgHeartRateWG.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['averageHeartRate'])
    lowHeartRateWG.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['lowestHeartRate'])
    peakHeartRateWG.append(data['guidedWorkoutActivities'][j]['heartRateSummary']['peakHeartRate'])
    zoneHeartRateWG.append(data['guidedWorkoutActivities'][j]['performanceSummary']['heartRateZones'])
    workoutIDWG.append(data['guidedWorkoutActivities'][j]['workoutPlanId'])

xWG = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDateWG]

#    startTime = args.start
#    lastIndex = dateRange.index(startTime)
#else:
lastIndexWG = len(activityDateWG)  
    
#if args.end:
#    endTime = args.end
#    firstIndex = dateRange.index(endTime)
#else:
firstIndexWG = 0
    
fig2 = plt.figure()
sea.set_style('darkgrid')
ax_wo1 = fig2.add_subplot(311)
ax_wo1.plot_date(xWG[firstIndexWG:lastIndexWG],caloriesBurnedWG[firstIndexWG:lastIndexWG],'r.')    # solid red line
sea.axlabel('','Calories Burned')

ax_wo2 = fig2.add_subplot(312)                        # 3 rows, 1 column, plot #2
ax_wo2.plot_date(xWG[firstIndexWG:lastIndexWG],actDurationWG[firstIndexWG:lastIndexWG],'b.')        # solid blue line
sea.axlabel('','Workout Duration')

ax_wo3 = fig2.add_subplot(313)                        # 3 rows, 1 column, plot #3
ax_wo3.plot_date(xWG[firstIndexWG:lastIndexWG],avgHeartRateWG[firstIndexWG:lastIndexWG],'g.')      # solid green line
ax_wo3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
fig2.autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
fig2.suptitle('MS Band Guided Workout Summary',fontsize=16)


activityDateR = []
caloriesBurnedR = []
avgHeartRateR = []
lowHeartRateR = []
peakHeartRateR = []
zoneHeartRateR = []
totalDistanceR = []
actDurationR = []
runningPaceR = []

for k in range(0, len(data['runActivities'])):
    activityDateR.append(re.sub('T.*','',data['runActivities'][k]['startTime']))
    caloriesBurnedR.append(data['runActivities'][k]['caloriesBurnedSummary']['totalCalories'])
    totalDistanceR.append(data['runActivities'][k]['distanceSummary']['totalDistance'])
    actDurationR.append((isodate.parse_duration(data['runActivities'][k]['duration'])).total_seconds())
    avgHeartRateR.append(data['runActivities'][k]['heartRateSummary']['averageHeartRate'])
    lowHeartRateR.append(data['runActivities'][k]['heartRateSummary']['lowestHeartRate'])
    peakHeartRateR.append(data['runActivities'][k]['heartRateSummary']['peakHeartRate'])
    zoneHeartRateR.append(data['runActivities'][k]['performanceSummary']['heartRateZones'])
    runningPaceR.append(data['runActivities'][k]['distanceSummary']['pace'])

xR = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDateR]

pprint(k)

lastIndexR = len(activityDateR)  
firstIndexR = 0

fig3 = plt.figure()
sea.set_style('darkgrid')
ax_r1 = fig3.add_subplot(311)
ax_r1.plot_date(xR[firstIndexR:lastIndexR],caloriesBurnedR[firstIndexR:lastIndexR],'r.')    # solid red line
sea.axlabel('','Calories Burned')

ax_r2 = fig3.add_subplot(312)                        # 3 rows, 1 column, plot #2
ax_r2.plot_date(xR[firstIndexR:lastIndexR],actDurationR[firstIndexR:lastIndexR],'b.')        # solid blue line
sea.axlabel('','Workout Duration')

ax_r3 = fig3.add_subplot(313)                        # 3 rows, 1 column, plot #3
ax_r3.plot_date(xR[firstIndexR:lastIndexR],avgHeartRateR[firstIndexR:lastIndexR],'g.')      # solid green line
ax_r3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
fig3.autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
fig3.suptitle('MS Band Run Summary',fontsize=16)

activityDateFW = []
caloriesBurnedFW = []
avgHeartRateFW = []
lowHeartRateFW = []
peakHeartRateFW = []
zoneHeartRateFW = []
actDurationFW = []

for n in range(0, len(data['freePlayActivities'])):
    activityDateFW.append(re.sub('T.*','',data['freePlayActivities'][n]['startTime']))
    caloriesBurnedFW.append(data['freePlayActivities'][n]['caloriesBurnedSummary']['totalCalories'])
    actDurationFW.append((isodate.parse_duration(data['freePlayActivities'][n]['duration'])).total_seconds())
    avgHeartRateFW.append(data['freePlayActivities'][n]['heartRateSummary']['averageHeartRate'])
    lowHeartRateFW.append(data['freePlayActivities'][n]['heartRateSummary']['lowestHeartRate'])
    peakHeartRateFW.append(data['freePlayActivities'][n]['heartRateSummary']['peakHeartRate'])
    zoneHeartRateFW.append(data['freePlayActivities'][n]['performanceSummary']['heartRateZones'])

xFW = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDateFW]

lastIndexFW = len(activityDateFW)  
firstIndexFW = 0

fig4 = plt.figure()
sea.set_style('darkgrid')
ax_fw1 = fig4.add_subplot(311)
ax_fw1.plot_date(xFW[firstIndexFW:lastIndexFW],caloriesBurnedFW[firstIndexFW:lastIndexFW],'r.')    # solid red line
sea.axlabel('','Calories Burned')

ax_fw2 = fig4.add_subplot(312)                        # 3 rows, 1 column, plot #2
ax_fw2.plot_date(xFW[firstIndexFW:lastIndexFW],actDurationFW[firstIndexFW:lastIndexFW],'b.')        # solid blue line
sea.axlabel('','Workout Duration')

ax_fw3 = fig4.add_subplot(313)                        # 3 rows, 1 column, plot #3
ax_fw3.plot_date(xFW[firstIndexFW:lastIndexFW],avgHeartRateFW[firstIndexFW:lastIndexFW],'g.')      # solid green line
ax_fw3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
fig4.autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
fig4.suptitle('MS Band Free Workout Summary',fontsize=16)    
    

'''
if args.activity == "golf":
    golfParOrBetter = []
    for p in range(0, len(data['golfActivities'])):
        activityDate.append(re.sub('T.*','',data['golfActivities'][i]['startTime']))
        caloriesBurned.append(data['golfActivities'][i]['caloriesBurnedSummary']['totalCalories'])
        actDuration.append(data['golfActivities'][i]['duration'])
        totalDistance.append(data['golfActivities'][i]['totalDistanceWalked'])
        golfParOrBetter.append(data['golfActivities'][i]['parOrBetterCount'])
'''

activityDateS = []
caloriesBurnedS = []
actDurationS = []
avgHeartRateS = []
lowHeartRateS = []
peakHeartRateS = []
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
    activityDateS.append(re.sub('T.*','',data['sleepActivities'][m]['startTime']))
    caloriesBurnedS.append(data['sleepActivities'][m]['caloriesBurnedSummary']['totalCalories'])
    sleepDuration.append(data['sleepActivities'][m]['sleepDuration'])
    actDurationS.append((isodate.parse_duration(data['sleepActivities'][m]['duration'])).total_seconds())
    avgHeartRateS.append(data['sleepActivities'][m]['heartRateSummary']['averageHeartRate'])
    lowHeartRateS.append(data['sleepActivities'][m]['heartRateSummary']['lowestHeartRate'])
    peakHeartRateS.append(data['sleepActivities'][m]['heartRateSummary']['peakHeartRate'])
    sleepNumWakeup.append(data['sleepActivities'][m]['numberOfWakeups'])
    fallAsleepTime.append(data['sleepActivities'][m]['fallAsleepTime'])
    wakeupTime.append(data['sleepActivities'][m]['wakeupTime'])
    sleepEfficiency.append(data['sleepActivities'][m]['sleepEfficiencyPercentage'])
    restfulSleep.append(data['sleepActivities'][m]['totalRestfulSLeepDuration'])
    restlessSleep.append(data['sleepActivities'][m]['totalRestlessSleepDuration'])
    awakeDuration.append(data['sleepActivities'][m]['awakeDuration'])
    fallAsleepDuration.append(data['sleepActivities'][m]['fallAsleepDuration'])

xS = [dt.datetime.strptime(d,'%Y-%m-%d').date() for d in activityDateS]

lastIndexS = len(activityDateS)  
firstIndexS = 0

fig5 = plt.figure()
sea.set_style('darkgrid')
ax_s1 = fig5.add_subplot(311)
ax_s1.plot_date(xS[firstIndexS:lastIndexS],caloriesBurnedS[firstIndexS:lastIndexS],'r.')    # solid red line
sea.axlabel('','Calories Burned')

ax_s2 = fig5.add_subplot(312)                        # 3 rows, 1 column, plot #2
ax_s2.plot_date(xS[firstIndexS:lastIndexS],actDurationS[firstIndexS:lastIndexS],'b.')        # solid blue line
sea.axlabel('','Workout Duration')

ax_s3 = fig5.add_subplot(313)                        # 3 rows, 1 column, plot #3
ax_s3.plot_date(xS[firstIndexS:lastIndexS],avgHeartRateS[firstIndexS:lastIndexS],'g.')      # solid green line
ax_s3.xaxis.set_major_formatter(dates.DateFormatter('%m/%d/%Y'))
fig5.autofmt_xdate()               # angle the dates for easier reading
sea.axlabel('Date','Heart Rate')
fig5.suptitle('MS Band Sleep Summary',fontsize=16)