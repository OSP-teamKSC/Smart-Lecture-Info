import json
import os
UnivList = ['인문대학', '사회과학대학', '자연과학대학', '경상대학', '공과대학', '농업생명과학대학', '예술대학', '사범대학', '수의과대학', '생활과학대학', '간호대학', '자율전공부', '의과대학', '치과대학', 'IT대학', '약학대학', '행정학부', '융합학부', '[상주캠퍼스]생태환경대학', '[상주캠퍼스]과학기술대학']

def getMajor(year, season):
    Dict = {}
    if not os.path.isdir('../crawler/UnivMajor/{}/{}'.format(year, season)):
        return Dict

    for univ in UnivList:
        if not os.path.isfile('../crawler/UnivMajor/{}/{}/univ_{}.json'.format(year, season, univ)):
            continue
        with open('../crawler/UnivMajor/{}/{}/univ_{}.json'.format(year, season, univ), 'r') as openfile:
            json_data = json.load(openfile)
            depas = json_data['data']
            depalist = []
            for depa in depas:
                depalist.append(depa['name'])

        Dict[univ] = depalist
    return Dict
