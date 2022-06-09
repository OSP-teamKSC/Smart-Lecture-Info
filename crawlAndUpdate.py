import os
import json
import crawler.GetClassList
import pymysql as sql


# 연도, 학기를 입력하면 대학 목록에서 json 불러와서 db로 update.
def unUpdate(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    updateDB('./jsons/{}/{}/simple/'.format(year, season), 'un' + str(year) + str(season), passwd)


# 연도, 학기를 입력하면 교양 목록에서 json 불러와서 db로 update.
def geUpdate(year, season, passwd=''):
    if passwd == '':
        passwd = input("password : ")
    updateDB('./jsonsge/{}/{}/simple/'.format(year, season), 'ge' + str(year) + str(season), passwd)


# 경로, 테이블명, db 비밀번호를 입력하면 선택한 경로의 json 파일들을 불러와서 테이블 update.
def updateDB(path, name, passwd):
    mydb = sql.connect(host='osp-db-server.mysql.database.azure.com', user='KSC',
                           passwd=passwd, db='knubus')
    cursor = mydb.cursor()
    files = os.listdir(path)
    sql_update = "update {} set ApplicantsCurrent = %s where ClassCode = %s".format(name)
    queries = []
    for file in files:
        with open(path + file, 'r') as json_file:
            json_data = json.load(json_file)
            json_line = json_data
            print(len(json_line))
            for i in json_line:
                queries.append((i['ApplicantsCurrent'], i['ClassCode']))

    try:
        print("Inserting to table...")
        cursor.executemany(sql_update, queries)

    except sql.IntegrityError:
        print('err...')
    mydb.commit()
    cursor.close()
    print("Done")


# 연도, 학기, 교양 유무를 입력하면 크롤러를 실행하여 자동으로 강의계획서 없는 json 파일을 크롤링하고 db를 update.
def crawlAndUpdate(year, season, isGE=False, passwd=''):
    # 잘못된 학기명을 입력시 return
    if season < 0 or season > 3:
        print('invalid season value.')
        return
    if passwd == '':
        passwd = input('mysql passwd : ')
    try:
        if not isGE:
            # 대학 목록 불러오기
            crawler.GetClassList.getUnivList(year, season)
            # 학과 목록 불러오기
            crawler.GetClassList.getAllDepartments(year, season)
            # 강의 목록 불러오기
            crawler.GetClassList.getAllMajorClasses(year, season, False)
        else:
            # 교양 세부 목록 불러오기
            crawler.GetClassList.getGEList()
            # 교양 강의 목록 불러오기
            crawler.GetClassList.getAllGEClasses(year, season, False)
    except:
        # 예외 발생시 바로 작동 중단
        print('failed to crawl...')
        return

        # json 파일 로드 완료시 즉시 db로 insert 진행
    if not isGE:
        unUpdate(year, season, passwd)
    else:
        geUpdate(year, season, passwd)

if __name__ == '__main__':
    crawlAndUpdate(2022,0,False)
