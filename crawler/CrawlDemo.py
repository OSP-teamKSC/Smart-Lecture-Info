import json
import GetClassList


# json 파일 조회 및 출력
def ReadSchedule(path):
    classes = []
    with open(path, 'r') as openfile:
        json_data = json.load(openfile)
        for cls in json_data['data']:
            dic = {}
            if cls['lssnsTimeInfo'] != None:
                t = (cls['lssnsTimeInfo']).split('<br/>')
                sche = []
                for i in t:
                    i0 = i.split(' ')
                    sche.append((i0[0], i0[1].split(',')))
                    dic['sche'] = sche
            else:
                dic['sche'] = None
            dic['name'] = cls['sbjetNm']
            dic['professor'] = cls['totalPrfssNm']
            classes.append(dic)
    for c in classes:
        print('[{0}]'.format(c['name']))
        if c['professor'] != '':
            print('교수 : {0}'.format(c['professor'].split('<br/>')))
        if c['sche'] != '':
            print('시간표 : {0}'.format(c['sche']), end='\n\n')


if __name__ == '__main__':
    GetClassList.getAllDepartments(2022, 1)
    GetClassList.getAllMajorClasses(2022, 1)

    # --JSON files save directory--
    # ./UnivMajor/(Year)/(Season)
    # ./Classes/Major/(Year)/(Season)/(Department)
    # ./Classes/GE/(Year)/(Season)/(SubClass)

    # Execution Order
    # getUnivList() -> getAllDepartments() -> getAllMajorClasses()
