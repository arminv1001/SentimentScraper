import os
from datetime import date
import time
import csv
from bs4 import BeautifulSoup
import requests
import DBConnetion
import logging

def getSoup():
    """
    Convert the Pagen https://www.wallstreet-online.de/indizes/put-call-sentiment-dax-index to BeatifulSoup
    :return: the page in beatiful soup - object
    """
    url = "https://www.wallstreet-online.de/indizes/put-call-sentiment-dax-index"
    try:
        page = requests.get(url).text
    except:
        return None
    my_soup = BeautifulSoup(page,"html.parser")
    return my_soup

def getSentiment(sentiment):
    """
    Extract from Soup the sentiment
    :param sentiment: Sentiment block from Soup
    :return: list with Senitment 0 - Call ---- 1 - Put
    """
    sentiment_liste = list(filter(None,sentiment.text.split("\n")))
    for index in range(len(sentiment_liste)):
        sentiment_liste[index] = sentiment_liste[index].replace("CALL: ", "").replace("PUT: ", "").replace("%", "").replace(",",".")
        sentiment_liste[index] = float(sentiment_liste[index])
    return sentiment_liste

def getLastUpdate(my_soup):
    """
    Scrap the last update time stamp.
    :param my_soup: page as a soup
    :return: last update date time as string
    """
    last_update_string = None
    last_update_soup = my_soup.find_all("div", class_="time firstRow hidden-xs")
    for element in last_update_soup:
        last_update_string = element.text.replace("\n", "").replace(" ", "").replace("LetzterKurs", "")
    return last_update_string

def writeToCSV(sentiment_liste):
    """
    Writes the Sentiment list in a csv File
    :param sentiment_liste: contains the sentiment and the time stamp
    :return: -
    """
    with open("Sentiment.csv","a") as fd:
        wr = csv.writer(fd, dialect='excel')
        wr.writerow(sentiment_liste)
        fd.close()

def readCSV():
    """
    Reads the CSV File and exports the entry's into the database. After successfully uploading the CSV-File the CSV-File will be removed.
    :return: -
    """
    with open("Sentiment.csv") as fd:
        csv_read = csv.reader(fd, delimiter=',')
        conn = DBConnetion.createConnection()
        for row in csv_read:
            DBConnetion.insertCSV(conn,row)
        fd.close()
    os.remove("Sentiment.csv")


if __name__ == "__main__":
    # start Scraper
    TO_DB = 10 # After how much csv entrys ride to DB
    counter_TO_DB = 0
    logging.basicConfig(level=logging.INFO,filename='sentiment_scrapper_log.txt', format='%(levelname)s - %(message)s')
    while(True):
        my_soup = getSoup()
        sentiment = my_soup.find("tr") # find sentiment block
        sentiment_liste = getSentiment(sentiment)
        sentiment_liste.append(str(date.today()) + " " + str(getLastUpdate(my_soup)))
        writeToCSV(sentiment_liste)
        counter_TO_DB +=1
        if(counter_TO_DB == TO_DB):
            readCSV()
            logging.info("{} / {} - wrote to CSV".format(counter_TO_DB, TO_DB))
            logging.info("wrote to DB - restart cycle" )
            counter_TO_DB = 0
        else:
            logging.info("{} / {} - wrote to CSV".format(counter_TO_DB,TO_DB))
        time.sleep(80)








