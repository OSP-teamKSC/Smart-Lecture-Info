import json
import requests
import os
from pathlib import Path

crawlURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectItttnCdListLectPlnInqr'
crawlLectureURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectListLectPlnInqr'

# 대학 목록 조회 페이로드
getUnivListPayload = {
    "search": {
        "gubun": "02",
        "code": "02",
        "name": "대학",
        "estblYear": "2022",
        "estblSmstrSctcd": "CMBS001400001",
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
        "estblSmstrSctcd": "CMBS001400004",
        "sbjetCd": "",
        "sbjetNm": "",
        "crgePrfssNm": "",
        "sbjetRelmCd": "01",
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

requestHeader = {'Content-Type': 'application/json'}


# 대학 목록 조회
def getUnivList():
    request = json.dumps(getUnivListPayload)
    response = requests.post(crawlURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    with open('./UnivList.json', 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)


# 전공 목록 조회
def getDepartmentList(univ_name, univ_code, file_name):
    getDepartmentListPayload['search']['code'] = univ_code
    getDepartmentListPayload['search']['name'] = univ_name
    request = json.dumps(getDepartmentListPayload)
    response = requests.post(crawlURL, request, headers=requestHeader)
    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    json_data = response.json()
    if len(json_data['data']) == 0:
        return
        # json_data['data']=[{'estblDprtnCd': univ_code}]
        # print('appended {0}'.format(univ_name))
    with open('./{0}.json'.format(file_name), 'w') as savefile:
        json.dump(json_data, savefile, indent=4)


# 모든 대학의 전공 조회
def getAllDepartments():
    with open('./UnivList.json', 'r') as openfile:
        json_data = json.load(openfile)
        for univ in json_data['data']:
            univCode = univ['code']
            univName = univ['name']
            getDepartmentList(univName, univCode, 'UnivMajor/univ_{0}'.format(univName))


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
def getMajorClass(depart_code, file_name):
    getMajorClassPayload['search']['estblDprtnCd'] = depart_code
    request = json.dumps(getMajorClassPayload)
    response = requests.post(crawlLectureURL, request, headers=requestHeader)

    if response.status_code >= 400:
        print('failed to get file')
        return
    print(response)
    with open('./{0}.json'.format(file_name), 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)

# 대학 전공 과목 조회
def getMajorClassesInUniv(univ_file, univ_name):
    with open('{0}'.format(univ_file), 'r') as openfile:
        json_data = json.load(openfile)
        for univ in json_data['data']:
            departCode = univ['code']
            departName = univ['name']
            departName = departName.replace('\\','_')                   # '/' 가 포함된 전공명이 경로값와 충돌이 발생, '_' 로 교체
            departName = departName.replace('/','_')
            getMajorClass(departCode, Path('Classes\\{0}\\{1}'.format(univ_name, departName)))


# 모든 전공 과목 조회
def getAllMajorClasses():
    for f in os.listdir('./UnivMajor'):
        if f[0]!='u':
            continue
        print('.\\UnivMajor\\'+f)
        Path('.\\Classes\\'+f.split('_')[1].split('.')[0]).mkdir(exist_ok=True)
        getMajorClassesInUniv(Path('.\\UnivMajor\\' + f), f.split('_')[1].split('.')[0])
