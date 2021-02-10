#Title: weather_station.py
#This is a program written for the Raspberry Pi and uses the GrovePi hat to allow for sensors to be attached
#This program records the temperature and humidity and stores the information in a JSON file. Then with a click
#of a button the JSON files is converted into a CSV file and then emailed to a particular recipient
#Author: Nicholas Richards
#date: 1/24/2021
#SNHU

import grovepi
from grovepi import *
import json
import csv
import smtplib
from datetime import datetime
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders

#Information for GMAIL server and account
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
GMAIL_USERNAME = 'raspberrypiprojectenhancement@gmail.com'
GMAIL_PASSWORD = 'Rpi4Email' 

outputData = {}
outputData['Weather'] = []

dht_sensor_port = 7

led_red = 4

led_green = 3

led_blue = 2

light_sensor = 0

threshold = 180

button = 6

grovepi.pinMode(button, "INPUT")
grovepi.pinMode(light_sensor, "INPUT")
grovepi.pinMode(led_red, "OUTPUT")
grovepi.pinMode(led_green, "OUTPUT")
grovepi.pinMode(led_blue, "OUTPUT")



while True:
    try:#try catch for IO errors
        
        sensor_value = grovepi.analogRead(light_sensor)
       
        
        
        if sensor_value <= 0: #I added this to keep from dividing from zero and crashing the program.
            
            resistance = 0
            
        else:
            
            resistance = (float)(1023- sensor_value) * 10 / sensor_value
         
        if resistance > threshold: #if resistance is greater than the threshold turn LED off and do not pull temperature reading
            
            grovepi.digitalWrite(led_green, 0)
            grovepi.digitalWrite(led_red, 0)
            grovepi.digitalWrite(led_blue, 0)
        
        else: #pull temperature reading and converts to Farenheit 
            [temp,hum] = dht(dht_sensor_port, 0)
            tempF = temp * 9/5 + 32
            
            
            t = str(tempF)
            h = str(hum)
            
            outputData['Weather'].append({'temperature':t, 'humidity':h})#appends temperature and humdity to outputData
    
            with open('outputData.json', 'w') as outfile: #creates JSON file from outputData 
                json.dump(outputData, outfile)
            
            
            if tempF > 60 and tempF < 85 and hum < 80:#turns green led on when condition is met
                
                
                grovepi.digitalWrite(led_green, 1)
            
            
            elif tempF > 85 and tempF < 90 and hum <80 :#turns on blue led on when condition is met
                
                grovepi.digitalWrite(led_blue, 1)
            
            
            elif tempF > 95: #turns red led on when tempF is higher than 95
                
                grovepi.digitalWrite(led_red, 1)
            
            elif hum > 80: #turns on green and blue led on it hum is higher than 80
                grovepi.digitalWrite(led_green, 1)
                grovepi.digitalWrite(led_blue, 1)
            
        button_state = digitalRead(button) #Reads button press
        if(button_state== 0):#if button not pressed
            print("Button not pressed")
        
        else: #button pressed    
            print("Button pressed")
            with open('outputData.json') as json_file:#loads json file to program
                data = json.load(json_file)
                
            weather_data = data['Weather']
                
            data_file = open('Weather Report.csv', 'w')
                
            csv_writer = csv.writer(data_file)#writes csv file
                
            count = 0
                
            for read in weather_data:#iterates through file
                if count == 0:
                    
                    header = read.keys()#creates csv headers
                    csv_writer.writerow(header)
                    count += 1
                    
                csv_writer.writerow(read.values())#writes values for each row
            data_file.close()
            
           
            #beginning parts of email for subject and filename
            SUBJECT = 'Weather Report'
            FILENAME = 'Weather Report.csv'
            FILEPATH = '/home/pi/Desktop/Python Files/Weather Report.csv'
            sendTo = 'nicholas.richards@snhu.edu'
       
            msg = MIMEMultipart()#creates email header
            msg['From'] = GMAIL_USERNAME
            msg['To'] = COMMASPACE.join([sendTo])
            msg['Subject'] = SUBJECT
            
            now = datetime.now()#gets current_time
            current_time = now.strftime("%H:%M:%S")
            content = 'This is the weather report you requested at {}'.format(current_time) 
            
            #creates attachment for csv file
            part = MIMEBase('application', "octet-stream")
            part.set_payload(open(FILEPATH, "rb").read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', 'attachment', filename=FILENAME) 
            
            #attaches attachment and content to email
            msg.attach(part)
            msg.attach(MIMEText(content))
            
            #connects to Gmail server and sends email
            smtpObj = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login(GMAIL_USERNAME, GMAIL_PASSWORD)
            smtpObj.sendmail(GMAIL_USERNAME, sendTo, msg.as_string())
            smtpObj.quit()
       
        time.sleep(5)#checks temperature every 5 seconds
        
     
    except (IOError, TypeError) as e:#IO exception
        print (str(e))
        grovepi.digitalWrite(led_red, 0)
        grovepi.digitalWrite(led_green, 0)
        grovepi.digitalWrite(led_blue, 0)   
        break
    except KeyboardInterrupt as e:#keyboard interrupt exception
        print(str(e))
        grovepi.digitalWrite(led_red, 0)
        grovepi.digitalWrite(led_green, 0)
        grovepi.digitalWrite(led_blue, 0)
        break
