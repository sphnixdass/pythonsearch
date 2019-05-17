from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.chrome.service as service
from bs4 import BeautifulSoup
import os, os.path
import sys
import getpass
from shutil import copyfile
import threading
import numpy as np
import psutil
from urllib.parse import urlparse
import sqlite3
import time
from time import sleep
from datetime import datetime
from datetime import timedelta

from flask import Flask, render_template, session, request, redirect, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, close_room, rooms, disconnect
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import ctypes
from win32com.shell import shell


companyname = ""
googlesearchpage = ""
webflag = 0
otherwebvar = ""
otherwebresult = ""
ProfileSearchCheckBox = ""
WorldCheckBox = ""
Fulltestvar = ""
worldchecktab = ""
domainname = ""
searchlist = ""
desktoppath =""

dll = ctypes.windll.shell32
df = shell.SHGetDesktopFolder()
pidl = df.ParseDisplayName(0, None,"::{450d8fba-ad25-11d0-98a8-0800361b1103}")[1]
path = shell.SHGetPathFromIDList(pidl)
desktoppath = path.decode('ascii').replace('\\\\','\\') + '\\Profile\\Desktop\\'

app = Flask(__name__)

@app.route('/')
def hello_name():
   return render_template('hello.html')


async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

tempsplit = ""

@app.route('/')
def index():
    return render_template('DassTemplate.html', async_mode=socketio.async_mode)

@socketio.on('click_submit', namespace='/test')
def test_message(message):
    global googlesearchpage
    global companyname
    global domainname
    global webflag
    global Fulltestvar
    global searchlist
    print("Click submit event trigger")
    companyname = str(message['companyname'])
    domainname = str(message['domainname'])
    searchlist = str(message['searchlist'])

    Fulltestvar = message
    #googlesearchpage = str(message['googlesearchpage'])

    print(message)
    
    removefile()
    cleardb()
    #chromeprint(strtemp,temppage = 4, addkeyword = "")
    xsp = companyname.split('<,>')
    
    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('select * from InputTable')
    rows = c.fetchall()
    conn.close()
    tempvalinput = ""
    for row in rows:
#        tempvalinput = tempvalinput + str(row[0])
        for x in range(0,len(xsp) -1):
            sp = xsp[x].split('<:>')
            print(str(sp[0]))
            print(sp[1])
            chromeprint(str(sp[0]),str(int(sp[1]) + 1), str(row[0]))
            print(x)
    google_indi()
    

    removefile()
    #mainprogram()
    #otherwebsites()
    webflag = 1
    MB_TOPMOST=0x40000
    ctypes.windll.user32.MessageBoxW(0, "Process has been completed. please click Show Result button.", "Agile Automation", MB_TOPMOST)



    #emit('my_response_dass',
    #   {'CIN': 'sss', 'Name': 'sssssss'})


@socketio.on('extract_button', namespace='/test')
def test_extract_button(message):
   global otherwebvar
   global filepathtemp
   global otherwebresult
   global worldchecktab

   #input str
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('select * from InputTable')
   rows = c.fetchall()
   conn.close()
   tempvalinput = ""
   for row in rows:
       tempvalinput = tempvalinput + str(row[0])
       
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   if message['selectedIndex'] >= 0:
       c.execute('select * from Master where Status = "Extracted" and ListSelection = "' + str("{0:.1f}".format(message['selectedIndex'])) + '"')
   else:
       c.execute('select * from Master where Status = "Extracted"')
       
   #c.execute('select * from Master where Status = "Extracted"')
   rows = c.fetchall()
   conn.close()
   tempval = ""
   for row in rows:
      tempval = tempval + str(row[0]) + "<!>" + str(row[1]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<!>" + str(row[3]) + "<!>" + str(row[14]) + "<`>"
   tempval = tempval[:-3]
   #print("extract_button : " + tempval)
   print("Timmer called : " + tempval)


   emit('my_response_dass',
        {'resultdata': str(tempval).replace('\n', r'<p></p>'),  'Tempinput' : str(tempvalinput)})
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })
   #emit('my_response_dass',
   #     {'resultdata': str(tempval).replace('\n', r'<p></p>'), '': str(otherwebvar).replace('\n', r'<p></p>') })

   #print("extract_button ==> " + message)




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

         tempval = tempval + str(row[0]) + "<!>" + str(row[1]) + "<!>" + str(row[6]) + "<!>" + str(row[8]) + "<!>" + str(row[2]) + "<!>" + str(row[15]) + "<!>" + str(row[7]) + "<!>" + str(row[10])  + str(row[3]) + "<`>"
      tempval = tempval[:-3]

      print("Timmer called : " + tempval)

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


@socketio.on('row_delete', namespace='/test')
def row_delete_timmer(message):
   global filepathtemp
   conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
   c = conn.cursor()
   c.execute('Delete from Master where id = "' + message + '"')
   conn.commit()
   conn.close()
   print("row deleted : " + message)
   


@socketio.on('OpenAuditFile', namespace='/test')
def fun_OpenAuditFile(message):
   global filepathtemp

   print("Audit File function Triggered")

   xl=win32com.client.Dispatch("Excel.Application")
   workbook = xl.Workbooks.Open(os.path.abspath(filepathtemp + str(getpass.getuser()).lower() + ".xlsm"), ReadOnly=0)
   xl.DisplayAlerts = True
   xl.Application.Run(filepathtemp + str(getpass.getuser()).lower() + ".xlsm!ModGoogleSearch.AuditFileOpen")
   xl.DisplayAlerts = False
   xl.Application.Save() # if you want to save then uncomment this line and change delete the ", ReadOnly=1" part from the open function.
   xl.DisplayAlerts = True
   workbook.Close(True)
   exceltodb()
   t1 = threading.Thread(target=google_indi)
   t1.start()
   t1.join()
   t1 = threading.Thread(target=google_indi)
   t1.start()
   t1.join()

   MB_TOPMOST=0x40000
   ctypes.windll.user32.MessageBoxW(0, "Data successfully Extracted from Audit file. please click Show Result button.", "Agile Automation", MB_TOPMOST)




# import win32com.client
# xl=win32com.client.Dispatch("Excel.Application")
# xl.Visible = True
# Path = "X:\\Coding\\Python\\Selenium\\Download.xlsm"
# xl.Workbooks.Open(Filename=Path)
# param1 = "https://github.com/coursera-dl/coursera-dl/issues/74"
# param2 = "X:\\Coding\\Python\\Selenium\\Text.html"
# xl.Application.Run("urldownload", param1, param2)


#filepathtemp = '\\\\fs12edx\\grpareas\\os\\Data\\NNS\\'
filepathtemp = 'X:\\Coding\\Python\\Selenium\\'
chromepath = 'X:\\Software\\Chrome\\'

def download_file_dll( url, filename ):
  #import ctypes
  myDLL = ctypes.WinDLL( "URLMon.DLL" )
  return( myDLL.URLDownloadToFileA( 0, url.encode( 'ascii', 'ignore' ), filename.encode( 'ascii', 'ignore' ), 0, 0 ))

def copydb():
    # global desktoppath
    # if os.path.exists(desktoppath + "GoogleSearch.txt"):
    #     pass
    # else:
    #     MB_TOPMOST=0x40000
    #     ctypes.windll.user32.MessageBoxW(0, "Google Search Keyword file has been created." + desktoppath + "GoogleSearch.txt", "Agile Automation", MB_TOPMOST)
    #     file = open(desktoppath + "GoogleSearch.txt", "w")
    #     file.close() 

        
    if os.path.exists(filepathtemp + getpass.getuser() + ".db"):
         os.remove(filepathtemp + getpass.getuser() + ".db")
         copyfile(filepathtemp + "Template.db", filepathtemp + getpass.getuser() + ".db")
    else:
        copyfile(filepathtemp + "Template.db", filepathtemp + getpass.getuser() + ".db")


def cleardb():
    global filepathtemp
    
    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    c = conn.cursor()
    c.execute('DELETE FROM Master')
    conn.commit()
    conn.close()
    # conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    # c = conn.cursor()
    # c.execute('DELETE FROM InputTable')
    # conn.commit()
    # conn.close()

def removefile():
    for item in os.listdir():
        #print("file name " + item)
        if item.startswith(getpass.getuser()) and item.endswith(".html"):
            os.system("cls")
            print("deleting file " + item)
            os.remove(item)


#https://selenium-python.readthedocs.io/locating-elements.html

temprc = 1
arrtemp = np.array(range(1000), dtype='a1000').reshape(250,4)

           
def chromeprint(strtemp,temppage, addkeyword):
    global temprc
    global arrtemp
    global filepathtemp
    options = webdriver.ChromeOptions()
    #options.add_argument("--disable-extensions")
    #options.add_argument('--disable-useAutomationExtension')
    options.add_experimental_option("useAutomationExtension",False)
    options.binary_location = "D:\\Users\\" + str(getpass.getuser()).lower() + "\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
    #options.binary_location = chromepath + "chrome.exe"

    #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
    
    chrome_driver_binary = chromepath + "chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
    driver.get("http://www.google.com")
    element = driver.find_element_by_name("q")
    element.send_keys(strtemp + addkeyword)
    element.submit()
    #date calculation
    #driver.get(driver.current_url + & "&tbs=cdr%3A1%2Ccd_min%3A" & Format(startdate, "MM") & "%2F" & Format(startdate, "DD") & "%2F" & Format(startdate, "YYYY") & "%2Ccd_max%3A" & Format(enddate, "MM") & "%2F" & Format(enddate, "DD") & "%2F" & Format(enddate, "YYYY"))
    

    conn = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')
    conn2 = sqlite3.connect(filepathtemp + str(getpass.getuser()).lower() + '.db')


    for pa in range(2,int(temppage) + 1):
        sys.stdout.write('\r')
        sys.stdout.write("Reading Page " + str(pa -1))
        #sys.stdout.write("[%-20s] %d%%" % ('='*pa-1, 5*pa-1))
        
        driver.save_screenshot("screenshot " + str(pa - 1) + ".png")
        #content = driver.find_elements_by_class_name('rc')
        #inner_text= driver.execute_script("return arguments[0].innerHTML;", x)
        inner_text = driver.page_source
        #print(inner_text)
        soup = BeautifulSoup(inner_text, 'html.parser')
        rctag = soup.find_all("div", {"class": "rc"})
        #print(rctag)
        for xtag in rctag:
            temph3 = xtag.find_all("h3")
            os.system("cls")
            print("Processing page " + str(pa -1) + " " + temph3[0].text)
            
            furl = xtag.find_all("a")
            tempftype2 = xtag.find_all("span", {"class": "sFZIhb b w xsm"})
            tempem = xtag.find_all("em")
            emstr = ""
            for emtag in tempem:
                emstr = emstr + emtag.text + " "
            #print(emstr)
            #print(furl[0]['href'])
            #print(temph3[0].text)
            tempftype = ''
            for tempftype3 in tempftype2:
                tempftype = tempftype3.text

            parsed_uri = urlparse(furl[0]['href'])
            domainurl = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

            c = conn.cursor()
            c2 = conn2.cursor()
            dburlfull = str(furl[0]['href']).replace('"', r'~').replace("'", r'')
            c2.execute('select * from Master where urlfull = "' + dburlfull  + '"')
            rows = c2.fetchall()
            tempval = ""
            if len(rows) == 0:
                download_file_dll(dburlfull,filepathtemp + str(getpass.getuser()).lower() + str("{:05d}".format(temprc)) + ".html" )

                dbID = str(str(getpass.getuser()).lower() + "{:05d}".format(temprc))
                dbsearchkey = str(strtemp + '+' + addkeyword)
                dbsheetnumber = str(pa -1)
                dboutertext = str(xtag.text).replace('"', r'').replace("'", r'').replace("'", r'').replace("\n\n", r'\n')
                dbouterhtml = str("").replace('"', r'').replace("'", r'').replace("'", r'')
                dblinkref = str("").replace('"', r'~').replace("'", r'').replace("'", r'')
                dburlfull = str(furl[0]['href']).replace('"', r'~').replace("'", r'')
                #dbfiletype = str(ws.Cells(rc ,7).Value).replace('"', r'~').replace("'", r'')
                dbfiletype = str(tempftype).replace('"', r'~').replace("'", r'')
                dbemkeyword = str(emstr).replace('"', r'~').replace("'", r'')
                dbDomainname =  str(domainurl).replace('"', r'~').replace("'", r'')
                dbcompanyname  = str(strtemp).replace('"', r'~').replace("'", r'')
                dblistselection  = str('').replace('"', r'~').replace("'", r'')
                dbStatus = 'YettoExtract'
                c.execute("INSERT into Master (ID, searchkey, sheetnumber, outertext, outerhtml, linkref, urlfull, filetype, emkeyword, Domainname, companyname, ListSelection, Status) VALUES ('" + dbID + "', '" +  dbsearchkey + "', '"  + dbsheetnumber +  "', '" +  dboutertext + "', '" +  dbouterhtml +  "', '" +  dblinkref +  "', '" +  dburlfull +  "', '" +  dbfiletype +  "', '" +  dbemkeyword +  "', '" +  dbDomainname +  "', '" +  dbcompanyname +  "', '" +  dblistselection + "', 'YettoExtract')")
                conn.commit()
                temprc = temprc + 1

            #print(frul['href'])


        elems = driver.find_elements_by_xpath("//a[@href]")
        for elem in elems:
            if(elem.text == str(pa)):
                #print(elem.text)
                elem.click()
                break
        sys.stdout.flush()

        # for x in content:
        #     inner_text= driver.execute_script("return arguments[0].innerHTML;", x)
            

        #     try:
        #         urlsp = inner_text.split('<h3')
        #         urlsp2 = urlsp[1].split('</h3>')
        #         urlsp3 = urlsp2[0].split('<a href=')
        #         urlsp4 = urlsp3[1].split('"')
        #         arrtemp[temprc,0] = urlsp4[1]
        #     except:
        #         print("Unable to extract href")
        #     #print(urlsp4[1])
            
        #     arrtemp[temprc,1] = strtemp
        #     arrtemp[temprc,2] = temprc
        #     arrtemp[temprc,3] = "Yet to Start"
        #     temprc = temprc + 1

        # aele = driver.find_elements_by_tag_name("a")
        # aeflag = False
        # for ae in aele:
        #     if aeflag == False:
        #         if ae.text == str(pa):
        #             ae.click()
        #             time.sleep(3)
        #             aeflag = True
                
            #print(urlsp4[0])
    #print(content)
    #inner_text= driver.execute_script("return arguments[0].innerText;", content)
    #print(inner_text)
    conn.close()
    conn2.close()
    driver.close()
    driver.quit()



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
            #print(iflag)
            if iflag != 0:
                rows1 = rows[0]
                #print(rows1)
                tempurl = rows1[6]
                #print(rows1[0])
                c.execute('update Master set Status = "Extracted" where ID = "' + str(rows1[0]) + '"')
                #print("after update query")
                conn.commit()
                conn.close()
                url = tempurl
                #IE started

                #print(url)
                #print("Reading file")
                os.system("cls")
                print("AI is Reading " + str(rows1[2]) + " page and link is " + str(rows1[6]))
                file = open(filepathtemp + rows1[0] + ".html", encoding="utf8")
                contemp = file.read()
                file.close()
                soup = BeautifulSoup(contemp, 'html.parser')
                #soup = BeautifulSoup(f)

                #tagsearch = ['p', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'table']
                tagsearch = ['p', 'h1']
                tags = soup.find_all(tagsearch)
                xc = 0
                sid = SentimentIntensityAnalyzer()
                strsen =""
                AIscore = 0


                tagreplacest = '<b style="color: green; background-color: #ffff42">'
                tagreplaceed = '</b>'
                #print("Entering for loop")
                for x in tags:
                    strsentag =""
                    tempstrsoupt = soup.find_all(tagsearch)[xc].string
                    if tempstrsoupt is not None:

                        #print("tagstring === " + str(xc) + soup.find_all(tagsearch)[xc].string)
                        lines_list = tokenize.sent_tokenize(tempstrsoupt)
                    #sentences.extend(strbody3)
                        for sentence in lines_list:
                            #print(sentence)
                            ss = sid.polarity_scores(sentence)
                            if ss['neg'] > 0:
                                AIscore = AIscore + int(ss['neg']*10)
                                strsen = strsen + "AI Score = " + str(ss['neg'] * 10) + " ==> " + sentence + '\n'
                                strsentag = strsentag + tagreplacest + sentence + '(AI Score = ' + str(ss['neg'] * 10) + ')' + tagreplaceed 

                                #print("AI Score = " + str(ss['neg']) + " ==> " + sentence)
                            else:
                                strsentag = strsentag + sentence
                    
                        soup.find_all(tagsearch)[xc].string = strsentag
                    xc = xc+1


                tempstr = soup
                tempstr = str(tempstr).replace('"', r'~')
                tempstr = str(tempstr).replace("'", r"~")
                tempstr = str(tempstr).replace("&lt;", r"<")
                tempstr = str(tempstr).replace("&gt;", r">")
                #tempstr = re.sub('[^A-Za-z0-9]<>~!@#$%^&*(){}+', '', str(tempstr))

                
                strsen = str(strsen).replace('"', r'~')
                strsen = str(strsen).replace("'", r"~")
                #strsen = re.sub('[^A-Za-z0-9]<>~!@#$%^&*(){}+', '', str(strsen))

                #tempstr = str(tempstr).replace('\n\n', r'\n')
                #tempstr = str(tempstr).replace('\r\n\r\n', r'\r\n')
                conn = sqlite3.connect(str(filepathtemp + getpass.getuser()).lower() + '.db')
                c = conn.cursor()
                #print("rawtext to db")
                c.execute("update Master set rawtext = '" + str("") + "', rawtexttag = '" + str(tempstr) + "', negtext = '" + str(strsen) + "', AIScore = '" + str(AIscore) + "' where ID = '" + str(rows1[0]) + "'")
                conn.commit()
                conn.close()

            else:
                conn.close()
                #ie.Quit()

                return
        except:
            print("Unable to read the file")
            conn.close()


if __name__ == '__main__':
    copydb()
    #otherwebsites()
    #clearfiles()
    #MainFun("cisco<:>1<:>SearchKeyWordList1<:>DomainName:cisco<:>AISearch:true<,>")
    socketio.run(app, debug=False)





# t1 = threading.Thread(target=chromeloop, args=("tcs + fraud",))
# t2 = threading.Thread(target=chromeloop, args=("Infosys + fraud",))


# t1.start()
# t2.start()

# t1.join()
# t2.join()




# def chromeloop(strtemp):
#     global temprc
#     global arrtemp
#     options = webdriver.ChromeOptions()
#     #options.add_argument("--disable-extensions")
#     #options.add_argument('--disable-useAutomationExtension')
#     options.add_experimental_option("useAutomationExtension",False)
#     options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
#     #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
    
#     chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
#     driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
#     driver.get("http://www.google.com")
#     element = driver.find_element_by_name("q")
#     element.send_keys(strtemp)
#     element.submit()
    

#     for pa in range(2,4):
#         content = driver.find_elements_by_class_name('rc')
#         for x in content:
#             inner_text= driver.execute_script("return arguments[0].innerHTML;", x)
#             try:
#                 urlsp = inner_text.split('<h3')
#                 urlsp2 = urlsp[1].split('</h3>')
#                 urlsp3 = urlsp2[0].split('<a href=')
#                 urlsp4 = urlsp3[1].split('"')
#                 arrtemp[temprc,0] = urlsp4[1]
#             except:
#                 print("Unable to extract href")
#             #print(urlsp4[1])
            
#             arrtemp[temprc,1] = strtemp
#             arrtemp[temprc,2] = temprc
#             arrtemp[temprc,3] = "Yet to Start"
#             temprc = temprc + 1

#         aele = driver.find_elements_by_tag_name("a")
#         aeflag = False
#         for ae in aele:
#             if aeflag == False:
#                 if ae.text == str(pa):
#                     ae.click()
#                     time.sleep(3)
#                     aeflag = True
                
#             #print(urlsp4[0])
#     #print(content)
#     #inner_text= driver.execute_script("return arguments[0].innerText;", content)
#     #print(inner_text)
#     driver.close()
#     driver.quit()


# # t1 = threading.Thread(target=chromeloop, args=("tcs + fraud",))
# # t2 = threading.Thread(target=chromeloop, args=("Infosys + fraud",))


# # t1.start()
# # t2.start()

# # t1.join()
# # t2.join()



# def chromeremaing():
#     global temprc
#     global arrtemp
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option("useAutomationExtension",False)
#     options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
#     chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
#     driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
#     procs = psutil.Process(driver.service.process.pid).children(recursive=True)
#     for x in range(temprc):
#         if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
#             arrtemp[x,3] = 'started'.encode('ascii')
            
#             try:
                
#                 driver.implicitly_wait(10)
#                 time.sleep(3)
#                 driver.get(arrtemp[x,0].decode('ascii'))
#                 driver.implicitly_wait(10)
#                 time.sleep(3)
#                 content = driver.find_elements_by_tag_name("html")
#                 driver.implicitly_wait(10)
#                 f = open("Doutput" + str(arrtemp[x,2].decode('ascii')).zfill(4) + ".txt", "w",encoding="utf-8")
#                 for e in content:
#                     f.write(e.text)
#                 f.close()
#                 arrtemp[x,3] = 'Completed'.encode('ascii')
#             except:
#                 print("Error occured on", x, arrtemp[x,3].decode('ascii'), arrtemp[x,0])
                
#                 time.sleep(3)
#                 for p in procs:
#                     p.terminate()
#                     gone, alive = psutil.wait_procs(procs, timeout=3)
#                 for p in alive:
#                     p.kill()
   
#     driver.close()
#     driver.quit()



# def chromeextract():
#     global temprc
#     global arrtemp
#     options = webdriver.ChromeOptions()
#     #options.add_argument("--disable-extensions")
#     #options.add_argument('--disable-useAutomationExtension')
#     options.add_experimental_option("useAutomationExtension",False)
#     options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
#     #capabilities = {'browserName': 'chrome','chromeOptions':  { 'useAutomationExtension': False, 'forceDevToolsScreenshot': True, 'args': ['--start-maximized', '--disable-infobars'] }}
    
#     chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
#     driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
#     procs = psutil.Process(driver.service.process.pid).children(recursive=True)
#     print(procs)

#     for x in range(temprc):
#         #print(x, arrtemp[x,3].decode('ascii'), arrtemp[x,3])
#         if arrtemp[x,3].decode('ascii') == 'Yet to Start':
#             arrtemp[x,3] = 'started'.encode('ascii')
            
#             try:
                
#                 driver.implicitly_wait(20)
#                 time.sleep(3)
#                 driver.get(arrtemp[x,0].decode('ascii'))
#                 driver.implicitly_wait(10)
#                 time.sleep(3)
#                 content = driver.find_elements_by_tag_name("html")
#                 driver.implicitly_wait(20)
#                 f = open("Doutput" + str(arrtemp[x,2].decode('ascii')).zfill(4) + ".txt", "w",encoding="utf-8")
#                 for e in content:
#                     f.write(e.text)
#                 f.close()
#                 arrtemp[x,3] = 'Completed'.encode('ascii')
#             except:
#                 print("Error occured on", x, arrtemp[x,3].decode('ascii'), arrtemp[x,0])
#                 time.sleep(20)
#                 try:
#                     for p in procs:
#                         p.terminate()
#                         gone, alive = psutil.wait_procs(procs, timeout=3)
#                     for p in alive:
#                         p.kill()
#                 except:
#                     print("error on killing")
# ##                options = webdriver.ChromeOptions()
# ##                options.add_experimental_option("useAutomationExtension",False)
# ##                options.binary_location = "D:\\Users\\selvgnb\\AppData\\Local\\Microsoft\\AppV\\Client\\Integration\\6F327610-34BD-42B9-8795-5D70F9F4F77D\\Root\\VFS\\ProgramFilesX86\\Google\\Chrome\\Application\\chrome.exe"
# ##                chrome_driver_binary = "X:\\Coding\\Python\\Selenium\\chromedriver.exe"
# ##                driver = webdriver.Chrome(chrome_driver_binary, chrome_options=options)
# ##                time.sleep(100)
#                 #return
#     driver.close()
#     driver.quit()


# # t1 = threading.Thread(target=chromeextract)  
# # t2 = threading.Thread(target=chromeextract)
# # t3 = threading.Thread(target=chromeextract)
# # t4 = threading.Thread(target=chromeextract)
# # t5 = threading.Thread(target=chromeextract)

# # t1.start()
# # t2.start()
# # t3.start()
# # t4.start()
# # t5.start()

# # t1.join()
# # t2.join()
# # t3.join()
# # t4.join()
# # t5.join()




# # for x in range(temprc):
# #     if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
# #         t1 = threading.Thread(target=chromeextract)  
# #         t2 = threading.Thread(target=chromeextract)
# #         t3 = threading.Thread(target=chromeextract)
# #         t4 = threading.Thread(target=chromeextract)
# #         t5 = threading.Thread(target=chromeextract)

# #         t1.start()
# #         t2.start()
# #         t3.start()
# #         t4.start()
# #         t5.start()

# #         t1.join()
# #         t2.join()
# #         t3.join()
# #         t4.join()
# #         t5.join()
        
# #         t1.exit()
# #         t2.exit()
# #         t3.exit()
# #         t4.exit()
# #         t5.exit()

# #         break


# # print("second loop exe")
# # for x in range(temprc):
# #     if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
# #         chromeremaing()
        
# # print("second indi ")
# # for x in range(temprc):
# #     if arrtemp[x,3].decode('ascii') == 'Yet to Start' or arrtemp[x,3].decode('ascii') == 'started':
# #         chromeremaing()


# # print(arrtemp)
# ##t2 = threading.Thread(target=chromeloop, args=("caleb",))
# ##t3 = threading.Thread(target=chromeloop, args=("caleb",))
# ##t4 = threading.Thread(target=chromeloop, args=("caleb",))
# ##t5 = threading.Thread(target=chromeloop, args=("caleb",))

# ##driver2.get("http://www.google.com");
# ##element = driver2.find_element_by_name("q")
# ##element.send_keys("pycon")
# ##element.submit();
# ##
# ##driver3.get("http://www.google.com");
# ##element = driver3.find_element_by_name("q")
# ##element.send_keys("pycon")
# ##element.submit();


# ##t2.start()
# ##t3.start()
# ##t4.start()
# ##t5.start()



# ##t2.join()
# ##t3.join()
# ##t4.join()
# ##t5.join()


# ##element = driver.find_element_by_css_selector('rc')
# ##inner_text= driver.execute_script("return arguments[0].innerText;", element)


