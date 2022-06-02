import mysql.connector
import json
mydb = mysql.connector.connect(
    host="osp-db-server.mysql.database.azure.com",
    user="KSC",
    passwd="1q2w3e4r@@",
    database="knubus"
)

myData = {
    "구분": "",
    "과목명": "",
    "과목코드": "",
    "과목코드_분반포함": "",
    "분반": "",
    "개설대학": "",
    "개설학과": "",
    "교수명": "",
    "개설학기": "",
    "수강총원": "",
    "수강인원": "",
    "비대면여부": "",
    "시간표": "",
    "학점": "",
    "출석비중": "",
    "중간고사": "",
    "기말고사": "",
    "과제": "",
    "발표": "",
    "토론": "",
    "안전교육": "",
    "기타": "",
    "etc": "",
    "권장선수과목": "",
    "권장후수과목": "",
}
myColumns = ['Gubun', 'SubjectName', 'SubjectCode', 'ClassCode', 'ClassDivideNumber', 'EstablishedUniversity', 'EstablishedDepartment', 'ProfessorNames', 'Season', 'ApplicantsMax', 'ApplicantsCurrent', 'IsUntact', 'Schedule', 'Credit', 'Rate1', 'Rate2', 'Rate3', 'Rate4', 'Rate5', 'Rate6', 'Rate7', 'Rate8', 'Rate9', 'PriorSubject', 'SubsequentSubject']


def transForm(data):
    tempData = myData
    tempData['개설학기'] = data['semester']
    tempData['개설학과'] = data['major']
    if data['university'] == 'GE':
        tempData['구분'] = data['college']
        if data['Core'] != "선택":
            tempData['개설학과'] = data['Core']

    elif data['university'] == 'UN':
        tempData['개설대학'] = data['college']
    return tempData

def searchWord(data):
    tempData = transForm(data)
    str = " where"
    cnt = 0
    for word in tempData:
        if tempData[word] == "":
            continue
        if cnt != 0:
            str += ' and'
        cnt = cnt + 1
        str += " {0} like '%{1}%'".format(word, tempData[word])
    return str

def accessDataBase(data):
    str = searchWord(data)
    dataDict = {}
    cursor = mydb.cursor()
    query = ("select * from 강의" + str)
    print(query)
    cursor.execute(query)
    print("Connection established")

    i = 0
    for rows in cursor:
        dataDict_Value = {}
        for word, col in zip(rows, myColumns):
            dataDict_Value[col] = word

        dataDict[i] = dataDict_Value
        i += 1

    return dataDict
