import json
import requests

requestHeader = {'Content-Type': 'application/json'}
requestURL = 'https://knuin.knu.ac.kr/public/web/stddm/lsspr/syllabus/lectPlnInputDtl/selectListLectPlnInputDtl'

def LoadClassSyllabus(year,season,sbjetCd,sbjetDvnno,lctreLnggeSctcd,estblDprtnCd,doPlan = "Kor",forTest = None):
    if lctreLnggeSctcd == None:
        lctreLnggeSctcd = str(season).replace('CMBS','STCU')
    payload = {
      "search": {
        "estblYear": year,
        "estblSmstrSctcd": season,
        "sbjetCd": sbjetCd,
        "sbjetDvnno": sbjetDvnno,
        "lctreLnggeSctcd": lctreLnggeSctcd,
        "doPlan": doPlan,
        "estblDprtnCd": estblDprtnCd,
        "readOnlyYn": "Y",
        "isApi": "Y"
      }
    }

    request = json.dumps(payload)
    for i in range(0,5):
        try:
            response = requests.post(requestURL, request, headers=requestHeader)
        except requests.exceptions.ConnectionError:
            if i == 4:
                print('Connection Failed')
                return None
            print('Connection Error, Retrying... {}/{}'.format(i + 1, 5))
            continue
        break

    if(forTest):
        forTest(len(response.content)/1024)
    if response.status_code >= 400:
        print('failed to get file : no response')
        return
    if response.json()['data'] == None or len(response.json()['data']) == 0:
        if lctreLnggeSctcd == 'STCU001400001':
            print('failed to get file : no data')
            return None
        return LoadClassSyllabus(year, season, sbjetCd, sbjetDvnno, 'STCU001400001', estblDprtnCd, doPlan="Kor", forTest=None)
    return response.json()['data']

