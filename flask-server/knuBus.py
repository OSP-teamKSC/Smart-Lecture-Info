import mysql.connector
import json
mydb = mysql.connector.connect(
    host="osp-db-server.mysql.database.azure.com",
    user="KSC",
    passwd="1q2w3e4r@@",
    database="knubus"
)
myData = {
    'Grade': '', #학년
    'Gubun': '',  # 전공, 교양, 첨성인**
    'SubjectName': '',  # 과목 명
    'SubjectCode': '',  # 과목 코드
    'ClassCode': '',  # 과목 코드 (분반 포함)
    'ClassDivideNumber': '',  # 분반
    'EstablishedUniversity': '',  # 개설 대학
    'EstablishedDepartment': '',  # 개설 학과
    'SearchUniversity': '',     #검색시 사용할 대학명
    'SearchDepartment': '',  # 검색시 사용할 학과명
    'ProfessorNames': '',  # 교수명 (배열 형식임)
    'Season': '',  # 개설 학기
    'ApplicantsMax': '',  # 수강 총원
    'ApplicantsCurrent': '',  # 수강 인원
    'IsUntact': '',  # 비대면 여부(Y or N)
    'Schedule': '',  # 시간표 (배열 형식임)
    'Credit': '',  # 학점
    'Rate1': '',  # 출석 비중
    'Rate2': '',  # 중간 시험
    'Rate3': '',  # 기말 시험
    'Rate4': '',  # 과제
    'Rate5': '',  # 발표
    'Rate6': '',  # 토론
    'Rate7': '',  # 안전교육
    'Rate8': '',  # 기타
    'Rate9': '',  # ?
    'PriorSubject': '',  # 권장선수과목
    'SubsequentSubject': '',  # 권장후수과
}

temp = {
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
# myColumns = ['Gubun', 'SubjectName', 'SubjectCode', 'ClassCode', 'ClassDivideNumber', 'EstablishedUniversity', 'EstablishedDepartment', 'ProfessorNames', 'Season', 'ApplicantsMax', 'ApplicantsCurrent', 'IsUntact', 'Schedule', 'Credit', 'Rate1', 'Rate2', 'Rate3', 'Rate4', 'Rate5', 'Rate6', 'Rate7', 'Rate8', 'Rate9', 'PriorSubject', 'SubsequentSubject']
myColumns = ['Grade', 'Gubun', 'SubjectName', 'SubjectCode', 'ClassCode', 'ClassDivideNumber', 'EstablishedUniversity', 'EstablishedDepartment', 'SearchUniversity', 'SearchDepartment', 'ProfessorNames', 'Season', 'ApplicantsMax', 'ApplicantsCurrent', 'IsUntact', 'Schedule', 'Credit', 'Rate1', 'Rate2', 'Rate3', 'Rate4', 'Rate5', 'Rate6', 'Rate7', 'Rate8', 'Rate9', 'PriorSubject', 'SubsequentSubject']

def transForm(data):
    tempData = myData
    #tempData['Season'] = data['Season']
    #tempData['SearchDepartment'] = data['SearchDepartment']
    for i in data:
        if data[i] != '':
            tempData[i] = data[i]
    if data['Gubun'] == 'GE':
        tempData['Gubun'] = '교양'

    elif data['Gubun'] == 'UN':
        tempData['Gubun'] = '전공'
        tempData['SearchUniversity'] = data['SearchUniversity']
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
        print(rows)
        dataDict_Value = {}
        for word, col in zip(rows, myColumns):
            if col == 'SearchDepartment':       # 전공 분류
                word = word.split(', ')
                if data[col] not in word:
                    continue
                word = data[col]
            dataDict_Value[col] = word
        dataDict[i] = dataDict_Value
        i += 1
    return dataDict
