# A project for discord weekly comps.
#! Warning! this isn't 100% automatic or reliable. sometimes you need to clean up the data a bit but then it should be fine
#! If the results have a time of 46:39.99 that means that there are < 3 results
import csv

#converts a csv file into a nested list
#!        \/ \/ \/ \/ <---- put file path here     
with open('stream all I wanted by paramore (Responses) - form responses 1.csv', newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    data = list(reader)

#!change corresponding to the number of collums that aren't designated for an event except names (so stuff like rate this comp, anything to add etc.)
non_event_collumns = 1

#Converts from milliseconds to the format xx:yy.zz where both minutes and ms are optional
def ms_to_time(time):
    minutes = int((time / (1000*60)) % 60)
    seconds = int(time / 1000) % 60
    milliseconds = int((time % 1000) / 10)

    if minutes == 0 and milliseconds == 0:
        return("{0}".format(seconds))
    
    elif minutes == 0:
        if milliseconds < 10:
            return("{0}.0{1}".format(seconds, milliseconds))
        return("{0}.{1}".format(seconds, milliseconds))
    
    elif milliseconds == 0:
        if seconds < 10:
            return("{0}:0{1}".format(minutes, seconds))
        return("{0}:{1}".format(minutes, seconds))
    
    else:
        if seconds < 10 and milliseconds < 10:
            return("{0}:0{1}.0{2}".format(minutes, seconds, milliseconds))
        elif seconds < 10:
            return("{0}:0{1}.{2}".format(minutes, seconds, milliseconds))
        elif milliseconds:
            return("{0}:{1}.0{2}".format(minutes, seconds, milliseconds))
        return("{0}:{1}.{2}".format(minutes, seconds, milliseconds))

#TODO make this less ugly. Beware that both minutes and ms are optional so have fun
#* time format: min:sec.ms [xx:yy.z(z)]
def time_to_ms(time):
    
    #if someone didn't compete the entry would be empty so we change it to not mess up sorting
    if time == '':
        return 99999999999
    
    #bunch of try excepts becouse both minutes and milliseconds are optionals and it would throw errors
    try:
        x, milliseconds = time.split('.')
    except:
        milliseconds = 0
        try:
            minutes, seconds = time.split(':')
        except:
            minutes = 0
            seconds = time
    else:
        try:
            minutes, seconds = x.split(':')
        except:
            minutes = 0
            seconds = x
    
    #fixes the problem where 0.1 and 0.01 would register as the same value and converts it to proper ms
    if milliseconds == 0:
        return int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)
    elif len(milliseconds) == 1:
        milliseconds = int(milliseconds)*100
    else:
        milliseconds = int(milliseconds)*10
    
    return int(minutes) * 60000 + int(seconds) * 1000 + int(milliseconds)

def list_formatting(list):
    for i in range(0, len(list)):
        list[i] = ''.join(c for c in list[i] if (c.isdigit() or c == '.' or c ==  ':'))
        list[i] = time_to_ms(list[i])

#pointer of name collumn and pointer for events
names_collumn_index = 1

names = []
for row_index in range(1, len(data)):
    names.append(data[row_index][names_collumn_index])

event_results = []
for col_index in range(names_collumn_index+1, len(data[0]) - non_event_collumns):
    
    #gets the name of current event
    current_event = data[0][col_index]
    
    for row_index in range(1, len(data)):
        event_results.append(data[row_index][col_index])
    
    print(current_event)
    
    list_formatting(event_results)
    sorted_results = sorted(event_results)
    print("1. {0} {1}".format(names[event_results.index(sorted_results[0])], ms_to_time(sorted_results[0])))
    print("2. {0} {1}".format(names[event_results.index(sorted_results[1])], ms_to_time(sorted_results[1])))
    print("3. {0} {1}".format(names[event_results.index(sorted_results[2])], ms_to_time(sorted_results[2])))
    print("\n")

    event_results.clear()