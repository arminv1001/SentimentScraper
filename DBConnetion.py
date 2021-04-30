import sqlite3
import logging

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return: -
    """
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

def createConnection():
    """
    Creates the necessary tables if they arent already existing.
    :return: connection to database
    """
    conn = sqlite3.connect('SentimentDB.db')
    logging.info("Connected")
    sentimentTable_SQL = """ CREATE TABLE IF NOT EXISTS Sentiment (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            call_s integer NOT NULL,
                                            putt_s integer NOT NULL,
                                            timeStempel datetime UNIQUE
                                        ); """
    create_table(conn, sentimentTable_SQL)
    return conn


def insertCSV(conn,row_csv):
    """
    Insert Sentiment-list in to the database
    :param conn: connection to database
    :param row_csv: sentiment-liste
    :return: -
    """
    cursor = conn.cursor()
    try:
        # Ignore because of same time stamps means same value
        cursor.execute("INSERT OR IGNORE INTO Sentiment ( call_s, putt_s, timeStempel) VALUES (?,?,?)",
                          (row_csv[0],row_csv[1],row_csv[2]))
    except sqlite3.Error as Error:
        logging.error("ERROR-Insert")
        logging.error(Error)
    conn.commit()
    cursor.close()

