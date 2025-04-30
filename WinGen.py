import os
import datetime
import time
import subprocess
import re

###Tasks
#generation of lnk files?

def validate_date_time(date_time):
    split_date_time = date_time.split(' ')
    #using regex to validate the date and time
    try:
        
        if (re.search("[0-9]{2}-[0-9]{2}-[0-9]{4}", split_date_time[0])) and (re.search("([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]",split_date_time[1])):
            #if the date is valid then the program continues
            valid_date_time = True
        else:
            valid_date_time = False
        return(valid_date_time)
    except:
        return (False)
        
    
def prefetch_menu():
    print('''
===================================================
                Prefetch Generator
===================================================
Generate a prefetch file for a desired executable
being run at a specified date and time

''')
    #taking input of the date and time the application should have been run
    valid_date_time = False
    while valid_date_time == False:
        #taking input of the date and time
        date_time = input('Date and time of execution (dd-mm-yyyy hh:mm:ss): ')
        if validate_date_time(date_time) == True:
            valid_date_time = True
        else:
            #if date is invalid it asks the user for it again
            print('Please input date and time in the format dd-mm-yyyy hh:mm:ss')

    #take input of the file path of the application to be run
    valid_path = False
    while valid_path != True:
        try:
            path = str(input('File path of executable (use /) :'))
            test = open(path,'rb') #opening the path in read bites mode to check it exists
        except:
            #if path is invalid prompt the user to correct it
            print('Ensure the path is formatted correctly and exists')
        else:
            #if it's valid then continue the program
            valid_path = True

    #Now we need to determine whether a prefetch file already exists for the executable
    file_path_as_list = path.split('/') #split the file path into a list
    exe_name = file_path_as_list[-1] #so that we can seperate the executable name from it

    prefetch_path = 'C:/Windows/Prefetch'#where prefetch files are stored in all windows machines

    #Check if there is already a prefetch file for that exe, if there is delete it
    for file in os.listdir(prefetch_path): #iterate through each file in the prefetch folder
        if exe_name.upper() in file: #checks if that prefetch file relates to the specified exe
            os.remove(prefetch_path+'/'+file)#delete the prefetch file

    
    current_datetime = datetime.datetime.now()#obtaing current date and time

    current_date = current_datetime.strftime('%d-%m-%y')#formatting the date correctly 

    current_time = time.strftime('%H:%M:%S',time.localtime())#formatting the time correctly

    
    generate_prefetch(date_time, path)#run the prefetch generator

    os.system(f'date {current_date}')#resetting date
    os.system(f'time {current_time}')#resetting time

def main_menu():
   
    #ensuring that only valid inputs are possible
    end = False
    while end != True:
        #printing simple text based menu
        print('''
===================================================
                      WINGEN
===================================================
1)Prefetch generator
3) Deleted Files
5) Close
''')
   
        choice = str(input('Please choose an option: '))
        if choice == '1':
            prefetch_menu()
            
        elif choice == '3':
            deleted_files()
        elif choice == '5':
            end = True
        else:
            print('Please select a valid option')
            
                     
def generate_prefetch(last_run_time,path):
    run_date, run_time = last_run_time.split()

    #obtaining current time and date so it can be switched back
    current_datetime = datetime.datetime.now()

    current_date = current_datetime.strftime('%d-%m-%y')

    current_time = time.strftime('%H:%M:%S',time.localtime())
    
    #setting desired date
    os.system(f'date {run_date}')
    #setting desired time
    os.system(f'time {run_time}')

    #opening and closing the desired application
    proc = subprocess.Popen([path])
    #ensuring it stays open long enough for a prefetch file to be generated
    time.sleep(0.1)
    proc.terminate()
   


def deleted_files():
    print('''
===================================================
                    Deleted Files
===================================================
Generate deleted text files to simulate subjects
attempting to hide evidence''')

    #taking input of the date and time the file was created
    valid_date_time = False
    while valid_date_time == False:
    #taking input of the date and time
        date_time = input('Date and time of execution (dd-mm-yyyy hh:mm:ss): ')
        if validate_date_time(date_time) == True:
            valid_date_time = True
        else:
        #if date is invalid it asks the user for it again
            print('Please input date and time in the format dd-mm-yyyy hh:mm:ss')
    #splitting into seperate date and time
    creation_date, creation_time = date_time.split(' ')


    #obtaining current time and date so it can be switched back
    current_datetime = datetime.datetime.now()

    formatted_date = current_datetime.strftime('%d-%m-%y')

    current_time = time.strftime('%H:%M:%S',time.localtime())


    #taking input of the filename
    file_name = str(input('Name of file :'))


    #taking input og the contents of the file
    contents = str(input('Contents of file :'))


    #setting the date and time
    os.system(f'date {creation_date}')
    os.system(f'time {creation_time}')
    #taking input of the filepath for the file to be created at and checking it is valid
    valid_path = False
    while valid_path != True:
        #combning the file name onto the end of the given path
        path = str(input('File path (using /) :')+'/'+file_name+'.txt')
        #attempting to open the file path
        try:
            file = open(path, 'w')
        except:
            #if it doesn't exist, prompt the user to reenter it
            print('''Check that the file path exists and has been input correctly
ensuring the use of /
e.g. C:/Users/Generic-User/Desktop''')
        #if it does exist the file is created 
        else:
            #write contents to file
            file.write(contents)
            file.close()
            valid_path = True

            #set time back
            os.system(f'date {formatted_date}')
            os.system(f'time {current_time}')

    #check if a different last modified time is required
    valid = False
    while valid != True:
        modified = str(input('Would you like a different last modified time? [Y/N] :'))
        if modified.lower() == 'y':
            #if yes, modify file at desired time

            #taking input of the date and time the file was created
            valid_date_time = False
            while valid_date_time == False:
            #taking input of the date and time
                date_time = input('Date and time of execution (dd-mm-yyyy hh:mm:ss): ')
                if validate_date_time(date_time) == True:
                    valid_date_time = True
                else:
                    #if date is invalid it asks the user for it again
                    print('Please input date and time in the format dd-mm-yyyy hh:mm:ss')
            modified_date, modified_time = date_time.split(' ')

            #taking input of modifications
            new_content = str(input('New content to add :'))

            #set date and time
            os.system(f'date {modified_date}')
            os.system(f'time {modified_time}')

            #open file and write new content to it
            file = open(path, 'a')
            file.write(new_content)
            file.close()

            #reset time
            os.system(f'date {formatted_date}')
            os.system(f'time {current_time}')


        elif modified.lower() == 'n':
            #if not continue to deletion of the file
            os.remove(path)
            valid = True


        else:
            print('Please input a valid option [Y/N]')
                    
    


#generate_prefetch("15-03-2022 14:26:50",formatted_date,current_time,"C:/Program Files/EnCase22/EnCase.exe")  
main_menu()
