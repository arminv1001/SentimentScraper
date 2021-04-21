import sqlite3
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    c = conn.cursor()
    c.execute(create_table_sql)
    c.close()

def createConnection():
    try:
        conn = sqlite3.connect('SentimentDB.db')
        print("Connected")
        sentimentTable_SQL = """ CREATE TABLE IF NOT EXISTS Sentiment (
                                                id integer PRIMARY KEY AUTOINCREMENT,
                                                call_s integer NOT NULL,
                                                putt_s integer NOT NULL,
                                                timeStempel datetime UNIQUE
                                            ); """
        create_table(conn, sentimentTable_SQL)
        return conn
    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

def insertCSV(conn,row_csv):
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Sentiment ( call_s, putt_s, timeStempel) VALUES (?,?,?)",
                          (row_csv[0],row_csv[1],row_csv[2]))
    except sqlite3.Error as error:
        print("ERROR-Insert")
        print(error)
    conn.commit()
    cursor.close()

