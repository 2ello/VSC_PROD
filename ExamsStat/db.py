import sqlite3
from sqlite3 import Error
from datetime import datetime

def createDb(db_file, subject):
    
    dbName = subject[:4]
    try:
        conn = sqlite3.connect(db_file)
        cu = conn.cursor()
        cu.execute(f"create table if not exists {dbName}StatTable(score,date)")
    except Error as e:
        pass
    finally:
        if conn:
            conn.close()


def queryToDb(subject, date, db_file):
    
    dbName = subject[:4]
    records = []
    month = int(date.split(",")[1])
    if month < 10:
        month = "0"+str(month)
    
    dateR = (str(date.split(',')[0]) + str(month) + str(date.split(',')[2])).replace(" ", "")
    try:
        conn = sqlite3.connect(db_file)
        cu = conn.cursor()
        sqlite_select_query = f"""SELECT score from {dbName}StatTable WHERE date={dateR}"""
        records = cu.execute(sqlite_select_query).fetchall()
        
        conn.commit()
        cu.close()
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

    strRecords = str(records)
    
    length = len(strRecords)
    intRecords = []
    i = 0

    while i < length:
        s_int = ''
        while i < length and '0' <= strRecords[i] <= '9':
            s_int += strRecords[i]
            i += 1
            
        i += 1
        
        if s_int != '':
            intRecords.append(int(s_int))

    
    return intRecords


def insert_into(subject, score, date, db_file):
    dbName = subject[:4]    
    conn = sqlite3.connect(db_file)
    cu = conn.cursor()
    month = int(date.split(",")[1])
    day = int(date.split(",")[2])
    if month < 10:
        month = "0"+str(month)
    if day < 10:
        day = "0"+str(day)

    dateR = str(date.split(',')[0]) + str(month) + str(day).replace(" ", "")

    cu.execute(f"""INSERT INTO {dbName}StatTable
                          (score, date)  VALUES  ({int(score)}, {str(dateR)})""")
    conn.commit()
    cu.close()


def deleteScoreFromDB(subject, date, db_file):

        month = int(date.split(",")[1])
        day = int(date.split(",")[2])
        if month < 10:
            month = "0"+str(month)
        if day < 10:
            day = "0"+str(day)

        dateR = str(date.split(',')[0]) + str(month) + str(day).replace(" ", "")
        try:
                conn = sqlite3.connect(db_file)
                cu = conn.cursor()
                dbName = subject[:4]
                cu.execute(f"""DELETE from {dbName}StatTable WHERE date={dateR}""")
                conn.commit()
                cu.close()
        except sqlite3.Error as error:
                print("Ошибка при работе с SQLite", error)
        finally:
                if conn:
                    conn.close()
            

def startedPointsGraph(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cu = conn.cursor()
        dateR = []
        day = '01'
        month = 1
        
        year = datetime.now().year
        while int(month) < 13:

            if int(month) < 10:
                month = "0"+str(month)
            dateR.append(f'{year}{month}{day}')
            if int(month) < 10:
                month = month[1:]
            month = int(month) + 1
            
        subjectList = ["mathematics","informatics","language"]
        for subject in subjectList:
            subject = subject[:4]
            for date in dateR:
                score = cu.execute(f'SELECT score FROM {subject}StatTable WHERE date={str(date)}').fetchall()
                if score:
                    pass
                else:
                    
                    cu.execute(f"""INSERT OR IGNORE INTO {subject}StatTable
                                    (score, date)  VALUES  (NULL, {str(date)})""")
                    conn.commit()
                    print(f"для даты {date} создана пустая запись в таблице {subject}StatTable")
            
        cu.close()
    except:
        try:
            createDb(db_file, "mathematics")
            createDb(db_file, "informatics")
            createDb(db_file, "language")
            startedPointsGraph(db_file)
        except:
            print("Начальные данные не записались в бд")

