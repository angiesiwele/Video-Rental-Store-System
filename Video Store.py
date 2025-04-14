'''
Author: Angel Siwele
Created: 28/107/2023 
PROLOGUE
This programme that is designed to manage a video store's rental system. This system has a server and client side applications. 
This is the client side application that enables the user (employee) to insert, update and request data from the MySQL video_store.sql database.
'''

import mysql.connector
conn = mysql.connector.connect(user="root", password="root", host="localhost", database="video_store")
cur = conn.cursor()

''' USE IF YOU WANT TO CREATE DATABASE FROM INSIDE PYTHON SCRIPT
#create database if not exit
database_query = "CREATE DATABASE IF NOT EXISTS  video_store;"
cur.execute(database_query)
conn.commit()
#create tables if not exit
customer_table_query = "\
CREATE TABLE IF NOT EXISTS customers(\
custId INT PRIMARY KEY AUTO_INCREMENT,\
fName VARCHAR(40)  NOT NULL,\
sName VARCHAR(40)  NOT NULL,\
address VARCHAR(40)  NOT NULL,\
phone VARCHAR(10) NOT NULL UNIQUE  \
);"
cur.execute(customer_table_query)
conn.commit()


#create tables if not exit
video_table_query = "\
CREATE TABLE IF NOT EXISTS videos(\
VideoId INT PRIMARY KEY AUTO_INCREMENT,\
videoVer INT NOT NULL ,\
vName VARCHAR(15) NOT NULL,\
videoType VARCHAR(1) NOT NULL ,\
dateAdded VARCHAR NOT NULL \
);"
cur.execute(video_table_query)
conn.commit()


#create tables if not exit
hire_table_query = "\
CREATE TABLE IF NOT EXISTS hire(\
custId INT NOT NULL,\
videoId INT NOT NULL,\
dateHired VARCHAR(20) NOT NULL,\
dateReturn VARCHAR(20),\
FOREIGN KEY (videoId) REFERENCES videos(videoId),\
FOREIGN KEY (custId) REFERENCES customers(custId))\
;"
cur.execute(hire_table_query)
conn.commit()
'''
menu = "=========================================================" + "\n"
menu = menu + "|                 VIDEO STORE                           |" + "\n"
menu = menu + "=========================================================" + "\n"
menu = menu + "| 1. Register Customer                                   |" + "\n"
menu = menu + "| 2. Register Video                                      |" + "\n"
menu = menu + "=========================================================" + "\n"
menu = menu + "| 3. Hire Out Video                                      |" + "\n"
menu = menu + "| 4. Return Video                                        |" + "\n"
menu = menu + "=========================================================" + "\n"
menu = menu + "| X. Exit                                                |" + "\n"
menu = menu + "=========================================================" + "\n"
menu = menu + "Choice:_"


def main():

    possible_answers = ["1","2","3","4","x","X"]
    answer = input(menu)
    while answer not in possible_answers:
        print("Please enter valid option")
        main()        
    else:
        #Exit  
        if answer == "x" or answer == "X":
            exit()
        #Register Customer if not insystem    
        elif int(answer) == 1:
            phone_number = input("Enter Customer's 10 digit Phone Number: ")
            #check if the phone number entered is ten disgit, if not ask for valid phone number
            while len(phone_number) != 10 or phone_number.isdecimal() == False:
                phone_number = input("Enter Customer's 10 digit Phone Number: ")
            else:
                while search_phone(phone_number) == True:                        
                    print("Customer already in database")  
                    main()
                else:
                    name = input("Customer Name: ")
                    surname = input("Customer Surname: ")
                    home_address = input("Customer Home Address: ")
                    # insert details into customers table
                    query = f'INSERT INTO customers (fName,sName,address,phone) VALUES ("{name}" , "{surname}" , "{home_address}" , "{phone_number}")'
                    #print(query)
                    cur.execute(query)
                    conn.commit()
                    print("Customer Successfully Registered")
                    main()
                                       
        #2 Register Video        
        elif int(answer) == 2:
            video_name = input("Please Enter video name:  ")
            #if Video already exists,if so set new video Id to existing videoId            
            video_type = input("Please Enter video type (R for New video or B for old videos): ")
            while video_type != "R" and video_type != "r" and video_type != "B" and video_type != "b":
                video_type = input("Please Enter Valid Video Type (R for New video or B for old videos): ")
            if search_video(video_name) == True:
                video_id = str(get_video_id(video_name))
                query = f'INSERT INTO videos (videoId,vName,videoType,dateAdded) VALUES ({video_id},"{video_name}","{video_type}",(SELECT CURDATE()))'
                cur.execute(query)
                conn.commit()
                print("Video Successfully Registered")
                main()
            else:                
                query =f'INSERT INTO videos (vName,videoType,dateAdded) VALUES ("{video_name}","{video_type}",(SELECT CURDATE()))'
                cur.execute(query)
                conn.commit()
                print("Video Successfully Registered")
                main()
           
           
        #3 Hire Out Video
        elif int(answer) == 3: 
            phone_number = input("Enter Customer's 10 digit Phone Number: ")
            #check if the phone number entered is ten disgit, if not ask for valid phone number
            while len(phone_number) != 10 or phone_number.isdecimal() == False:
                phone_number = input("Enter Customer's 10 digit Phone Number: ")
            else:
                #check if customer registered 
                #if customer is not registered, take user back to main menu to register customer
                if search_phone(phone_number) == False:              
                    print("Customer not Registered")  
                    main()
                #if customer is registered check if video exists 
                elif search_phone(phone_number) == True:
                    #checking if video exists
                    video_id = input("Enter Video ID ")
                    if video_exists(video_id) == True:
                        query = f'INSERT INTO hire (custId,videoId,dateHired) VALUES ((SELECT custId FROM customers WHERE phone = "{phone_number}"),{int(video_id)},(SELECT CURDATE()))'
                        cur.execute(query)
                        conn.commit()
                        print("Video Hire Successfully Recorded")
                        main()
                    else: 
                        print("Video does not exist in system")
                        main()

        #4 Return Video
        elif int(answer) == 4: 
            video_id = input("Please enter video id of video being returned: ")
            phone_number = input("Enter Customer's 10 digit Phone Number: ")
            #check if the phone number entered is ten disgit, if not ask for valid phone number
            while len(phone_number) != 10 or phone_number.isdecimal() == False:
                phone_number = input("Enter Customer's 10 digit Phone Number: ")

            get_cust_id_query = f'SELECT * FROM customers WHERE phone = "{phone_number}"'             
            cur.execute(get_cust_id_query)
            #print("check 1")
            #print("check 2")
            customer_id = cur.fetchall()[0][0]
            #check record of video being hired
            if get_hire_record(customer_id,int(video_id)) == True:
                query = f'UPDATE hire SET dateReturn = (SELECT CURDATE()) WHERE videoId = {video_id} AND custId = (SELECT custId FROM customers WHERE phone = "{phone_number}")'
                cur.execute(query)
                conn.commit()
                print("Video Return Successfully Recorded")
                main()
            else:
                print("There is no record of this video being hired by this customer")
                main()

# return true if customer is in database
def search_phone(number):        
        query = f'SELECT * FROM customers WHERE phone = {number}'
        cur.execute(query)
        result = cur.fetchall()
        return len(result)>0
# returns true if video already exists in database 
def search_video(video_name):
    query = f'SELECT * FROM videos WHERE vName = "{video_name}"'
    cur.execute(query)
    result = cur.fetchall()
    return len(result)>0

# return video id of video in database
def get_video_id(video_name):
    query = f'SELECT * FROM videos WHERE vName = "{video_name}"'
    cur.execute(query)
    result = cur.fetchall() # return is a list of tuples eg [(1),(2),(4),(8)]
    #print(result)
    return result[0][0] # OR (result[0])[0] OR result[0]  

#return true if record of video hire exists (in hire table)
def get_hire_record(customer_id,video_id):
    query = f'SELECT * FROM hire WHERE videoId = {video_id} AND custId = {customer_id}'
    cur.execute(query)
    result = cur.fetchall()
    return len(result)>0

#return true if video exists in system
def video_exists(video_id): 
    query = f'SELECT * FROM videos WHERE videoId = {video_id}'
    cur.execute(query)
    result = cur.fetchall()
    return len(result)>0

main()
conn.close()



