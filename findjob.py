import sys
import requests
import re
import os.path
import time
from datetime import date


bad_url = [        
"www.googletagservices.com\n",
"www.google.com\n",
"www.googletagmanager.com\n",
"www.linkedin.com\n",
"www.facebook.com\n",
"www.kijiji.it\n",
"www.romaforever.com\n",
]



def beforechecking(stringa):
    if stringa in bad_url:
        return False
    return True


def trytowrite(filename,stringa):
    if beforechecking(stringa):
        if os.path.isfile(filename): 
            file = open( filename, 'r') 
            lines = file.readlines()
            file.close()
        else:
            lines = []
        notfound = True
        for line in lines:
            if line == stringa:
                notfound= False
                break
            if not line:
                break
        if notfound:
            file = open(filename, 'a+')
            file.write(stringa)
            file.close()
            return 1
    return 0

try:
    sys.argv[1]
except NameError:
    print "Devi immettere un lavoro"
else:
    debug_file = open("debug.txt","a+") 
    filename = str(date.today())+sys.argv[1]
    print "Daje di JobRapido"
    counter = 0
    url = 'http://it.jobrapido.com/?w='+sys.argv[1]+'&l=italia&r=auto'
    page = requests.get(url)
    web_pages = re.findall('www\.[a-zA-Z0-9.]*\.[a-zA-Z0-9.]*', page.content, re.IGNORECASE) 
    if web_pages:
        print "Trovati "+str(len(web_pages))+" siti web"
        for web_page in web_pages:
            counter += trytowrite(filename,web_page+"\n")
    print "Salvati "+str(counter)
    
    
    counter = 0
    print "Esamino URL"
    links = re.findall('href="(http://it.jobrapido.com.*)"', page.content, re.IGNORECASE)
    if links:
        for link in links:
            print link
            page = requests.get(link)
            names = re.findall('searchResults::(.*),', page.content, re.IGNORECASE)
            if names:
                print names
            
    print "Daje di Subito"
    counter = 0
    url = 'http://www.subito.it/annunci-italia/vendita/offerte-lavoro/?q='+sys.argv[1]
    print url

    
    
    
    
    