import os, os.path
import json
import win32com.client
import sqlite3
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil
import numpy as np
import argparse
import re
import imutils
import cv2
import sys
import csv
import subprocess
import getpass
import ctypes
from shutil import copyfile
from PIL import Image
from numpy import genfromtxt
from sklearn import datasets, svm, metrics
from subprocess import Popen
from threading import Lock
from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pythoncom
from bs4 import BeautifulSoup

pythoncom.CoInitialize()
ShellWindowsCLSID = '{9BA05972-F6A8-11CF-A442-00A0C90A8F39}'
companyname = ""
googlesearchpage = ""
webflag = 0
otherwebvar = ""
#live path
#filepathtemp = '\\\\fs12edx\\grpareas\\os\\Data\\pythonsearch\\'
filepathtemp = 'X:\\Coding\\Python\\pythonsearch\\'

app = Flask(__name__)

@app.route('/')
def hello_name():
   return render_template('hello.html')


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()

tempsplit = ""

@app.route('/')
def index():
    return render_template('GSearch.html', async_mode=socketio.async_mode)

@socketio.on('click_submit', namespace='/test')
def test_message(message):
   global googlesearchpage
   global companyname
   global webflag
   print("Click submit event trigger")
   companyname = str(message['companyname'])
   #googlesearchpage = str(message['googlesearchpage'])

   print(message)
   mainprogram()
   #otherwebsites()
   webflag = 1
   ctypes.windll.user32.MessageBoxW(0, "Process has been completed. please click Show Result button.", "Agile Automation", 0)
   

   
   #emit('my_response_dass',
   #   {'CIN': 'sss', 'Name': 'sssssss'})


@socketio.on('extract_button', namespace='/test')
def test_extract_button(message):
   global otherwebvar
   global filepathtemp
   if os.path.exists(str(getpass.getuser()).lower() + ".xlsm"):
      print("Open Excel to extract otherwebsite result")
      xl=win32com.client.Dispatch("Excel.Application")
      xl.Workbooks.Open(os.path.abspath(str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=1)
      ws = xl.Worksheets("OtherWeb")
      for rc in range(2, 9):
         otherwebvar = str(otherwebvar) + "Artificial Intelligence Match Score : " + str(ws.Range("Y" + str(rc)).Value) + "<p></p>" + str(ws.Range("AA" + str(rc)).Value) +  str(ws.Range("Z" + str(rc)).Value) + '<hr class="my-4">' + "<p></p>"
      xl.Application.Quit()
   else:
      print("Unable to open the excel")
      
#emit('my_response_dass',
#     {'tabledata': 'sss', 'Name': 'sssssss'})
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from Master where Status = "Extracted"')
   rows = c.fetchall()
   conn.close()
   tempval = ""
   for row in rows:
      tempval = tempval + str(row[0]) + "<!>" + str(row[10]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<`>"
   print("extract_button : " + tempval)  
   emit('my_response_dass',
        {'resultdata': str(tempval).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebvar).replace('\n', r'<p></p>') })
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })

   print("extract_button ==> " + message)




@socketio.on('testmy_event', namespace='/test')
def test_message_timmer(message):
   global webflag
   global filepathtemp
   if webflag == 1:
      webflag = 0
      
      #emit('my_response_dass',
      #     {'tabledata': 'sss', 'Name': 'sssssss'})
      conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
      c = conn.cursor()
      c.execute('select * from Master where Status = "Extracted"')
      rows = c.fetchall()
      conn.close()
      tempval = ""
      for row in rows:
         
         tempval = tempval + str(row[0]) + "<!>" + str(row[10]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<!>" + str(row[10]) + "<`>"
      print("Timmer called : " + tempval)  
      emit('my_response_dass',
           {'resultdata': str(tempval).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebvar).replace('\n', r'<p></p>') })
      #emit('my_response_dass',
      #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })
      #emit('my_response_dass',
      #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })
    
   print("Timmer trigged ==> " + message)
    

@socketio.on('row_Index', namespace='/test')
def row_index_timmer(message):
   global filepathtemp
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from Master where Status = "Extracted"')
   rows = c.fetchall()
   conn.close()
   print(str(message))
   row = rows[int(message) -1]
   print("Timmer called : " + str(row))  
   emit('my_response_rowclick',
        {'resultdata': str(row[14]).replace('\n', r'<p></p>'), 'AInews': str(row[13]).replace('\n', r'<p></p>')})
    
    
   print("index call back" + message)



def removefile():
    global filepathtemp
    for item in os.listdir():
        if item.startswith(filepathtemp + getpass.getuser()) and item.endswith(".txt"):
           print("deleting file " + item)
           os.remove(item)

   
def mainprogram():
   global googlesearchpage
   global companyname
   global filepathtemp
   removefile()

   
      
   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("Main Program")
      xl=win32com.client.Dispatch("Excel.Application")
      xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = xl.Worksheets("SystemRef")
   else:
      print("Unable to open the excel")
   ws.Range("C7").Value = str(companyname)
   #ws.Range("B1").Value = str(googlesearchpage)
   xl.DisplayAlerts = False 
   xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
   xl.DisplayAlerts = True
   xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModGoogleSearch.Google_search")
   xl.DisplayAlerts = False 
   xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
   xl.DisplayAlerts = True
   xl.Application.Quit()

   exceltodb()
   t1 = threading.Thread(target=google_indi)
   #t2 = threading.Thread(target=google_indi)
   #t3 = threading.Thread(target=google_indi)

   #t4 = threading.Thread(target=otherwebsites)
   
   #t4 = threading.Thread(target=google_indi)
   #t5 = threading.Thread(target=google_indi)
   
   t1.start()
   #t2.start()
   #t3.start()
   #t4.start()
   #t5.start()
   
   t1.join()
   #t2.join()
   #t3.join()
   #t4.join()
   
   #backup process
   t1 = threading.Thread(target=google_indi)
   t1.start()
   t1.join()
   #t5.join()
   
   
def otherwebsites():
   global otherwebvar
   global filepathtemp
   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("Other website search start")
      xl=win32com.client.Dispatch("Excel.Application")
      xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = xl.Worksheets("OtherWeb")
      xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModOtherWeb.OtherWeb")
      print("Other website macro completed")
      xl.DisplayAlerts = False 
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      for rc in range(2, 9):
         #otherwebvar = str(otherwebvar) + "Artificial Intelligence Match Score : " + str(ws.Range("Y" & rc).Value) + str(ws.Range("AA" & rc).Value) +  str(ws.Range("Z" & rc).Value)
         otherwebvar = str(otherwebvar) + "Artificial Intelligence Match Score : " + str(ws.Range("Y" + str(rc)).Value) + "<p></p>" + str(ws.Range("AA" + str(rc)).Value) +  str(ws.Range("Z" + str(rc)).Value) + '<hr class="my-4">' + "<p></p>"
         
         
      xl.Application.Quit()

      
   else:
      print("Unable to open the excel")
   
   


def exceltodb():
    global filepathtemp
    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('DELETE FROM Master')
    conn.commit()
    conn.close()

    if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
        print("xl object")
        xl=win32com.client.Dispatch("Excel.Application")
        xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=1)
        ws = xl.Worksheets("DB")
        conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
        for rc in range(2, 65000):
            if str(ws.Cells(rc ,1).Value) != "None":
               
               c = conn.cursor()
                #print("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, Status) VALUES ('" + str(ws.Cells(rc ,11).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,1).Value).replace('"', r'~') + "', '"  + str(ws.Cells(rc ,2).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,3).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,4).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,5).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,6).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,7).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,8).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,9).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,10).Value).replace('"', r'~') + "')")

               dbID = str(ws.Cells(rc ,11).Value).replace('"', r'~').replace("'", r'')
               dbsearchkey = str(ws.Cells(rc ,1).Value).replace('"', r'~').replace("'", r'')
               dbsheetnumber = str(ws.Cells(rc ,2).Value).replace('"', r'~').replace("'", r'')
               dboutertext = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
               dbouterhtml = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
               dblinkref = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
               dburlfull = str(ws.Cells(rc ,6).Value).replace('"', r'~').replace("'", r'')
               dbfiletype = str(ws.Cells(rc ,7).Value).replace('"', r'~').replace("'", r'')
               dbemkeyword = str(ws.Cells(rc ,8).Value).replace('"', r'~').replace("'", r'')
               dbDomainname =  str(ws.Cells(rc ,9).Value).replace('"', r'~').replace("'", r'')
               dbcompanyname  = str(ws.Cells(rc ,10).Value).replace('"', r'~').replace("'", r'')
               dbStatus = 'YettoExtract'
               c.execute("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, Status) VALUES ('" + dbID + "', '" +  dbsearchkey + "', '"  + dbsheetnumber +  "', '" +  dboutertext + "', '" +  dbouterhtml +  "', '" +  dblinkref +  "', '" +  dburlfull +  "', '" +  dbfiletype +  "', '" +  dbemkeyword +  "', '" +  dbDomainname +  "', '" +  dbcompanyname + "', 'YettoExtract')")

               #c.execute("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, Status) VALUES ('" + str(ws.Cells(rc ,11).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,1).Value).replace('"', r'~') + "', '"  + str(ws.Cells(rc ,2).Value).replace('"', r'~') +  "', '" +  str("").replace('"', r'~') + "', '" +  str("").replace('"', r'~') +  "', '" +  str("").replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,6).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,7).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,8).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,9).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,10).Value).replace('"', r'~') + "', 'YettoExtract')")
               conn.commit()
            else:
                print("break executed")
                break
        conn.close()

        xl.Application.Quit()


    else:
            print("Unable to open the excel")



def google_indi():
    global filepathtemp
    #pythoncom.CoInitialize()
    tempurl = ""
    rowcount = 0
    #ie = win32com.client.Dispatch("InternetExplorer.Application")
    #ie.Visible = 1 #make this 0, if you want to hide IE window


    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('select * from Master where Status = "YettoExtract"')
    rows = c.fetchall()
    rowcount = len(rows)
    conn.close()

    for i in range(rowcount):
        try:
            conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
            c = conn.cursor()
            c.execute('select * from Master where Status = "YettoExtract"')
            rows = c.fetchall()
            iflag = len(rows)
            print(iflag)
            if iflag != 0:
                rows1 = rows[0]
                print(rows1)
                tempurl = rows1[6]
                print(rows1[0])
                c.execute('update Master set Status = "Extracted" where ID = "' + str(rows1[0]) + '"')
                print("after update query")
                conn.commit()
                conn.close()
                url = tempurl
                #IE started
                print(url)
                if rows1[7] == 'None':
                    #time.sleep(0.5)
                    #ie.Navigate(url)
                    #time.sleep(0.5)
                    #it takes a little while for page to load. sometimes takes 5 sec.
                    #print(ie.Busy)
##                    temptime = 0
##                    while ie.Busy == True and temptime < 10:
##                        print("ie busy")
##                        temptime = temptime + 1
##                        time.sleep(0.5)
##                    time.sleep(1)
##                    text = str(ie.Document.body.outerHTML)
                    #fnamet = str(rows1 + ".txt")
                    print("Reading file")
                    file = open(filepathtemp + rows1[0] + ".txt", encoding="utf8")
                    contemp = file.read()
                    file.close()
                    soup = BeautifulSoup(contemp, 'html.parser')
                    #soup = BeautifulSoup(f)
                    
                    print("closing file")
                    page = soup.find_all('p')
                    print(page)
                    #print(page.getText())
                    print("soup page extracted")
                    tempstr = ""
                    for page2 in page:
                        tempstr = tempstr + page2.text + '\n'
                        #print(page2.text)
                    #print(tempstr)

                    tempstr = str(tempstr).replace('"', r'~')
                    tempstr = str(tempstr).replace("'", r"~")
                    tempstr = str(tempstr).replace('\n\n', r'\n')
                    tempstr = str(tempstr).replace('\r\n\r\n', r'\r\n')

                    lines_list = tokenize.sent_tokenize(tempstr)
                    #sentences.extend(strbody3)
                    sid = SentimentIntensityAnalyzer()
                    strsen =""
                    strsentag =""
                    AIscore = 0
                    for sentence in lines_list:
                        #print(sentence)
                        ss = sid.polarity_scores(sentence)
                        if ss['neg'] > 0:
                            AIscore = AIscore + int(ss['neg']*10)
                            strsen = strsen + "AI Score = " + str(ss['neg'] * 10) + " ==> " + sentence + '\n'
                            strsentag = strsentag + '<b class="text-danger">' + sentence + '(AI Score = ' + str(ss['neg']) + ')</b>' + '\n'

                            #print("AI Score = " + str(ss['neg']) + " ==> " + sentence)
                        else:
                            strsentag = strsentag + sentence + '\n'
                    
                    conn = sqlite3.connect(str(filepathtemp + getpass.getuser()).lower() + '.db')
                    c = conn.cursor()
                    print("rawtext to db")
                    c.execute("update Master set rawtext = '" + str(tempstr) + "', rawtexttag = '" + str(strsentag) + "', negtext = '" + str(strsen) + "', AIScore = '" + str(AIscore) + "' where ID = '" + str(rows1[0]) + "'")
                    conn.commit()
                    conn.close()
                
            else:
                conn.close()
                #ie.Quit()
                
                return
        except:
            print("end of loop")
            conn.close()
            
        #text is in unicode, so get it into a string
        #text = unicode(text)
        #text = text.encode('ascii','ignore')
        #save some memory by quitting IE! **very important** 
    #ie.Quit()


         
if __name__ == '__main__':
   
   if os.path.exists(filepathtemp + getpass.getuser() + ".xlsm"):
      os.remove(filepathtemp + getpass.getuser() + ".xlsm")
      copyfile(filepathtemp + "AI_AML_Template.xlsm", filepathtemp + getpass.getuser() + ".xlsm")
   else:
      copyfile(filepathtemp + "AI_AML_Template.xlsm", filepathtemp + getpass.getuser() + ".xlsm")

   if os.path.exists(filepathtemp + getpass.getuser() + ".db"):
      os.remove(filepathtemp + getpass.getuser() + ".db")
      copyfile(filepathtemp + "Template.db", filepathtemp + getpass.getuser() + ".db")
   else:
      copyfile(filepathtemp + "Template.db", filepathtemp + getpass.getuser() + ".db")
      
   socketio.run(app, debug=True)



##
##def google_indi():
##    pythoncom.CoInitialize()
##    tempurl = ""
##    rowcount = 0
##    ie = win32com.client.Dispatch("InternetExplorer.Application")
##    ie.Visible = 1 #make this 0, if you want to hide IE window
##
##
##    conn = sqlite3.connect(str(getpass.getuser()).lower() + '.db')
##    c = conn.cursor()
##    c.execute('select * from Master where Status = "YettoExtract"')
##    rows = c.fetchall()
##    rowcount = len(rows)
##    conn.close()
##
##    for i in range(rowcount):
##        try:
##            conn = sqlite3.connect(str(getpass.getuser()).lower() + '.db')
##            c = conn.cursor()
##            c.execute('select * from Master where Status = "YettoExtract"')
##            rows = c.fetchall()
##            iflag = len(rows)
##            print(iflag)
##            if iflag != 0:
##                rows1 = rows[0]
##                print(rows1)
##                tempurl = rows1[6]
##                print(rows1[0])
##                c.execute('update Master set Status = "Extracted" where ID = "' + str(rows1[0]) + '"')
##                print("after update query")
##                conn.commit()
##                conn.close()
##                url = tempurl
##                #IE started
##                print(url)
##                if rows1[7] == 'None':
##                    time.sleep(0.5)
##                    ie.Navigate(url)
##                    time.sleep(0.5)
##                    #it takes a little while for page to load. sometimes takes 5 sec.
##                    print(ie.Busy)
##                    temptime = 0
##                    while ie.Busy == True and temptime < 10:
##                        print("ie busy")
##                        temptime = temptime + 1
##                        time.sleep(0.5)
##                    time.sleep(1)
##                    text = str(ie.Document.body.outerHTML)
##                    soup = BeautifulSoup(text, 'html.parser')
##                    page = soup.find_all('p')
##                    #print(page.getText())
##                    print("soup page extracted")
##                    tempstr = ""
##                    for page2 in page:
##                        tempstr = tempstr + page2.text + '\n'
##                        #print(page2.text)
##                    #print(tempstr)
##
##                    tempstr = str(tempstr).replace('"', r'~')
##                    tempstr = str(tempstr).replace("'", r"~")
##                    tempstr = str(tempstr).replace('\n\n', r'\n')
##                    tempstr = str(tempstr).replace('\r\n\r\n', r'\r\n')
##
##                    lines_list = tokenize.sent_tokenize(tempstr)
##                    #sentences.extend(strbody3)
##                    sid = SentimentIntensityAnalyzer()
##                    strsen =""
##                    strsentag =""
##                    AIscore = 0
##                    for sentence in lines_list:
##                        #print(sentence)
##                        ss = sid.polarity_scores(sentence)
##                        if ss['neg'] > 0:
##                            AIscore = AIscore + int(ss['neg']*100)
##                            strsen = strsen + "AI Score = " + str(ss['neg'] * 100) + " ==> " + sentence + '\n'
##                            strsentag = strsentag + '<b class="text-danger">' + sentence + '(AI Score = ' + str(ss['neg']) + ')</b>' + '\n'
##
##                            #print("AI Score = " + str(ss['neg']) + " ==> " + sentence)
##                        else:
##                            strsentag = strsentag + sentence + '\n'
##                    
##                    conn = sqlite3.connect(str(getpass.getuser()).lower() + '.db')
##                    c = conn.cursor()
##                    print("rawtext to db")
##                    c.execute("update Master set rawtext = '" + str(tempstr) + "', rawtexttag = '" + str(strsentag) + "', negtext = '" + str(strsen) + "', AIScore = '" + str(AIscore) + "' where ID = '" + str(rows1[0]) + "'")
##                    conn.commit()
##                    conn.close()
##                
##            else:
##                conn.close()
##                ie.Quit()
##                
##                return
##        except:
##            print("end of loop")
##            conn.close()
##            
##        #text is in unicode, so get it into a string
##        #text = unicode(text)
##        #text = text.encode('ascii','ignore')
##        #save some memory by quitting IE! **very important** 
##    ie.Quit()
##
##
##
















    
    #t1 = threading.Thread(target=googleSearch)
    #t2 = threading.Thread(target=googleSearch)
    #t1.start()
    #t1.join()

    #t1 = threading.Thread(target=googleSearchIndividual)
    #t1.start()


##    t2 = threading.Thread(target=googleSearchIndividual)
##    t2.start()
##
##
##    t3 = threading.Thread(target=googleSearchIndividual)
##    t3.start()
##
##
##    t4 = threading.Thread(target=googleSearchIndividual)
##    t4.start()

    #t1.join()
##    t2.join()
##    t3.join()
##    t4.join()
##    #t2.join()

    #googleSearch()
    #session['receive_count'] = session.get('receive_count', 0) + 1
    #emit('my_response_dass',
    #     {'data': message['data'], 'count': session['receive_count']})
    # emit('my_bo',
    #      {'CIN': Customer_ID, 'Name': Salutation, 'Country_of_birth': Country_of_birth, 'Tax_Residence1': Tax_Residence1, 'Tax_Residence2': Tax_Residence2, 'Tax_Residence3': Tax_Residence3, 'Tax_Residence4': Tax_Residence4, 'Tax_Residence5': Tax_Residence5, 'Tax_Residence6': Tax_Residence6, 'Tax_Residence7': Tax_Residence7, 'Tax_Residence8': Tax_Residence8, 'Tax_Residence9': Tax_Residence9})
    # emit('img_result',
    #      {'img_resultss': resultimg})

# @socketio.on('disconnect', namespace='/test')
# def test_disconnect():
#     print('Client disconnected', request.sid)
#
#
# @socketio.on('my_eventtesting', namespace='/test')
# def bo_data(message):
#     global Customer_ID
#     emit('my_bo',
#          {'CIN': Customer_ID, 'Name': Salutation})
#

##temprc = 1
##arrtemp = np.array(range(1000), dtype='a1000').reshape(250,4)
##
##def googleSearch():
##    global temprc
##    global arrtemp
##    conn = sqlite3.connect('dassdb')
##    c = conn.cursor()
##    c.execute('delete from Master')
##    conn.commit()
##    conn.close()
##
##
####    #driver = webdriver.Firefox(executable_path='/home/dass/Coding/Python/geckodriver')
####
####    options = webdriver.ChromeOptions()
####    #options.add_argument("--disable-extensions")
####    #options.add_argument('--disable-useAutomationExtension')
####    options.add_experimental_option("useAutomationExtension",False)
####    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
####    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
####    
####    chrome_driver_binary = "chromedriver.exe"
####    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
####
##    driver = webdriver.Ie("IEDriverServer.exe")
##    time.sleep(1)
##    driver.get("http://www.google.com")
##    time.sleep(4)
##    # assert "Python" in driver.title
##    elem = driver.find_element_by_name("q")
##    elem.clear()
##    elem.send_keys("TCS")
##    elem.send_keys(Keys.RETURN)
##    #assert "No results found." not in driver.page_source
##
##    for pa in range(2,4):
##        time.sleep(1)
##        content = driver.find_elements_by_class_name('rc')
##        for x in content:
##            acon = x.find_elements_by_tag_name('a')
##            strcon = x.find_elements_by_class_name('st')
##
##            strcon2= driver.execute_script("return arguments[0].outerHTML;", strcon[0])
##            headingstr= driver.execute_script("return arguments[0].innerText;", acon[0])
##            acon3= driver.execute_script("return arguments[0].outerHTML;", acon[0])
##
##            #print(acon3)
##            acon4= re.findall(r'href="(.*?)"',acon3)
##            itemtext = ["TCS","selvgnb","YettoExtract",str(acon4[0]),str(strcon2),str(headingstr)]
##
##            conn = sqlite3.connect('DassDB.db')
##            c = conn.cursor()
##            c.execute('insert into Master(CompanyName,Racf,Status,Url,googletext,googletagtext) values (?,?,?,?,?,?)', itemtext)
##            conn.commit()
##            conn.close()
##
##    driver.close()
##    driver.quit()
##
##
##def googleSearchIndividual():
##    global temprc
##    global arrtemp
##
####    options = webdriver.ChromeOptions()
####    #options.add_argument("--disable-extensions")
####    #options.add_argument('--disable-useAutomationExtension')
####    options.add_experimental_option("useAutomationExtension",False)
####    options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
####    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
####    
####    chrome_driver_binary = "chromedriver.exe"
####    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
##    driver = webdriver.Ie("IEDriverServer.exe")
##    
##    #driver = webdriver.Firefox(executable_path='/home/dass/Coding/Python/geckodriver')
##
##    for i in range(1,100):
##
##        iflag = 0
##
##        try:
##            conn = sqlite3.connect('DassDB.db')
##            c = conn.cursor()
##            c.execute('select * from Master where Status = "YettoExtract"')
##            rows = c.fetchall()
##            iflag = len(rows)
##            if iflag != 0:
##                rows1 = rows[0]
##                c.execute('update Master set Status = "Extracted" where ID = "' + str(rows1[0]) + '"')
##                conn.commit()
##                conn.close()
##
##            else:
##                conn.close()
##                driver.close()
##                driver.quit()
##                return
##        except:
##            print("end of loop")
##            conn.close()
##            driver.close()
##            driver.quit()
##            return
##
##        time.sleep(2)
##        driver.get(rows1[1])
##        time.sleep(2)
##        strbody3 = ""
##        strbody = driver.find_elements_by_tag_name('p')
##        for x in strbody:
##            strbody2 = driver.execute_script("return arguments[0].innerText;", x)
##            strbody3 = strbody3 + '/n' + strbody2
##
##        lines_list = tokenize.sent_tokenize(strbody3)
##        #sentences.extend(strbody3)
##        sid = SentimentIntensityAnalyzer()
##        strsen =""
##        strsentag =""
##        for sentence in lines_list:
##            #print(sentence)
##            ss = sid.polarity_scores(sentence)
##            if ss['neg'] > 0:
##                strsen = strsen + "AI Score = " + str(ss['neg']) + " ==> " + sentence + '/n'
##                strsentag = strsentag + "<b>" + sentence + "(AI Score = " + str(ss['neg']) + ")</b>" + '/n'
##
##                print("AI Score = " + str(ss['neg']) + " ==> " + sentence)
##            else:
##                strsentag = strsentag + sentence + '/n'
##            #print(strbody2)
##
##
##        conn = sqlite3.connect('DassDB.db')
##        c = conn.cursor()
##        c.execute('update Master set rawtext = "' + str(driver.page_source).replace('"', r'~') + '", sentext = "' + str(strsen).replace('"', r'~') + '", sentexttag = "' + str(strsentag).replace('"', r'~') + '"  where ID = "' + str(rows1[0]) + '"')
##        conn.commit()
##        conn.close()


    # #driver = webdriver.Firefox()
    # driver.get("http://www.python.org")
    # assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()





# CREATE TABLE `Master` (
# 	`CompanyName`	TEXT,
# 	`Racf`	TEXT,
# 	`Status`	TEXT,
# 	`Url`	TEXT,
# 	`googletext`	TEXT,
# 	`googletagtext`	TEXT,
# 	`rawtext`	TEXT,
# 	`sentext`	TEXT,
# 	`sentexttag`	TEXT
# );
