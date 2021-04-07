import pandas as pd
from datetime import date
import time
import csv
from bs4 import BeautifulSoup
import requests
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

while(True):
    my_soup = getSoup()
    sentiment = my_soup.find("tr")
    sentiment_liste = getSentiment(sentiment)
    sentiment_liste.append(str(getLastUpdate(my_soup)))
    sentiment_liste.append(date.today())
    writeToCSV(sentiment_liste)
    time.sleep(30)








