import sys

def parserProgram(name): # Function to read log file line by line
  with open(name,'r') as file:
    logfile = file.read()
    file.close()
    
    logfile = logfile.lower().splitlines()
    if(logfile[0].lower() == "time log:"):
      return getTimeValue(logfile)
      
# Getting both initial and ending time from each line and compute total hours
def getTimeValue(logfile): 
    hours = 0
    minutes = 0
    # Creating for loop for searching Line By Line
    for l in logfile:
    # Finding AM and PM in log file
        if 'am' in l or 'pm' in l:
            f = 0
            for i in range(len(l)):
                if f > 2:
                    break
                # Spliting with using colon and get the start time
                if f == 0 and (l[i:i + 2] == 'am' or l[i:i + 2] == 'pm'):
                    start = l[i - 5:i]
                    f += 1
                # Spliting with using colon and get the end time
                elif f == 1 and (l[i:i + 2] == 'am' or l[i:i + 2] == 'pm'):
                    end = l[i - 5:i]
                    f += 1
                elif f == 2:
                    minute_start = abs(int(start[-2:]))
                    minute_end = abs(int(end[-2:]))
                    hour_start = abs(int(start[:2].strip()))
                    hour_end = abs(int(end[:2].strip()))
                    if (minute_start>60 or minute_end > 60 or hour_start>12 or hour_end>12):
                        index = logfile.index(l)+1
                        b = ("There is an error in time format in line {}:\n{}".format(index,l))
                        return b
                    hours, minutes = getTimePeriod(minute_start, minute_end, hour_start, hour_end, hours, minutes)
                    break
        # Using assignment operator for changing minutes to hours
        hours += (minutes // 60)
        # Using Mod to get the left over minutes
        minutes = (minutes % 60)
    # Printing hours and minutes taken to complete the file
    return hours,minutes
    
    
    
# From the time value finding the deference between the initial and final time in each line to find the duration on each line
def getTimePeriod(minute_start, minute_end, hour_start, hour_end, hours, minutes): 
    minute = 0
    hour = 0

    if minute_start > minute_end:
        minute = 60 - (minute_start - minute_end)
        hour = hour - 1
    else:
        minute = minute_end - minute_start

    if hour_start > hour_end:
        hour = hour + (12 - (hour_start - hour_end))
    else:
        hour = hour + hour_end - hour_start

    # Hours = Hours+ Hour(Assignment operator to calculate the hours)
    hours += hour
    # Minutes = Minutes+ Minute (Assignment operator to add the minutes)
    minutes += minute
    f = 0
    return hours,minutes
