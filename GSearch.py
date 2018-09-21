import os, os.path
import json
#import win32com.client
import sqlite3
import threading
import numpy as np
import selenium.webdriver.chrome.service as service
import time
import psutil
import numpy as np
import argparse
import re
#import imutils
#import cv2
import sys
import csv
import subprocess
import getpass
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

@socketio.on('my_event', namespace='/test')
def test_message(message):

    print("my-event trigger")
    t1 = threading.Thread(target=googleSearch)
    #t2 = threading.Thread(target=googleSearch)
    t1.start()

    #t2.start()
    t1.join()
    googleSearchIndividual()
    #t2.join()

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

temprc = 1
arrtemp = np.array(range(1000), dtype='a1000').reshape(250,4)

def googleSearch():
    global temprc
    global arrtemp
    conn = sqlite3.connect('/home/dass/Coding/Python/flask/GoogleSearch/dassdb')
    c = conn.cursor()
    c.execute('delete from Master')
    conn.commit()
    conn.close()


    driver = webdriver.Firefox(executable_path='/home/dass/Coding/Python/geckodriver')
    driver.get("http://www.google.com")
    # assert "Python" in driver.title
    elem = driver.find_element_by_name("q")
    elem.clear()
    elem.send_keys("TCS")
    elem.send_keys(Keys.RETURN)
    #assert "No results found." not in driver.page_source

    for pa in range(2,3):
        time.sleep(1)
        content = driver.find_elements_by_class_name('rc')
        for x in content:
            acon = x.find_elements_by_tag_name('a')
            strcon = x.find_elements_by_class_name('st')

            strcon2= driver.execute_script("return arguments[0].outerHTML;", strcon[0])
            headingstr= driver.execute_script("return arguments[0].innerText;", acon[0])
            acon3= driver.execute_script("return arguments[0].outerHTML;", acon[0])

            #print(acon3)
            acon4= re.findall(r'href="(.*?)"',acon3)
            itemtext = ["TCS","selvgnb","YettoExtract",str(acon4[0]),str(strcon2),str(headingstr)]

            conn = sqlite3.connect('/home/dass/Coding/Python/flask/GoogleSearch/dassdb')
            c = conn.cursor()
            c.execute('insert into Master(CompanyName,Racf,Status,Url,googletext,googletagtext) values (?,?,?,?,?,?)', itemtext)
            conn.commit()
            conn.close()

    driver.close()
    driver.quit()


def googleSearchIndividual():
    global temprc
    global arrtemp

    driver = webdriver.Firefox(executable_path='/home/dass/Coding/Python/geckodriver')

    for i in range(1,100):

        iflag = 0

        try:
            conn = sqlite3.connect('/home/dass/Coding/Python/flask/GoogleSearch/dassdb')
            c = conn.cursor()
            c.execute('select * from Master where Status = "YettoExtract"')
            rows = c.fetchall()
            iflag = len(rows)
            if iflag != 0:
                rows1 = rows[0]
                c.execute('update Master set Status = "Extracted" where ID = "' + str(rows1[0]) + '"')
                conn.commit()
                conn.close()

            else:
                conn.close()
                driver.close()
                driver.quit()
                return
        except:
            print("end of loop")
            conn.close()
            driver.close()
            driver.quit()
            return


        driver.get(rows1[4])
        strbody3 = ""
        strbody = driver.find_elements_by_tag_name('p')
        for x in strbody:
            strbody2 = driver.execute_script("return arguments[0].innerText;", x)
            strbody3 = strbody3 + '/n' + strbody2
            
            #print(strbody2)


        conn = sqlite3.connect('/home/dass/Coding/Python/flask/GoogleSearch/dassdb')
        c = conn.cursor()
        c.execute('update Master set rawtext = "' + str(driver.page_source).replace('"', r'~') + '" where ID = "' + str(rows1[0]) + '"')
        conn.commit()
        conn.close()


    # #driver = webdriver.Firefox()
    # driver.get("http://www.python.org")
    # assert "Python" in driver.title
    # elem = driver.find_element_by_name("q")
    # elem.clear()
    # elem.send_keys("pycon")
    # elem.send_keys(Keys.RETURN)
    # assert "No results found." not in driver.page_source
    # driver.close()


if __name__ == '__main__':
    socketio.run(app, debug=True)


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
