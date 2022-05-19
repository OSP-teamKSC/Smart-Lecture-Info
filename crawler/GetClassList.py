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


def getAllGEClasses(year=2022, season=0, withSyllabus = False, forTest = None):
    print('')
    Path('./Classes').mkdir(exist_ok=True)
    Path('./Classes/GE').mkdir(exist_ok=True)
    Path('./Classes/GE/{}'.format(str(year))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}'.format(str(year), str(season))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}/첨성인기초'.format(str(year), str(season))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}/첨성인소양'.format(str(year), str(season))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}/첨성인핵심'.format(str(year), str(season))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}/첨성인핵심/인문_사회'.format(str(year), str(season))).mkdir(exist_ok=True)
    Path('./Classes/GE/{}/{}/첨성인핵심/자연과학'.format(str(year), str(season))).mkdir(exist_ok=True)
    print('첨성인기초.json')
    getGEClass('./UnivGE/첨성인기초.json', 'Classes/GE/{}/{}/첨성인기초'.format(str(year), str(season)), 2022, 0,withSyllabus, forTest)

    print('첨성인핵심인문.json')
    getGEClass('./UnivGE/첨성인핵심인문.json', 'Classes/GE/{}/{}/첨성인핵심/인문_사회'.format(str(year), str(season)), 2022, 0,withSyllabus, forTest)

    print('첨성인핵심자연.json')
    getGEClass('./UnivGE/첨성인핵심자연.json', 'Classes/GE/{}/{}/첨성인핵심/자연과학'.format(str(year), str(season)), 2022, 0,withSyllabus, forTest)

    print('첨성인소양.json')
    getGEClass('./UnivGE/첨성인소양.json', 'Classes/GE/{}/{}/첨성인소양'.format(str(year), str(season)), 2022, 0,withSyllabus, forTest)

    print('done!')


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


# 교양 과목 조회
def getGEClasses():
    request = json.dumps(getGEClassPayload)
    response = requests.post(crawlLectureURL, request, headers=requestHeader)

    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    with open('./Classes/general_elective.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)


# 전공 과목 조회
def getMajorClass(depart_code, file_name, year=2022, season=0,withSyllabus = False,forTest = None):
    getMajorClassPayload['search']['estblDprtnCd'] = depart_code
    getMajorClassPayload['search']['estblYear'] = str(year)
    getMajorClassPayload['search']['estblSmstrSctcd'] = seasons[season]
    request = json.dumps(getMajorClassPayload)
    response = requests.post(crawlLectureURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file : no response')
        return
    if len(response.json()['data']) == 0:
        print('failed to get file : no data')
        return
    if(forTest):
        forTest(len(response.content)/1024)
    with open('./{0}.json'.format(file_name), 'w') as savefile:
        json.dump(ClassJsonConverter.ConvertJSON(response.json(),withSyllabus,forTest), savefile, indent=4)
    print('.', end='')


# 교양 과목 조회
def getGEClass(openfile, savepath, year=2022, season=0, withSyllable = False, forTest = None):
    lastTime = time.time()
    with open(openfile, 'r') as readfile:
        for sub in json.load(readfile)['data']['option']['codes']:
            code = sub['codeId']
            name = sub['codeNm']
            path = Path('{}/{}'.format(savepath,name))
            getGEClassPayload['search']['sbjetRelmCd'] = code
            getGEClassPayload['search']['estblYear'] = str(year)
            getGEClassPayload['search']['estblSmstrSctcd'] = seasons[season]
            request = json.dumps(getGEClassPayload)
            response = requests.post(crawlLectureURL, request, headers=requestHeader)

            if response.status_code >= 400:
                print('failed to get file : no response')
                return
            if len(response.json()['data']) == 0:
                print('failed to get file : no data')
                return
            if forTest:
                forTest(len(response.content)/1024)
            with open('./{0}.json'.format(path), 'w') as savefile:
                json.dump(ClassJsonConverter.ConvertJSON(response.json(), withSyllable, forTest), savefile, indent=4)
            print('.', end='')
        print('done!')
        print('elapsed time : {}ms'.format(round((time.time()-lastTime)*1000)))


# 대학 전공 과목 조회
def getMajorClassesInUniv(univ_file, univ_name, year=2022, season=0,withSyllabus = False, forTest = None):
    lastTime = time.time()
    with open('{0}'.format(univ_file), 'r') as openfile:
        json_data = json.load(openfile)
        for univ in json_data['data']:
            departCode = univ['code']
            departName = univ['name']
            departName = departName.replace('\\', '_')  # '/' 가 포함된 전공명이 경로값와 충돌이 발생, '_' 로 교체
            departName = departName.replace('/', '_')
            Path('./Classes/Major'.format(univ_name)).mkdir(exist_ok=True)
            Path('./Classes/Major/{}'.format(str(year))).mkdir(exist_ok=True)
            Path('./Classes/Major/{}/{}'.format(str(year), str(season))).mkdir(exist_ok=True)
            Path('./Classes/Major/{0}/{1}/{2}'.format(str(year), str(season), univ_name)).mkdir(exist_ok=True)
            getMajorClass(departCode,
                          Path('Classes/Major/{0}/{1}/{2}/{3}'.format(str(year), str(season), univ_name, departName)),
                          year, season,withSyllabus, forTest)
        print('done!')
        print('elapsed time : {}ms'.format(round((time.time()-lastTime)*1000)))


# 모든 전공 과목 조회
def getAllMajorClasses(year=2022, season=0,withSyllabus= False,forTest=None):
    for f in os.listdir('./UnivMajor/{}/{}'.format(str(year), str(season))):
        if f[0] != 'u':
            continue
        print('Getting Lectures from "/UnivMajor/' + f + '"')
        Path('./Classes').mkdir(exist_ok=True)
        getMajorClassesInUniv(Path('./UnivMajor/{}/{}/'.format(str(year), str(season)) + f),
                              f.split('_')[1].split('.')[0], year, season,withSyllabus,forTest)
