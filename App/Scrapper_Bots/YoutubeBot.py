import sys, unittest, time, datetime
import urllib.request, urllib.error, urllib.parse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidArgumentException
from bs4 import BeautifulSoup



def Youtube_bot(urls):
    Youtube_Url = 'https://www.youtube.com/channel/{}'
    url = Youtube_Url.format(urls)
    channelid = urls
    #driver=webdriver.Firefox()
    file_path = 'App/Scrapper_Bots/chromedriver.exe'
    driver=webdriver.Chrome(file_path)
    driver.get(url)
    time.sleep(5)
    dt=datetime.datetime.now().strftime("%Y%m%d%H%M")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    lastheight = 0
    while True:
        if lastheight == height:
            break
        lastheight = height
        driver.execute_script("window.scrollTo(0, " + str(height) + ");")
        time.sleep(2)
        height = driver.execute_script("return document.documentElement.scrollHeight")
    
    Videos_Links = driver.find_elements_by_xpath('//*[@id="video-title"]')
    Subscribers = driver.find_elements_by_id("subscriber-count")
    
    Subs = []
    for x in Subscribers:
        Subs.append(x)
        print(x.text)
        
    Link = []
    if Videos_Links is not None:
        for i in range(len(Videos_Links)):
            print(Videos_Links[i].get_attribute('href'))
            link = (Videos_Links[i].get_attribute('href'))
            f = open(channelid+'-'+dt+'.list', 'a+')
            if link is not None:
                Link.append(link)
            else:
                break
            f.close
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content, 'lxml')
        views = soup.findAll('span', class_='style-scope ytd-grid-video-renderer')
        views_List = []
        for j in views:
            Text = str(j.text)
            views_List.append(Text)
    
        views_videos = []
        for text_val in views_List:
            Is_Contains_Views = text_val.find("views",0,len(text_val))
            if Is_Contains_Views> -1:
                views_videos.append(text_val)


    Dict = {}
    Dict["Sub"] = Subs[0].text
    Dict["Links"] = Link
    Dict["#of_Post"] = len(Link)
    Dict["Views"] = views_videos


    return Dict

