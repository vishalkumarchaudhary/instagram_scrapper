# it is same as whatever written in main.ipnyb

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import shutil
import requests
import sys
import time
import os
from lxml import etree, html
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
try:
    os.stat("images")
except:
    os.mkdir("images") 
try:
    os.stat("comments")
except:
    os.mkdir("comments") 

def load_more_comment():
    tmp = driver.find_elements_by_tag_name("a")
    for i in (tmp):
        if "Load more comments" in str(i.get_attribute("innerHTML"))   :
            i.click()
#             return

def save_comments():
    comm = (driver.find_elements_by_tag_name( "li"))
    # images= (driver.find_elements_by_tag_name("img"))
    # print(comm.get_attribute("innerHTML"))
    comments = " "
    flag = 0 
    for i in comm :

        document_root = html.fromstring(i.get_attribute('innerHTML'))
    #     document_root = html.fromstring(i.get_attribute('outerHTML'))
        x = (etree.tostring(document_root, encoding='unicode', pretty_print=True))
        try :
            if(flag):
                comments += str(x).split("<span>")[3].split("</")[0]+" "
                
        except :
            pass
        if (not flag and "Load more comments" in str(x)):
            flag = 1
    return comments

def save_image(image_comment_link,image_name):
    link = "https://www.instagram.com"+image_comment_link
    driver.get(link)
    images= (driver.find_elements_by_tag_name("img"))
    counter = image_name
    for i in (images[1:]):

    #     document_root = html.fromstring(i.get_attribute('innerHTML'))
        document_root = html.fromstring(i.get_attribute('outerHTML'))
        x = (etree.tostring(document_root, encoding='unicode', pretty_print=True))
    #     print(x)
        image_link = str(document_root.get("src")) 

        ##stroring images into file
        with open(str(counter), 'wb') as handle:
            response = requests.get(image_link, stream=True)

            if not response.ok:
                print( response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
    
    
driver = webdriver.Firefox()
number_of_scrolls = 5 ## directly proportional to number of phpto of a celebreties
image_id_counter = 1
comment_id  =1
num_load_more_comment = 2

with open("celeb.csv",'r') as cf :
    for line in cf.readlines():
        
        celeb = str(line)[0:-1]
        print(celeb)

   
        driver.get("https://www.instagram.com/"+ celeb +"/")
        
        for i in range(number_of_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        listss= driver.find_elements_by_tag_name("a")
        image_comment_link = []
        for i in (listss[2:]):

        #     document_root = html.fromstring(i.get_attribute('innerHTML'))
            document_root = html.fromstring(i.get_attribute('outerHTML'))
#             x = (etree.tostring(document_root, encoding='unicode', pretty_print=True))
         
            image_link = document_root.get("href")
            if(len(image_link)>2 and image_link[1]=='p'):
                image_comment_link.append( image_link)
                continue
            else :
                pass
        
        
        
       
        
        comment_file = open("comments/"+str(celeb)+".csv","w")
        for k in image_comment_link :
            try :
                save_image(k,"images/"+str(celeb)+"/"+str(image_id_counter)+".jpg")
                print(image_id_counter , comment_id)
                print(k)
                for _tmp in range(num_load_more_comment):
                    try :
                        load_more_comment()  

                    except:
                        pass
                comment = save_comments()
                print(comment)
        
                comment_file.write(str(comment_id)+" , " + comment +"\n" )
        
                comment_id +=1
                image_id_counter = comment_id 
#                 image_id_counter +=1
            except :
                pass
        comment_file.close()
        ## number of load more comments
           
            
            
