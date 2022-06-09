import schedule
import time
import threading

def printHello():
    while True:
        print("Hello")
        time.sleep(10)

def init():
    th1 = threading.Thread(target=printHello)
    th1.daemon = True
    th1.start()
