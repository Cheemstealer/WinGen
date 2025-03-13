import os
import datetime
import time
import subprocess
import re
def prefetch_menu():
    print('''
===================================================
                Prefetch Generator
===================================================
Generate a prefetch file for a desired executable
being run at a specified date and time

''')
    valid_date_time = False
    while valid_date_time == False:
        date_time = input('Date and time of execution (dd-mm-yyyy hh:mm:ss): ')
        #splitting the date and time apart
        split_date_time = date_time.split(' ')
        #using regex to validate the date and time
        if (re.search("[0-9]{2}-[0-9]{2}-[0-9]{4}", split_date_time[0])) and (re.search("([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]",split_date_time[1])):
            print('reg working')
            valid_date_time = True
        else:
            print('Please input date and time in the format dd-mm-yyyy hh:mm:ss')
            

def main_menu():
    #printing simple text based menu
    print('''
===================================================
                      WINGEN
===================================================
1)Prefetch generator
''')
    #ensuring that only valid inputs are possible
    valid = False
    while valid == False:
        choice = str(input('Please choose an option: '))
        if choice == '1':
            prefetch_menu()
            valid = True
        else:
            print('Please select a valid option')
            
                     
def generate_prefetch(last_run_time,current_date,current_time,path):
    run_date, run_time = last_run_time.split()
    
    #setting desired date
    os.system(f'date {run_date}')
    #setting desired time
    os.system(f'time {run_time}')

    #opening and closing the desired application
    proc = subprocess.Popen([path])
    #ensuring it stays open long enough for a prefetch file to be generated
    time.sleep(0.1)
    proc.terminate()
   
    #change time back after making the prefetch file
    os.system(f'date {current_date}')
    os.system(f'time {current_time}')

#obtaining current time and date so it can be switched back
current_datetime = datetime.datetime.now()

formatted_date = current_datetime.strftime('%d-%m-%y')

current_time = time.strftime('%H:%M:%S',time.localtime())


#generate_prefetch("15-03-2022 14:26:50",formatted_date,current_time,"C:/Program Files/EnCase22/EnCase.exe")  
main_menu()

