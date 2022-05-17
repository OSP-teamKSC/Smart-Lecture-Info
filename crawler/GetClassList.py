import json
import requests
import os
from pathlib import Path

crawlURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectItttnCdListLectPlnInqr'
crawlLectureURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInqr/selectListLectPlnInqr'

seasons = ['CMBS001400001',  # 1
           'CMBS001400004',  # summer
           'CMBS001400002',  # 2
           'CMBS001400003']  # winter

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
def getMajorClass(depart_code, file_name, year=2022, season=0):
    getMajorClassPayload['search']['estblDprtnCd'] = depart_code
    getMajorClassPayload['search']['estblYear'] = str(year)
    getMajorClassPayload['search']['estblSmstrSctcd'] = seasons[season]
    request = json.dumps(getMajorClassPayload)
    response = requests.post(crawlLectureURL, request, headers=requestHeader)

    if response.status_code >= 400:
        print('failed to get file')
        return
    with open('./{0}.json'.format(file_name), 'w') as savefile:
        json.dump(response.json(), savefile, indent=4)
    print('.', end='')


# 대학 전공 과목 조회
def getMajorClassesInUniv(univ_file, univ_name, year=2022, season=0):
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
                          Path('Classes/Major/{0}/{1}/{2}/{3}'.format(str(year), str(season), univ_name, departName)),year,season)
        print('done!')


# 모든 전공 과목 조회
def getAllMajorClasses(year=2022, season=0):
    for f in os.listdir('./UnivMajor/{}/{}'.format(str(year), str(season))):
        if f[0] != 'u':
            continue
        print('Getting Lectures from "/UnivMajor/' + f + '"')
        Path('./Classes').mkdir(exist_ok=True)
        Path('./Classes/' + f.split('_')[1].split('.')[0]).mkdir(exist_ok=True)
        getMajorClassesInUniv(Path('./UnivMajor/{}/{}/'.format(str(year), str(season)) + f), f.split('_')[1].split('.')[0], year, season)

    # --JSON files save directory--
    # ./UnivMajor/Year/Season
    # ./Classes/Major/Year/Season
    # ./Classes/GE/Year/Season

    # getUnivList() -> getAllDepartments() -> getAllMajorClasses()