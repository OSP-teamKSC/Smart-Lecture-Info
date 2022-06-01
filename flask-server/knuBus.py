import mysql.connector
import json
mydb = mysql.connector.connect(
    host="osp-db-server.mysql.database.azure.com",
    user="KSC",
    passwd="1q2w3e4r@@",
    database="knubus"
)

getData = {
    "구분": "",
    "개설학기": "",
    "개설대학": "",
    "개설학과": "",
    "과목명": "",
}

def transForm(data):
    if data["subject"] == "GE":
        getData["구분"] = data["university"]
    elif data["subject"] == "UN":
        getData["개설대학"] = data["university"]

    getData["개설학기"] = data["semester"]
    getData["과목명"] = data["deparment"]
    if data["addOn"] != "":
        getData["과목명"] = data["addOn"]

def searchWord(data):
    transForm(data)
    str = " Where"
    cnt = 0
    for word in getData:
        if getData[word] == "":
            continue
        if cnt != 0:
            str += ' and'
        cnt = cnt + 1
        str += " {0} = '{1}'".format(word, getData[word])
    return str

def accessDataBase():
    # str = searchWord(data)
    dataList = {}
    cursor = mydb.cursor()
    query = ("select * from 강의" )

    cursor.execute(query)

    i = 0
    for ddd in cursor:
        dataList[i] = ddd
        i+=1

    print("Connection established")

    return dataList
