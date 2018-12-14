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
#from PIL import Image
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
otherwebresult = ""
ProfileSearchCheckBox = ""
WorldCheckBox = ""
Fulltestvar = ""
worldchecktab = ""

#live path
#filepathtemp = '\\\\fs12edx\\grpareas\\os\\Data\\pythonsearch\\'
#filepathtemp = 'X:\\Coding\\Python\\pythonsearch\\'
filepathtemp = ""

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
   global Fulltestvar
   print("Click submit event trigger")
   companyname = str(message['companyname'])
   ProfileSearchCheckBox = str(message['ProfileSearchCheckBox'])
   WorldCheckBox = str(message['WorldCheckBox'])
   Fulltestvar = message
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
   global otherwebresult
   global worldchecktab
   # if os.path.exists(str(getpass.getuser()).lower() + ".xlsm"):
   #    print("Open Excel to extract otherwebsite result")
   #    xl=win32com.client.Dispatch("Excel.Application")
   #    xl.Workbooks.Open(os.path.abspath(str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=1)
   #    ws = xl.Worksheets("OtherWeb")
   #    for rc in range(2, 9):
   #       otherwebvar = str(otherwebvar) + "Artificial Intelligence Match Score : " + str(ws.Range("Y" + str(rc)).Value) + "<p></p>" + str(ws.Range("AA" + str(rc)).Value) +  str(ws.Range("Z" + str(rc)).Value) + '<hr class="my-4">' + "<p></p>"
   #    xl.Application.Quit()
   # else:
   #    print("Unable to open the excel")

#emit('my_response_dass',
#     {'tabledata': 'sss', 'Name': 'sssssss'})
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from Master where Status = "Extracted"')
   rows = c.fetchall()
   conn.close()
   tempval = ""
   for row in rows:
      tempval = tempval + str(row[0]) + "<!>" + str(row[10]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<!>" + str(row[3]) + "<`>"
   tempval = tempval[:-3]
   #print("extract_button : " + tempval)
   print("Timmer called : " + tempval)
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from WorldCheck')
   rows = c.fetchall()
   conn.close()
   worldchecktab = ""
   print("worldchecktab ===================")
   rcw = 1
   for row in rows:
       worldchecktab = worldchecktab + str(rcw) + "<!>" + str(row[0]) + "<!>" +  str(row[2]) + "<!>"  + str(row[3]) + "<!>" + str(row[5]) + "<!>" + str(row[1]).replace('<body', r'<p') + "<`>"
       rcw = rcw + 1

   #print(worldchecktab)
   worldchecktab = worldchecktab[:-3]
   print("Extract button ============")

   emit('my_response_dass',
        {'resultdata': str(tempval).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebresult).replace('\n', r'<p></p>'), 'worldchecktab' : str(worldchecktab).replace('\n', r'<p></p>')})
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })

   print("extract_button ==> " + message)




@socketio.on('testmy_event', namespace='/test')
def test_message_timmer(message):
   global webflag
   global filepathtemp
   global otherwebresult
   global worldchecktab
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

         tempval = tempval + str(row[0]) + "<!>" + str(row[10]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<!>" + str(row[10])  + str(row[3]) + "<`>"
      tempval = tempval[:-3]

      print("Timmer called : " + tempval)
      conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
      c = conn.cursor()
      c.execute('select * from WorldCheck')
      rows = c.fetchall()
      conn.close()
      worldchecktab = ""
      for row in rows:
          worldchecktab = worldchecktab + '<h3>' + str(row[0]) + '</h3>' + str(row[1]).replace('<body', r'<p')

      print(worldchecktab)
      print("testmy_event ========")
      emit('my_response_dass',
           {'resultdata': str(tempval).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebresult).replace('\n', r'<p></p>'), 'worldchecktab' : str(worldchecktab).replace('\n', r'<p></p>')})
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
   c.execute('select * from Master where id = "' + message + '"')
   rows = c.fetchall()
   conn.close()
   print(str(message))
   #print(rows)
   #row = rows[int(message) -1]
   row = rows[0]
   print("Timmer called : " + str(row))
   print("Timmer called : " + str(row[0]))
   emit('my_response_rowclick',
        {'resultdata': str(row[14]).replace('\n', r'<p></p>'), 'AInews': str(row[13]).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebresult).replace('\n', r'<p></p>') })


   print("index call back" + message)


@socketio.on('GenerateReport', namespace='/test')
def fun_generate_report(message):
   global filepathtemp
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from Master where id = "' + message + '"')
   rows = c.fetchall()
   conn.close()
   print(str(message))
   #print(rows)
   #row = rows[int(message) -1]
   row = rows[0]
   print("Timmer called : " + str(row))
   print("Timmer called : " + str(row[0]))
   emit('my_response_rowclick',
        {'resultdata': str(row[14]).replace('\n', r'<p></p>'), 'AInews': str(row[13]).replace('\n', r'<p></p>'), 'otherwebvar': str(otherwebresult).replace('\n', r'<p></p>') })


   print("index call back" + message)


def removefile():
    global filepathtemp
    for item in os.listdir():
        if item.startswith(filepathtemp + getpass.getuser()) and item.endswith(".html"):
           print("deleting file " + item)
           os.remove(item)


def mainprogram():
   global googlesearchpage
   global companyname
   global filepathtemp
   global ProfileSearchCheckBox
   global WorldCheckBox
   global Fulltestvar

   removefile()



   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("Main Program")
      xl=win32com.client.Dispatch("Excel.Application")
      workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = workbook.Worksheets("SystemRef")
      ws.Range("C7").Value = str(companyname)


      ws.Range("B20").Value = str(ProfileSearchCheckBox)
      ws.Range("B21").Value = str(WorldCheckBox)


    #ws.Range("B1").Value = str(googlesearchpage)
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModGoogleSearch.Google_search")
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      workbook.Close(True)
      #xl.Application.Quit()

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
      print("other profile " + str(Fulltestvar))
      tempvar2 = str(Fulltestvar)
      if "ProfileWebsitetrue" in str(tempvar2):
          otherwebsites()
      if "WorldChecktrue" in str(tempvar2):
          worldcheckfun()
   else:
      print("Unable to open the excel")

def worldcheckfun():
   global worldchecktab

   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("WorldCheck search start")
      xl=win32com.client.Dispatch("Excel.Application")
      workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = xl.Worksheets("WorldCheck")
      #Temp disable the run macro command
      xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModWorldCheck.WorldCheck")
      print("WorldCheck macro completed")
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      rc = 1
      conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
      for rc in range(2, 65000):
          if str(ws.Cells(rc ,1).Value) != "None":
             c = conn.cursor()
             rc = rc + 1
             dbCompanyName = str(ws.Cells(rc ,1).Value).replace('"', r'~').replace("'", r'')
             dbCompanyResult = str(ws.Cells(rc ,2).Value).replace('"', r'~').replace("'", r'')
             dbCompanyReport = str(ws.Cells(rc ,3).Value).replace('"', r'~').replace("'", r'')
             dbCompanysub = str(ws.Cells(rc ,4).Value).replace('"', r'~').replace("'", r'')
             dbOrgName = str(ws.Cells(rc ,5).Value).replace('"', r'~').replace("'", r'')
             dbMatchScore = str(ws.Cells(rc ,6).Value).replace('"', r'~').replace("'", r'')

             c.execute("INSERT into WorldCheck (CompanyName, CompanyResultFull, CompanyReport, CompanySub, OrgName, MatchScore) VALUES ('" + dbCompanyName + "', '" +  dbCompanyResult + "', '" +  dbCompanyReport + "', '" +  dbCompanysub + "', '" +  dbOrgName + "', '" + dbMatchScore + "')")

             #c.execute("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, Status) VALUES ('" + str(ws.Cells(rc ,11).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,1).Value).replace('"', r'~') + "', '"  + str(ws.Cells(rc ,2).Value).replace('"', r'~') +  "', '" +  str("").replace('"', r'~') + "', '" +  str("").replace('"', r'~') +  "', '" +  str("").replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,6).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,7).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,8).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,9).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,10).Value).replace('"', r'~') + "', 'YettoExtract')")
             conn.commit()
          else:
              print("break executed")
              break
      conn.close()
      workbook.Close(True)
      #xl.Application.Close()
      #xl.Application.Quit()


   else:
       print("Unable to open the excel")





def otherwebsites():
   global otherwebvar
   global filepathtemp
   global otherwebresult
   tempresult = ""
   tempfilename = ["_Other_00001.html","_Other_00002.html","_Other_00003.html","_Other_00004.html","_Other_00005.html","_Other_00006.html","_Other_00007.html","_Other_00008.html"]
   if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
      print("Other website search start")
      xl=win32com.client.Dispatch("Excel.Application")
      workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
      ws = xl.Worksheets("OtherWeb")
      xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModOtherWeb.OtherWeb")
      print("Other website macro completed")
      xl.DisplayAlerts = False
      xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
      xl.DisplayAlerts = True
      rc = 1
      rc2 = 1

      ws2 = xl.Worksheets("OtherWeb")

      for val in range(2,500):
          rc = rc + 1
          rc2 = rc2 + 1
          if rc2 > 10:
              rc2 = 2
          if ws2.Cells(rc ,26).Value != "" and ws2.Cells(rc ,26).Value is not None:
             #print("File Found " + item)
             #print("Reading file")
             file = open(ws2.Cells(rc ,26).Value, encoding="utf8")
             contemp = file.read()
             file.close()
             soup = BeautifulSoup(contemp, 'html.parser')
             ws = xl.Worksheets("Mapping")

             tempresult = tempresult + '<h3><a href="' + ws2.Cells(rc ,28).Value + '" target="_blank"> ' + ws2.Cells(rc ,27).Value + '</a></h3><p><b>Artificial intelligent matching sore: ' + str(ws2.Cells(rc ,25).Value) + '</b></p>'
             for x in range(29,40):
                 if ws.Cells(rc2,x).Value != "" and ws.Cells(rc2,x).Value is not None:
                     tempstr2 = ws.Cells(rc2,x).Value
                     #print("Cell Value" + tempstr2)
                     temp3  = tempstr2.split(":")
                     mydivs = soup.findAll("", {"class": temp3[1]})
                     if len(temp3) == 2:
                         for page2 in mydivs:
                             tempresult = tempresult + '<p>' + page2.text + '</p>'
                             #print(temp3 + page2.text)
                     elif  len(temp3) == 3:

                         try:
                             for page2 in mydivs[temp3[3]]:
                                 tempresult = tempresult + '<p>' + page2.text + '</p>'
                         except:
                             print("Unable to read value " + str(temp3))
                              #print(temp3 + page2.text)
          else:
              workbook.Close(True)
              #xl.Application.Close()
              #xl.Application.Quit()
              otherwebresult = tempresult
              return


   else:
      print("Unable to open the excel")

   otherwebresult = tempresult
   #print(tempresult)


def exceltodb():
    global filepathtemp
    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('DELETE FROM Master')
    conn.commit()
    conn.close()
    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('DELETE FROM WorldCheck')
    conn.commit()
    conn.close()

    if os.path.exists(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"):
        print("xl object")
        xl=win32com.client.Dispatch("Excel.Application")
        workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=1)
        ws = xl.Worksheets("DB")
        conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
        for rc in range(2, 65000):
            if str(ws.Cells(rc ,1).Value) != "None":

               c = conn.cursor()
                #print("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, Status) VALUES ('" + str(ws.Cells(rc ,11).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,1).Value).replace('"', r'~') + "', '"  + str(ws.Cells(rc ,2).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,3).Value).replace('"', r'~') + "', '" +  str(ws.Cells(rc ,4).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,5).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,6).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,7).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,8).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,9).Value).replace('"', r'~') +  "', '" +  str(ws.Cells(rc ,10).Value).replace('"', r'~') + "')")

               dbID = str(ws.Cells(rc ,11).Value).replace('"', r'~').replace("'", r'')
               dbsearchkey = str(ws.Cells(rc ,1).Value).replace('"', r'~').replace("'", r'')
               dbsheetnumber = str(ws.Cells(rc ,2).Value).replace('"', r'~').replace("'", r'')
               dboutertext = str(ws.Cells(rc ,3).Value).replace('"', r'~').replace("'", r'').replace("'", r'').replace("\n\n", r'\n')
               dbouterhtml = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
               dblinkref = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
               dburlfull = str(ws.Cells(rc ,6).Value).replace('"', r'~').replace("'", r'')
               #dbfiletype = str(ws.Cells(rc ,7).Value).replace('"', r'~').replace("'", r'')
               dbfiletype = str(ws.Cells(rc ,14).Value).replace('"', r'~').replace("'", r'')
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
        workbook.Close(True)
        #xl.Application.Close()
        #xl.Application.Quit()


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
                #if rows1[7] == 'None':
                if True:
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
                    file = open(filepathtemp + rows1[0] + ".html", encoding="utf8")
                    contemp = file.read()
                    file.close()
                    soup = BeautifulSoup(contemp, 'html.parser')
                    #soup = BeautifulSoup(f)

                    #print("closing file")
                    page = soup.find_all('p')
                    pageh1 = soup.find_all('h1')
                    pageh2 = soup.find_all('h2')
                    pageh3 = soup.find_all('h3')
                    pageh4 = soup.find_all('h4')
                    pageh5 = soup.find_all('h5')
                    pageh6 = soup.find_all('h6')

                    #print(page)
                    #print(page.getText())
                    print("soup page extracted")
                    tempstr = ""
                    for page2 in pageh1:
                        tempstr = tempstr + page2.text + '\n'
                    for page2 in pageh2:
                        tempstr = tempstr + page2.text + '\n'
                    for page2 in pageh3:
                        tempstr = tempstr + page2.text + '\n'
                    for page2 in pageh4:
                        tempstr = tempstr + page2.text + '\n'
                    for page2 in pageh5:
                        tempstr = tempstr + page2.text + '\n'
                    for page2 in pageh6:
                        tempstr = tempstr + page2.text + '\n'


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
    #otherwebsites()

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
