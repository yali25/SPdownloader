#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from subprocess import call
import os 
import codecs

# pdftext for converting the pdf to text 
# decrypt text with python
# generate pdf with chrome 

def wrongpdf(furl,heading1,heading2,date) :
    with codecs.open("wrong.txt","a","utf-8") as wrongf:
       wrongf.write(u'{:s} {:s} {:s} {:s}\n'.format(furl,heading1,heading2,date))

def badPDF(filep):
    pdfsize = os.stat(filep).st_size / 1024
    if pdfsize >= 210 or pdfsize <= 55:
       print("File was not generated correctly: %s\n" % filep)
       os.remove(filep) # remove the wrong pdf
       return True
    else:
       return False
        

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
#remote-debugging-port=9222'
driver = webdriver.Chrome(executable_path=os.path.abspath("./chromedriver"), chrome_options=chrome_options)  

#driver = webdriver.PhantomJS(executable_path='./phantomjs',service_args=['--load-images=no'])
#driver.implicitly_wait(80)
#driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')

#pageFormat = '''this.paperSize = {format: "A4", orientation: "portrait", margin: { top: "1cm", right: "1cm", left: "1cm", bottom: "2.5cm"} };'''
# 1 Xpaths of the SpiegelPlus Articles
print "1. Go to Spiegel+ to get article links"
starturl = "http://www.spiegel.de/spiegelplus"
#starturl = "http://www.spiegel.de/spiegelplus/archiv-2017070.html"

#HasArticles = True
while True:
   print("Goto page: %s"%starturl)
   driver.get(starturl)

   if "archiv" in starturl:
     c=1 
   else:
     c=0

   #nexturl      = driver.find_elements_by_id("content-main").find_element_by_link_text("Mehr Artikel").get_attribute("href")
   try:
      nexturl      = driver.find_element_by_link_text("Mehr Artikel").get_attribute("href")
   except:
      print("Reached the last page of the Archive, go back to start in the next iteration\n")  
      nexturl = "http://www.spiegel.de/spiegelplus"
      #break; 
      # HasArticles = False
   #except:
   # Try a different archive link
   #print("Try different XPATH for next page...")
   #archive       = '/html/body/div[4]/div[1]/div/div[2]/div/div[18]/a[2]' # oder 19 /html/body/div[4]/div[1]/div/div[2]/div/div[19]/a[2]
   #starturl      = driver.find_element_by_xpath(archive).get_attribute("href")
                                            
   #topArticle   = driver.find_elements_by_xpath('//*[@id="content-main"]/div/div/p/a')
   #articleLinks = driver.find_elements_by_xpath('//*[@id="content-main"]/div/div/div/p/a')
   # Erste Artikel auf Seite (Only obe top article) gibt es nicht auf den anderen Seiten
   if c==0:
      topArticle    = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/p/a')
      topH1         = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/h2/a/span[1]')
      topH2         = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/h2/a/span[2]')
      articleLinks  = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/p/a')
      headings1     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/h2/a/span[1]')
      headings2     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/h2/a/span[2]') 

      articleLinks = [topArticle] + articleLinks
      headings1    = [topH1] + headings1
      headings2    = [topH2] + headings2
      datetime     = ["DummyDate, DummyTime"]  + ["DummyDate, DummyTime"] * len(articleLinks)
   else:
      articleLinks  = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/p/a')
      tempDate      = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/div[@class="source-date"]')
      datetime = []
      # Convert to string
      for e in tempDate:
        datetime.append(e.text)
      headings1     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/h2/a/span[1]')                               
      headings2     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/h2/a/span[2]') 

   finalUrlList = []
   print "Create List %s %s %s %s" % (len(articleLinks),len(headings1),len(headings2),len(datetime))
   for link,h1,h2, d in zip(articleLinks,headings1,headings2,datetime):
     #print h1.text
     #print h2.text 
     url = link.get_attribute("href")
     if url.find("laterpay") == -1:
       print((u"Process: {} ({})".format(h1.text,h2.text)))
       printUrl = url  
       ggTranslateUrl = "https://translate.google.co.jp/translate?hl=ja&sl=ko&tl=en&u="+printUrl+"&anno=2"
       #print ggTranslateUrl
       finalUrlList.append((ggTranslateUrl,h1.text,h2.text,d.split(",",1)[0]))
   
   #for e in finalUrlList:
   #  print("%s %s %s"%(e[0],e[1],e[2]))
   
   print "Found %s Spiegel+ articles" % len(articleLinks)

   dirp = "./SP"
   print "Create PDFs"
   success = 0
   for url in finalUrlList:
    furl     = url[0]
    heading1 = url[1]
    heading2 = url[2]

    filename = u"{}: ({}).pdf".format(heading1.replace("/","_").replace(":",""),heading2.replace("/","_"))
    filepnd = dirp + "/" + "NoDate" + "/" + filename
    noDateDir = os.path.exists(filepnd)

    if  noDateDir == True:
        if badPDF(filepnd) == True:
           pass
        else:
           print("Already exist: %s" % filepnd)
           success = success + 1
           continue

    if c != 0:
      date     = url[3]
      # Check if pdf already exist
      #filename = u"{} ({}).pdf".format(heading1.replace("/","_"),heading2.replace("/","_"))
      #print(u"Try to get: %s" % filename)
      filep = dirp + "/" + date.replace(".","_") + "/" + filename
     
      #filep = dirpf 
      # Check if the pdf does not exist
      dateDir   = os.path.exists(filep)
      if  dateDir == True:
        if badPDF(filep):
           pass
        else:
           print("Already exist: %s" % filep)
           success = success + 1
           continue

    driver.get(furl)
    driver.switch_to.frame(driver.find_element_by_name("c")) #print "Switches to iframe"

    # Check for the print link
    NoDrucken = False
    try:
       #link = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]/span/a')
       link = driver.find_element_by_link_text("Drucken")
       # Date must be obtained if we are on the first page because there it is only contained inside the article         
    except:
       NoDrucken = True
       #print "Will add data to the next queue"
    
    # Check for the date     
    try:
       if c==0:
          date = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div[5]/div/div[2]/time/span/span[2]/b').text    
    except:
       date = "NoDate"

    # Construct the path    
    dirpf = dirp + "/" + date.replace(".","_")
    filep = dirpf + "/" + filename
   
    # Check if the pdf already exist
    if os.path.exists(filep):
      print("In here Already exist: %s" % filep)
      success = success + 1
      continue



  
    # Check if the pdf does not exist
    if NoDrucken == False and not os.path.exists(filep):
      #print("Not exist: %s" % filep)
      # Create dir
      if not os.path.exists(dirpf):
        os.makedirs(dirpf)

      pdfLink =  link.get_attribute("href")
      call(["google-chrome","--headless","--disable-gpu",u"--print-to-pdf="+filep, pdfLink])

      # Check filesize to check if the pdf was correct generated
      if badPDF(filep) == True:
         wrongpdf(furl,heading1,heading2,"FileSize")
      else:
        success = success + 1

    elif os.path.exists(filep):
      print("Never here Already exist: %s" % filep)
      success = success + 1
    elif NoDrucken == True and not os.path.exists(filep):
      print "Could not locate element DRUCKEN: %s %s " % (date, furl)
      wrongpdf(furl,heading1,heading2,"NoDrucken")

   logstr = "%s %s %s\n"
   with open("download_log.txt","a") as log:
       if success != len(finalUrlList):
          logstr = "------->"+logstr
       log.write(logstr %(success,len(finalUrlList),starturl))

   # set the next page
   starturl = nexturl
   c = c + 1
driver.quit()
