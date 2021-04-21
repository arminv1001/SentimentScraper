import os

import pandas as pd
from datetime import date
import time
import csv
from bs4 import BeautifulSoup
import requests
import DBConnetion
def getSoup():
    url = "https://www.wallstreet-online.de/indizes/put-call-sentiment-dax-index"
    page = requests.get(url).text
    my_soup = BeautifulSoup(page,"html.parser")
    return my_soup
# 0 - Call ---- 1 - Put

def getSentiment(sentiment):
    sentiment_liste = list(filter(None,sentiment.text.split("\n")))
    for index in range(len(sentiment_liste)):
        sentiment_liste[index] = sentiment_liste[index].replace("CALL: ", "").replace("PUT: ", "").replace("%", "").replace(",",".")
        sentiment_liste[index] = float(sentiment_liste[index])
    return sentiment_liste

def getLastUpdate(my_soup):
    last_update_soup = my_soup.find_all("div", class_="time firstRow hidden-xs")
    for element in last_update_soup:
        last_update_string = element.text.replace("\n", "").replace(" ", "").replace("LetzterKurs", "")
    return last_update_string

def writeToCSV(sentiment_liste):
    with open("Sentiment.csv","a") as fd:
        wr = csv.writer(fd, dialect='excel')
        wr.writerow(sentiment_liste)
        fd.close()

def readCSV():
    with open("Sentiment.csv") as fd:
        csv_read = csv.reader(fd, delimiter=',')
        line_count = 0
        conn = DBConnetion.createConnection()
        for row in csv_read:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                DBConnetion.insertCSV(conn,row)
        fd.close()
    os.remove("Sentiment.csv")




TO_DB = 5
counter_TO_DB = 0
while(True):
    my_soup = getSoup()
    sentiment = my_soup.find("tr")
    sentiment_liste = getSentiment(sentiment)
    sentiment_liste.append(str(date.today()) + " " + str(getLastUpdate(my_soup)))
    writeToCSV(sentiment_liste)
    counter_TO_DB +=1
    if(counter_TO_DB == TO_DB):
        readCSV()
        print("Finish")
        break
    print(counter_TO_DB)
    time.sleep(60)








