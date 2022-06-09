import schedule
import time
import threading
import DB.crawlAndInsert as crawlAndInsert
import DB.crawlAndUpdate as crawlAndUpdate
def updateDB(DBPW):
    while True:
        for season in range(0, 4):
            crawlAndUpdate.crawlAndUpdate(2022, season, True, DBPW)
            crawlAndUpdate.crawlAndUpdate(2022, season, False, DBPW)
        time.sleep(5)


def init(DBPW):
    th1 = threading.Thread(target=updateDB(DBPW))
    th1.daemon = True
    th1.start()
