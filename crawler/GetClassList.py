import json
import requests
import os
import ClassJsonConverter
import time
from pathlib import Path

crawlURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectItttnCdListLectPlnInqr'
crawlLectureURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectListLectPlnInqr'
crawlListURL = 'https://knuin.knu.ac.kr/public/cmmnn/cmmbs/code/selectListCode'

seasons = ['CMBS001400001',  # 1학기
           'CMBS001400004',  # 여름학기
           'CMBS001400002',  # 2학기
           'CMBS001400003']  # 겨울학기

GEcodes = ['STCU001000005',  # 첨성인기초
           'STCU001000006',  # 첨성인핵심
           'STCU001000007',  # 첨성인일반
           'STCU001000028',  # 첨성인소양
           'STCU001100027',  # 첨성인핵심 / 인문.사회
           'STCU001100028']  # 첨성인핵심 / 자연과학

# 대학 목록 조회 페이로드
getUnivListPayload = {
    "search": {
        "gubun": "02",
        "code": "02",
        "name": "대학",
        "estblYear": "",
        "estblSmstrSctcd": "",
        "isApi": "Y",
        "rowStatus": "U"
    }
}

# 전공 목록 조회 페이로드
getDepartmentListPayload = {
    "search": {
        "gubun": "03",
        "code": "",
        "name": "",
        "estblYear": "2022",
        "estblSmstrSctcd": "CMBS001400001",
        "isApi": "Y",
        "rowStatus": "R"
    }
}

# 교양 과목 조회 페이로드
getGEClassPayload = {
    "search": {
        "estblYear": "2022",
        "estblSmstrSctcd": "CMBS001400001",
        "sbjetCd": "",
        "sbjetNm": "",
        "crgePrfssNm": "",
        "sbjetRelmCd": "",
        "sbjetSctcd": "",
        "estblDprtnCd": "",
        "rmtCrseYn": "",
        "rprsnLctreLnggeSctcd": "",
        "flplnCrseYn": "",
        "pstinNtnnvRmtCrseYn": "",
        "dgGbDstrcRmtCrseYn": "",
        "gubun": "01",
        "isApi": "Y",
        "bldngSn": "",
        "bldngCd": "",
        "bldngNm": "",
        "lssnsLcttmUntcd": "",
        "sbjetSctcd2": "",
        "contents": ""
    }
}

# 전공 과목 조회 페이로드
getMajorClassPayload = {
    "search": {
        "estblYear": "2022",
        "estblSmstrSctcd": "CMBS001400001",
        "sbjetCd": "",
        "sbjetNm": "",
        "crgePrfssNm": "",
        "sbjetRelmCd": "",
        "sbjetSctcd": "",
        "estblDprtnCd": "",
        "rmtCrseYn": "",
        "rprsnLctreLnggeSctcd": "",
        "flplnCrseYn": "",
        "pstinNtnnvRmtCrseYn": "",
        "dgGbDstrcRmtCrseYn": "",
        "gubun": "01",
        "isApi": "Y",
        "bldngSn": "",
        "bldngCd": "",
        "bldngNm": "",
        "lssnsLcttmUntcd": "",
        "sbjetSctcd2": "",
        "contents": ""
    }
}

# 교양 세부항목 조회 페이로드
getGEListPayload = {
    "search": {
        # "reqId": "",
        "key": "STCU0011",
        "upperKey": "",  # 가변코드
        "listCode": "false",
        "attrs": [],
        "searchParam": ""
    }
}

requestHeader = {'Content-Type': 'application/json'}


def getGEList():
    # 첨성인 기초 세부항목 조회
    Path('./UnivGE').mkdir(exist_ok=True)
    getGEListPayload['search']['upperKey'] = GEcodes[0]
    getGEListPayload['search']['key'] = 'STCU0011'
    request = json.dumps(getGEListPayload)
    response = requests.post(crawlListURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    with open('./UnivGE/첨성인기초.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)

    # 첨성인 소양 세부항목 조회
    getGEListPayload['search']['upperKey'] = GEcodes[3]
    request = json.dumps(getGEListPayload)
    response = requests.post(crawlListURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    with open('./UnivGE/첨성인소양.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)

    # 첨성인 핵심 - 인문/사회 세부항목 조회
    getGEListPayload['search']['upperKey'] = GEcodes[4]
    getGEListPayload['search']['key'] = 'STCU0012'
    request = json.dumps(getGEListPayload)
    response = requests.post(crawlListURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    with open('./UnivGE/첨성인핵심인문.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)

    # 첨성인 핵심 - 자연과학 세부항목 조회
    getGEListPayload['search']['upperKey'] = GEcodes[5]
    request = json.dumps(getGEListPayload)
    response = requests.post(crawlListURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    with open('./UnivGE/첨성인핵심자연.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)


# 대학 목록 조회
def getUnivList(year=2022, season=0):
    getUnivListPayload['search']['estblYear'] = str(year)
    getUnivListPayload['search']['estblSmstrSctcd'] = seasons[season]
    request = json.dumps(getUnivListPayload)
    response = requests.post(crawlURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    with open('./UnivList.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)


# 전공 목록 조회
def getDepartmentList(univ_name, univ_code, file_name, year=2022, season=0):
    getDepartmentListPayload['search']['code'] = univ_code
    getDepartmentListPayload['search']['name'] = univ_name
    getDepartmentListPayload['search']['estblYear'] = str(year)
    getDepartmentListPayload['search']['estblSmstrSctcd'] = seasons[season]
    request = json.dumps(getDepartmentListPayload)
    response = requests.post(crawlURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    json_data = response.json()
    if len(json_data['data']) == 0:
        return
    with open('./{0}.json'.format(file_name), 'w') as savefile:
        json.dump(json_data, savefile, indent=4)


# 모든 대학의 전공 조회
def getAllDepartments(year=2022, season=0):
    with open('./UnivList.json', 'r') as openfile:
        json_data = json.load(openfile)
        for univ in json_data['data']:
            univCode = univ['code']
            univName = univ['name']
            Path('./UnivMajor').mkdir(exist_ok=True)
            Path('./UnivMajor/{}'.format(str(year))).mkdir(exist_ok=True)
            Path('./UnivMajor/{}/{}'.format(str(year), str(season))).mkdir(exist_ok=True)
            getDepartmentList(univName, univCode, 'UnivMajor/{0}/{1}/univ_{2}'.format(str(year), str(season), univName),
                              year, season)

# 전공 과목 조회

def getMajorClass2(depart_code, index, year=2022, season=0, withSyllabus = False, forTest = None, depart_name='',univ_name=''):
    t = 0
    if(os.path.exists('./jsons/{0}.json'.format(index+t))):
        print('file exist. passing..')
        t+=1
        return t

    getMajorClassPayload['search']['estblDprtnCd'] = depart_code
    getMajorClassPayload['search']['estblYear'] = str(year)
    getMajorClassPayload['search']['estblSmstrSctcd'] = seasons[season]
    request = json.dumps(getMajorClassPayload)
    for i in range(0, 5):
        try:
            response = requests.post(crawlLectureURL, request, headers=requestHeader)
        except requests.exceptions.ConnectionError:
            if i == 4:
                print('Connection Failed')
                return None
            print('Connection Error, Retrying... {}/{}'.format(i + 1, 5))
            continue
        break

    if response.status_code >= 400:
        print('failed to get file : no response')
        return
    if len(response.json()['data']) == 0:
        print('failed to get file : no data')
        return
    if(forTest):
        forTest(len(response.content)/1024)
    with open('./jsons/{0}.json'.format(index+t), 'w') as savefile:
        json.dump(ClassJsonConverter.ConvertJSON(response.json(),withSyllabus,forTest,univ_name,depart_name), savefile, indent=4)
    t+=1
    print('.', end='')
    return t


# 교양 과목 조회

def getGEClass2(index, openfile, year=2022, season=0, withSyllable=False, forTest=None, GubunName=''):
    t = 0
    lastTime = time.time()
    with open(openfile, 'r') as readfile:
        for sub in json.load(readfile)['data']['option']['codes']:
            name = sub['codeNm']
            code = sub['codeId']

            if(os.path.exists('./jsonsge/{0}.json'.format(index+t))):
                print('file exist. passing..')
                t+=1
                continue

            path = Path('./jsonsge/{}'.format(index+t))
            t+=1
            getGEClassPayload['search']['sbjetRelmCd'] = code
            getGEClassPayload['search']['estblYear'] = str(year)
            getGEClassPayload['search']['estblSmstrSctcd'] = seasons[season]
            request = json.dumps(getGEClassPayload)
            for i in range(0,5):
                try:
                    response = requests.post(crawlLectureURL, request, headers=requestHeader)
                except requests.exceptions.ConnectionError:
                    if i == 4:
                        print('Connection Failed')
                        return None
                    print('Connection Error, Retrying... {}/{}'.format(i+1,5))

                    continue
                break

            if response.status_code >= 400:
                print('failed to get file : no response')
                return
            if len(response.json()['data']) == 0:
                print('failed to get file : no data')
                return
            if forTest:
                forTest(len(response.content) / 1024)
            with open('{0}.json'.format(path), 'w') as savefile:
                json.dump(ClassJsonConverter.ConvertJSON(response.json(), withSyllable, forTest,GubunName,name, GubunName), savefile,
                          indent=4)
            print('.', end='')
        print('done!')
        print('elapsed time : {}ms'.format(round((time.time() - lastTime) * 1000)))
        return t


# 대학 전공 과목 조회
def getMajorClassesInUnivAlt(index, univ_file, univName, year=2022, season=0,withSyllabus = False, forTest = None):
    lastTime = time.time()
    t = 0
    with open('{0}'.format(univ_file), 'r') as openfile:
        json_data = json.load(openfile)
        for univ in json_data['data']:
            departCode = univ['code']
            departName = univ['name']
            t+= getMajorClass2(departCode,
                          index+t,
                          year, season,withSyllabus, forTest,departName,univName)
        print('done!')
        print('elapsed time : {}ms'.format(round((time.time()-lastTime)*1000)))
    return t

# 모든 전공 과목 조회
def getAllMajorClasses(year=2022, season=0,withSyllabus= False,forTest=None):
    t = 0
    for f in os.listdir('./UnivMajor/{}/{}'.format(str(year), str(season))):
        if f[0] != 'u':
            continue
        print('Getting Lectures from "/UnivMajor/' + f + '"')
        Path('./jsons').mkdir(exist_ok=True)
        t+=getMajorClassesInUnivAlt(t,Path('./UnivMajor/{}/{}/'.format(str(year), str(season)) + f),
                              f.split('_')[1].split('.')[0], year, season,withSyllabus,forTest)


def getAllGEClasses(year=2022, season=0, withSyllabus = False, forTest = None):
    index = 0
    print('')
    Path('./jsonsge').mkdir(exist_ok=True)
    index += getGEClass2(index,'./UnivGE/첨성인기초.json', 2022, 0,withSyllabus, forTest,'첨성인기초')

    print('첨성인핵심인문.json')
    index += getGEClass2(index, './UnivGE/첨성인핵심인문.json', 2022, 0,withSyllabus, forTest,'첨성인핵심_인문사회')

    print('첨성인핵심자연.json')
    index += getGEClass2(index, './UnivGE/첨성인핵심자연.json', 2022, 0,withSyllabus, forTest,'첨성인핵심_자연과학')

    print('첨성인소양.json')
    index += getGEClass2(index, './UnivGE/첨성인소양.json', 2022, 0,withSyllabus, forTest,'첨성인소양')

    print('done!')