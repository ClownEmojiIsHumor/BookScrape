"""WzXX7d3HJpVD91kW1fmWBOP_SkGDsA
WzXX7d3HJpVD91kW1fmWBOP_SkGDsA
WzXX7d3HJpVD91kW1fmWBOP_SkGDsA"""

import tkinter
import os
from ast import main
from typing import Counter
import nltk 
import praw
from nltk.stem import WordNetLemmatizer
from googlesearch import search
from PIL import Image
#nltk.download("stopwords")
#nltk.download('punkt')
#nltk.download('wordnet')
#nltk.download('omw-1.4')
#nltk.download('averaged_perceptron_tagger')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from google_images_download import google_images_download 

from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from colorthief import ColorThief


def bookBot(bookvar):
    reddit = praw.Reddit(
        client_id="FwM74aWJgLHngSHkg6X0Og",
        client_secret="WzXX7d3HJpVD91kW1fmWBOP_SkGDsA",
        user_agent="Book Emotion bot",
    )

    subreddit=reddit.subreddit("books")

    commentList=[]
    stop_words = set(stopwords.words("english")).union(["lot", "important", "http","huge", "[", "]",  "\\-", "'", "series", "part", "'s", ".", ",", ":", "'m", "n't", "Wo", "''", "?", "``", "*", "book", "story", "first", "last", "good", "bad", "wrong", "right", "second", 
    "third", "many", "few", "favorite", "favourite", "'", "much", "less", "little", "main", "’", "“", "great", "best", "entire", "interesting", "amazing", "worst", "strong", "unlikely", "unlikely", '"', "big", "wonderful", "awful", "character"])
    #print(stop_words)


    bookName= bookvar
    adjectiveList=[]
    nounList=[]
    nounProperList=[]
    lemmatizer=WordNetLemmatizer()
    for submission in subreddit.search(bookName,sort='relevance',limit=15):
        print("Title: ", submission.title)
        #print("Text: ", submission.selftext)
        print("Score: ", submission.score)
        mainList= word_tokenize(submission.selftext)
        filteredList=nltk.pos_tag(mainList)
        filteredList=[ word for word in filteredList if word[0].casefold() not in stop_words]

        for wordi in filteredList:
            word= (lemmatizer.lemmatize(wordi[0]), wordi[1])
            if word[1]=="JJ" or word[1]=="JJR" or word[1]=="JJS":
                adjectiveList.append(word)
            elif word[1]=='NN'or word[1]=="NNPS":
                nounList.append(word)
            elif word[1]=="NNP":
                nounProperList.append(word)

        # adjectiveList=[adjective for adjective in filteredList if  adjective[1]=="JJ" or adjective[1]=="JJR" or adjective[1]=="JJS"]
        # nounList=[noun for noun in filteredList if noun[1]=='NN'or noun[1]=="NNPS" or  noun[1]=="NNP" ]
        #filteredList=[ word for word in mainList if word.casefold() not in stop_words]

        #print("Adjectives:", adjectiveList)
        #print("Nouns", nounList)
        #print("\n \n\n\n\n\n\n\n\n\n\n\n\n", ("Paul", "NNP") in nounList)
        #print("Token: ", filteredList)
        #print("Token1 :", mainList)
        # comTree=submission.comments
        # for topComments in range(0, 3):
        #     print("Comment: ", comTree[topComments].body)
        print("---------------------------------\n")

    adjectiveDict=Counter(adjectiveList)
    nounListDict=Counter(nounList)
    nounProperDict=Counter(nounProperList)
    print(adjectiveDict)
    print(nounListDict)
    print("\n\n\n\n\n\n")
    print(nounProperDict)

    #query= nounProperDict.most_common(10)[0][0][0]+nounProperDict.most_common(10)[1][0][0]+nounProperDict.most_common(10)[2][0][0]+"Dune"+nounListDict.most_common(5)[0][0][0]+adjectiveDict.most_common(5)[0][0][0]

    query=""
    queryList=[]
    for nouns in range(0, 7):
        query=query+" "+nounProperDict.most_common(15)[nouns][0][0]
        queryList.append(nounProperDict.most_common(15)[nouns][0][0])

    query=query+" "+bookName 
    query=query+ " " +nounListDict.most_common(15)[0][0][0]+ " " +adjectiveDict.most_common(15)[0][0][0]
    queryList.append(nounListDict.most_common(15)[0][0][0])
    queryList.append(nounListDict.most_common(15)[1][0][0])
    queryList.append(adjectiveDict.most_common(15)[0][0][0])
    queryList.append(adjectiveDict.most_common(15)[1][0][0])
    print(query)
        

    options=webdriver.ChromeOptions()
    options.headless=True
    #options.add_argument("--headless")
    #driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    colourList= []
    for t in range(len(queryList)):
        driver.get('https://images.google.com/')

        box = driver.find_element(By.CLASS_NAME, 'gLFyf.gsfi')
        box.send_keys(queryList[t]+" "+bookName)
        box.send_keys(Keys.ENTER)
        time.sleep(1)

        for i in range(1, 5):
            try:
                original_window = driver.current_window_handle
                time.sleep(1)
                image=driver.find_element(By.XPATH, '//*[@id="islrg"]/div[1]/div['+str(i)+']/a[1]/div[1]/img')
                #print("found image")
                source_link=image.get_attribute('src')
                driver.switch_to.new_window('tab')
                driver.get(source_link)
                image=driver.find_element(By.TAG_NAME, "img")
                image.screenshot('cache\img'+str(i)+str(t)+'.png')
                driver.close()
                driver.switch_to.window(original_window)
                #image.screenshot('cache\img'+str(i)+str(t)+'.png')
                
            except:
                pass





def processImages():
    images = [Image.open('cache\\'+x) for x in os.listdir('cache\\')]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new('RGB', (total_width, max_height), color=(251, 251, 251))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

    new_im.save('test.jpg')
    color_thief = ColorThief('test.jpg')
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=20)
    counter=0
    for col in palette:
        new_im = Image.new('RGB', (total_width, max_height), color=col)
        new_im.save('test'+str(counter)+'.jpg')
        counter+=1
    print(palette)
    return(palette)

def bookBotify(bookvar):
    bookBot(bookvar)
    processImages()

bookBotify("Dune")
