import os
import json
import DB.crawler.GetClassList as GetClassList

import pymysql as sql


# 연도, 학기를 입력하면 대학 목록에서 json 불러와서 db로 insert.
def unInsert(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    insertDB('./jsons/{}/{}/'.format(year, season), 'un' + str(year) + str(season), passwd)


# 연도, 학기를 입력하면 교양 목록에서 json 불러와서 db로 insert.
def geInsert(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    insertDB('./jsonsge/{}/{}/'.format(year, season), 'ge' + str(year) + str(season), passwd)


# 경로, 테이블명, db 비밀번호를 입력하면 선택한 경로의 json 파일들을 불러와서 테이블로 insert.
def insertDB(path, name, passwd):
    mydb = sql.connect(host='osp-db-server.mysql.database.azure.com', user='KSC', passwd=passwd, db='knubus')
    dir = path
    files = os.listdir(dir)
    cursor = mydb.cursor()
    for file in files:
        if '.json' not in file:
            continue
        with open(dir + file, 'r') as json_file:
            json_data = json.load(json_file)
            json_line = json_data
            for i in json_line:
                sql_insert = \
                    "insert into {} (Grade, Gubun, SubjectName, SubjectCode, ClassCode, ClassDivideNumber, " \
                    "EstablishedUniversity, EstablishedDepartment, SearchUniversity, SearchDepartment, " \
                    "ProfessorNames, Season, " \
                    "ApplicantsMax, ApplicantsCurrent, IsUntact, Schedule, Credit, Rate1, Rate2, Rate3, Rate4, Rate5, " \
                    "Rate6, Rate7, Rate8, Rate9, PriorSubject, SubsequentSubject) values(%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                    "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)".format(name)
                ts = ''
                if i['Schedule'] is not None:
                    for index in range(0, len(i['Schedule'])):
                        if index < len(i['Schedule']) - 2 and i['Schedule'][index] == ',' \
                                and i['Schedule'][index + 2] == ' ':
                            ts += '|'
                        else:
                            ts += i['Schedule'][index]

                    i['Schedule'] = ts
                sql_duplicate = "update {} set SearchDepartment = concat(SearchDepartment, %s) " \
                                "where ClassCode = (%s)".format(name)

                try:
                    cursor.execute(sql_insert, (
                        i["Grade"], i["Gubun"], i["SubjectName"], i["SubjectCode"], i["ClassCode"],
                        i["ClassDivideNumber"],
                        i["EstablishedUniversity"], i["EstablishedDepartment"], i["SearchUniversity"],
                        i["SearchDepartment"], i["ProfessorNames"], i["Season"], i["ApplicantsMax"],
                        i["ApplicantsCurrent"],
                        i["IsUntact"], i["Schedule"], i["Credit"], i["Rate1"], i["Rate2"], i["Rate3"], i["Rate4"],
                        i["Rate5"], i["Rate6"], i["Rate7"], i["Rate8"], i["Rate9"], i["PriorSubject"],
                        i["SubsequentSubject"]))
                    print("Inserting [%s, %s] to tabel" % (i["SubjectName"], i["ClassCode"]))  # 삽입 성공

                except sql.IntegrityError:
                    cursor.execute(sql_duplicate, (", ", i["ClassCode"]))  # 쉼표추가
                    cursor.execute(sql_duplicate,
                                   (i["EstablishedDepartment"], i["ClassCode"]))  # 중복된 상황에서 예외 않고 한 칼럼에 추가
                    print("%s %s %s already in tabel" % (
                        i["ClassCode"], i["EstablishedUniversity"], i["EstablishedDepartment"]))  # 이미 삽입한 값

    mydb.commit()
    cursor.close()
    print("done.")


# 연도, 학기, 교양 유무를 입력하면 크롤러를 실행하여 자동으로 크롤링하고 db로 insert.
def crawlAndInsert(year, season, isGE=False, passwd=''):
    # 잘못된 학기명을 입력시 return
    if (season < 0 or season > 3):
        print('invalid season value.')
        return
    if passwd == '':
        passwd = input('mysql passwd : ')
    try:
        if not isGE:
            # 대학 목록 불러오기
            GetClassList.getUnivList(year, season)
            # 학과 목록 불러오기
            GetClassList.getAllDepartments(year, season)
            # 강의 목록 불러오기
            GetClassList.getAllMajorClasses(year, season, True)
        else:
            # 교양 세부 목록 불러오기
            GetClassList.getGEList()
            # 교양 강의 목록 불러오기
            GetClassList.getAllGEClasses(year, season, True)
    except:
        # 예외 발생시 바로 작동 중단
        print('failed to crawl...')
        return

        # json 파일 로드 완료시 즉시 db로 insert 진행
    if not isGE:
        unInsert(year, season, passwd)
    else:
        geInsert(year, season, passwd)
