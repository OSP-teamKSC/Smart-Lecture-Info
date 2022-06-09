import os
import json
import crawler.GetClassList
import pymysql as sql


def unInsert(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    insertDB('./jsons/{}/{}/'.format(year, season), 'un' + str(year) + str(season), passwd)


def geInsert(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    insertDB('./jsonsge/{}/{}/'.format(year, season), 'ge' + str(year) + str(season), passwd)


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
                    print("Inserting [%s, %s] to 교양" % (i["SubjectName"], i["ClassCode"]))  # 삽입 성공

                except sql.IntegrityError:
                    cursor.execute(sql_duplicate, (", ", i["ClassCode"]))  # 쉼표추가
                    cursor.execute(sql_duplicate,
                                   (i["EstablishedDepartment"], i["ClassCode"]))  # 중복된 상황에서 예외 않고 한 칼럼에 추가
                    print("%s %s %s already in 교양" % (
                        i["ClassCode"], i["EstablishedUniversity"], i["EstablishedDepartment"]))  # 이미 삽입한 값

    mydb.commit()
    cursor.close()
    print("done.")


def crawlAndInsert(year, season, isGE=False):
    if (season < 0 or season > 3):
        print('invalid season value.')
        return
    passwd = input('mysql passwd : ')
    try:
        if not isGE:
            crawler.GetClassList.getUnivList(year, season)
            crawler.GetClassList.getAllDepartments(year, season)
            crawler.GetClassList.getAllMajorClasses(year, season,True)
        else:
            crawler.GetClassList.getGEList()
            crawler.GetClassList.getAllGEClasses(year, season,True)
    except:
        print('failed to crawl...')
        return

    if not isGE:
        unInsert(year,season,passwd)
    else:
        geInsert(year,season,passwd)


if __name__ == '__main__':
    # crawler.GetClassList.getAllGEClasses(2022,1,True)
    crawlAndInsert(2022,1,False)
