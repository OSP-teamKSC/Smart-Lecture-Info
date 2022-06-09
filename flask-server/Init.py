import schedule
import time
import threading
import DB.crawlAndInsert as crawlAndInsert
import DB.crawlAndUpdate as crawlAndUpdate
def updateDB(DBPW):
    crawlAndUpdate.crawlAndUpdate(2022, 0, False, DBPW)
    crawlAndUpdate.crawlAndUpdate(2022, 0, True, DBPW)


def init(DBPW):
    th1 = threading.Thread(target=updateDB(DBPW))
    th1.daemon = True
    th1.start()
