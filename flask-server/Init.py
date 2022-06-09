import time
import threading
import DB.crawlAndInsert as crawlAndInsert
import DB.crawlAndUpdate as crawlAndUpdate

def InsertDB(DBPW):
    for season in range(0, 4):
        crawlAndInsert.crawlAndInsert(2022, season, False, DBPW)
        crawlAndInsert.crawlAndInsert(2022, season, True, DBPW)

def updateDB(DBPW):
    while True:
        for season in range(0, 2):
            crawlAndUpdate.crawlAndUpdate(2022, season, False, DBPW)
            crawlAndUpdate.crawlAndUpdate(2022, season, True, DBPW)
        time.sleep(300)


def init(DBPW):
    th1 = threading.Thread(target=updateDB, args=[DBPW])
    th1.daemon = True
    th1.start()

