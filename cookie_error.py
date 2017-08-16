#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from subprocess import call
import os 

# driver = webdriver.PhantomJS(executable_path='./phantomjs',service_args=['--cookies-file=./cookies.txt','--debug=yes'])
def execute(script, args):
    driver.execute('executePhantomScript', {'script': script, 'args' : args })

def wrongpdf(url):
    with open("wrong.txt","a") as wrongf:
       wrongf.write(url+"\n")

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")  
#chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'

driver = webdriver.Chrome(executable_path=os.path.abspath("./chromedriver"), chrome_options=chrome_options)  

#driver = webdriver.PhantomJS(executable_path='./phantomjs')
#driver.command_executor._commands['executePhantomScript'] = ('POST', '/session/$sessionId/phantom/execute')

#pageFormat = '''this.paperSize = {format: "A4", orientation: "portrait", margin: { top: "1cm", right: "1cm", left: "1cm", bottom: "2.5cm"} };'''
# 1 Xpaths of the SpiegelPlus Articles
print "1. Go to Spiegel+ to get article links"
#starturl = "http://www.spiegel.de/spiegelplus"
starturl = "http://www.spiegel.de/spiegelplus/archiv-2017058.html"
#archive = "/html/body/div[4]/div[1]/div/div[2]/div[4]/div[2]/a"
c=0
while True:
   print("Goto page: %s"%starturl)
   driver.get(starturl)
   # TODO set the url for the next run
   #try:
   starturl      = driver.find_element_by_link_text("Mehr Artikel").get_attribute("href")
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
   
      
   # Die andereren Artikel und die Ueberschriften
   if c==0:
      articleLinks  = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/p/a')
      headings1     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/h2/a/span[1]')
      headings2     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[3]/div/div/h2/a/span[2]') 
   else:
      articleLinks  = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/p/a')
      headings1     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/h2/a/span[1]')                               
      headings2     = driver.find_elements_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div/div/h2/a/span[2]') 

   # Create a single list (only on the first page)
   if c==0:              
      articleLinks = [topArticle] + articleLinks
      headings1    = [topH1] + headings1
      headings2    = [topH2] + headings2
   
   finalUrlList = []
   print "Create List %s %s %s " % (len(articleLinks),len(headings1),len(headings2))
   for link,h1,h2 in zip(articleLinks,headings1,headings2):
     #print h1.text
     #print h2.text 
     url = link.get_attribute("href")
     if url.find("laterpay") == -1:
       print((u"Process: {} ({})".format(h1.text,h2.text)))
       printUrl = url  
       ggTranslateUrl = "https://translate.google.co.jp/translate?hl=ja&sl=ko&tl=en&u="+printUrl+"&anno=2"
       #print ggTranslateUrl
       finalUrlList.append((ggTranslateUrl,h1.text,h2.text))
   
   #for e in finalUrlList:
   #  print("%s %s %s"%(e[0],e[1],e[2]))
   
   print "Found %s Spiegel+ articles" % len(articleLinks)
   
   c=0
   #driver.implicitly_wait(30)
   dirp = "./SP"
   print "Create PDFs"
   for url in finalUrlList:
    furl = url[0]
    heading1 = url[1]
    heading2 = url[2]
    #print furl
    #print heading1
    #print heading2
    driver.get(furl)
    driver.switch_to.frame(driver.find_element_by_name("c"))
    #print "Switches to iframe"
    link = ""
    data = ""
    try:
       #link = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]/span/a')
       link = driver.find_element_by_link_text("Drucken")
       date = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[1]/div[5]/div/div[2]/time/span/span[2]/b').text                                  
    except:
       wrongpdf(furl)
       #print "Could not locate element: %s " % furl
       #print "Will add data to the next queue"
       continue
   
    pdfLink =  link.get_attribute("href")
    filename = u"{} ({}).pdf".format(heading1,heading2)
    #print(u"{}".format(filename))
    dirpf = dirp + "/" + date.replace(".","_")
    filep = dirpf + "/" + filename
    # Check if the pdf does not exist
    if not os.path.exists(filep):
      print("Not exist: %s" % filep)
      # Create dir
      if not os.path.exists(dirpf):
        os.makedirs(dirpf)
      call(["google-chrome","--headless","--disable-gpu",u"--print-to-pdf="+filep, pdfLink])
      pdfsize = os.stat(filep).st_size / 1024
      if pdfsize >= 210 or pdfsize <= 55:
        wrongpdf(furl) 
        os.remove(filep) # remove the wrong pdf
    else:
      print("Exist: %s" % filep)
      #print(u"PDF was not generated correclty: %s" % filep)
   c = c + 1
   #print pdfLink 
   #driver.get(pdfLink)
   #link.click()
   #driver.switch_to_window(driver.window_handles[1])
   #print furl
   #driver.get(furl)
   #execute(pageFormat, [])
   #render = 'this.render("%s.pdf")' % c
   #execute(render, [])
   #call(["google-chrome","--headless","--disable-gpu","--print-to-pdf="+str(c)+".pdf",furl])
   #c = c+1
   #link = driver.find_element_by_xpath('/html/body/div[4]/div[1]/div/div[2]/div[2]/div[2]/div[1]/ul/li[1]/span/a')
   #driver.switch_to_frame(driver.find_element_by_xpath('//*[@id="contentframe"]/iframe'))
   #print "Switched to iframe"
   #driver.switch_to.default_content()
   #print driver.page_source
   #link = driver.find_element_by_link_text("Drucken")
   # # set page format
   # # inside the execution script, webpage is "this"
   # pageFormat = '''this.paperSize = {format: "A4", orientation: "portrait", margin: { top: "1cm", right: "1cm", left: "1cm", bottom: "1cm"} };'''
   # execute(pageFormat, [])
   # # render current page
   # render = '''this.render("test.pdf")'''
   # execute(render, [])
driver.quit()
