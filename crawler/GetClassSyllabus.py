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
    response = requests.post(requestURL, request, headers=requestHeader)
    if(forTest):
        forTest(len(response.content)/1024)
    if response.status_code >= 400:
        print('failed to get file : no response')
        return
    if len(response.json()['data']) == 0:
        print('failed to get file : no data')
        return
    return response.json()['data']

