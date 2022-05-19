import json
import requests
import os
import GetClassSyllabus
from pathlib import Path


def ConvertJSON(j):
    if j['data'] is None:
        print('No Data.')
        return
    js = []
    for t in j['data']:
        js.append({
            'SubjectName': t['sbjetNm'],
            'SubjectCode': t['sbjetCd'],
            'ClassCode': t['crseNo'],
            'ClassDivideNumber': t['sbjetDvnno'],
            'EstablishedUniversity': t['estblUnivNm'],
            'EstablishedDepartment': t['estblDprtnNm'],
            'ProfessorNames': t['totalPrfssNm'],
            'Season': t['estblSmstrSctnm'],
            'ApplicantsMax': t['appcrCnt'],
            'ApplicantsCurrent': t['attlcPrscpCnt'],
            'IsUntact': 'Y' if t['lctreMthodNm'] == '비대면' else 'N',
            'Schedule': t['lssnsTimeInfo']})

    return js


def ConvertJSON(j, withSyllabus=False,forTest = None):
    if j['data'] is None:
        print('No Data.')
        return
    js = []
    for t in j['data']:
        js.append({
            'SubjectName': t['sbjetNm'],  # 과목 명
            'SubjectCode': t['sbjetCd'],  # 과목 코드
            'ClassCode': t['crseNo'],  # 과목 코드 (분반 포함)
            'ClassDivideNumber': t['sbjetDvnno'],  # 분반
            'EstablishedUniversity': t['estblUnivNm'],  # 개설 대학
            'EstablishedDepartment': t['estblDprtnNm'],  # 개설 학과
            'ProfessorNames': t['totalPrfssNm'],  # 교수명 (배열 형식임)
            'Season': t['estblSmstrSctnm'],  # 개설 학기
            'ApplicantsMax': t['appcrCnt'],  # 수강 총원
            'ApplicantsCurrent': t['attlcPrscpCnt'],  # 수강 인원
            'IsUntact': 'Y' if t['lctreMthodNm'] == '비대면' else 'N',  # 비대면 여부
            'Schedule': t['lssnsTimeInfo'],  # 시간표 (배열 형식임)
            'Credit': t['crdit']})  # 학점
        if (withSyllabus == True):
            t2 = GetClassSyllabus.LoadClassSyllabus(t['estblYear'], 'CMBS001400001', t['sbjetCd'], t['sbjetDvnno'],
                                                    t['lctreLnggeSctcd'], t['estblDprtnCd'],t['doPlan'],forTest)

            # 성적 비중
            js[len(js) - 1]['Rate1'] = t2['oriEvltnRate1']  # 출석 비중
            js[len(js) - 1]['Rate2'] = t2['oriEvltnRate2']  # 중간 시험
            js[len(js) - 1]['Rate3'] = t2['oriEvltnRate3']  # 기말 시험
            js[len(js) - 1]['Rate4'] = t2['oriEvltnRate4']  # 과제
            js[len(js) - 1]['Rate5'] = t2['oriEvltnRate5']  # 발표
            js[len(js) - 1]['Rate6'] = t2['oriEvltnRate6']  # 토론
            js[len(js) - 1]['Rate7'] = t2['oriEvltnRate7']  # 안전교육
            js[len(js) - 1]['Rate8'] = t2['oriEvltnRate8']  # 기타
            js[len(js) - 1]['Rate9'] = t2['oriEvltnRate9']  # ?
            js[len(js) - 1]['PriorSubject'] = t2['oriRcmmdPlrSbjetInfo']         # 권장선수과목
            js[len(js) - 1]['SubsequentSubject'] = t2['oriRcmmdSbstsSbjetInfo']  # 권장후수과목

    return js
