import xbmcaddon
import xbmcgui
import socket, sys
import struct
from optparse import OptionParser
import inspect
import sqlite3
import shlex
import time
import datetime
import os
import xbmc
import math



addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

# Access log file: /users/chaseclarke/Library/Logs
def log(s):
    xbmc.log("EC521PROJ_LOG SERVICE: " + s)
    return 0

line1 = "This is our demo:"
line2 = "  we are demonstrating some common"
line3 = "  vulnerabilities in this file."


#spamming log so output can be easily seen
log("      ~ these numbers are written to find file output with ease ~ ")
for i in range(10):
    log(str(i))

################## exec vulnerability ##################

def callExec(command):
    log("executing command: " + command)
    exec(command)
    return 0

callExec("print('hi')")

################## ################## ##################

################## socket vulnerability ##################


def Sockets(httpRec):
    s = socket.socket()
    s.connect(('google.com', 80))
    s.send(httpRec)
    s.recv(8)
    s.close()
    return 0

http = b'GET / HTTP/1.1\r\nHost: google.com\r\n\r\n'
log(http)
Sockets(http)

################## ################## ##################

################## SQL vulnerability ##################

def create_table():
    # Create table
    try:
        c.execute('''CREATE TABLE people (name text, age text)''')
        return 0
    
    except:
        return 0

def insert_into_table(name, age):  # Vulnerable
    # Insert a row of data
    c.execute("INSERT INTO people (name, age) VALUES (?, ?)", (name, age))
    return 0

def close_db():
    # Save (commit) the changes
    conn.commit()
    conn.close()
    return 0

def read_db(name):
    c.execute("SELECT * FROM people WHERE name = '%s'" % name)
    log(str(c.fetchone()))
    return 0

def SQLVuln(name, age):
    
    global conn
    global c
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    
    # SQL
    create_table()
    insert_into_table(name, age)
    read_db(name)
    close_db()


#creating the database
SQLVuln("chase", 20)

################## ################## ##################

# printing to the popup window
xbmcgui.Dialog().ok(addonname, line1, line2, line3)



def sanitize(input):
    charList = ['|', '&', '<', '>', '!', '$', ';', '`']
    output = ""
    for i in input:
        if (i not in charList):
            output += i
    return output

################## accepting user input ##################

# source: https://forum.kodi.tv/showthread.php?tid=82250

def GUIEditExportName(name):
    exit = True
    while (exit):
        kb = xbmc.Keyboard('default', 'heading', True)
        kb.setDefault(name)
        kb.setHeading('Enter Movie Title')
        kb.setHiddenInput(False)
        kb.doModal()
        if (kb.isConfirmed()):
            name_confirmed  = kb.getText()
            name_correct = name_confirmed.count(' ')
            if (name_correct):
                GUIInfo(2,'English')
            else:
                name = name_confirmed
                exit = False
        else:
            GUIInfo(2,'English')
    return(name)


userIn = GUIEditExportName("")

#os.system("ls")
#os.system(userIn)
#exec(userIn1)

userIn1 = sanitize(userIn)
log(userIn1)

os.system(userIn)




################## ################## ##################

# end spam to log
for i in range(10):
    log(str(i))

