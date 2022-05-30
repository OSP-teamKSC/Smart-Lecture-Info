#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8


# In[2]:


import getpass
import pymysql as mysqldb
import math
import pandas as pd
import json
import os
# connect to MySQL server
mydb = mysqldb.connect(host='osp-db-server.mysql.database.azure.com', user='KSC',
                               passwd='1q2w3e4r@@', db='knubus')
cursor = mydb.cursor()


# In[3]:


folder = 'Downloads/jsonsge/'
files = os.listdir(folder)
for file in files:
        with open(folder+file, 'r') as json_file:    
                    json_data = json.load(json_file)
                            json_line = json_data
                                    print(len(json_line))

                                            for i in json_line:
                                                            sql_insert = "insert into 강의 (구분, 과목명, 과목코드, 과목코드_분반포함, 분반, 개설대학, 개설학과, 교수명, 개설학기, 수강총원, 수강인원, 비대면여부, 시간표, 학점, 출석비중, 중간고사, 기말고사, 과제, 발표, 토론, 안전교육, 기타, etc, 권장선수과목, 권장후수과목) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                                                        ts = ''
                                                                                    #시간 구분선 추가
                                                                                                if i['Schedule'] is not None:
                                                                                                                    for index in range(0,len(i['Schedule'])):
                                                                                                                                            if index<len(i['Schedule'])-2 and i['Schedule'][index] == ',' and i['Schedule'][index+2] == ' ':
                                                                                                                                                                        ts += '|'
                                                                                                                                                                                            else:
                                                                                                                                                                                                                        ts += i['Schedule'][index]

                                                                                                                                                                                                                                        i['Schedule'] = ts
                                                                                                                                                                                                                                                    try:
                                                                                                                                                                                                                                                                        cursor.execute(sql_insert,(i["Gubun"],i["SubjectName"],i["SubjectCode"],i["ClassCode"],i["ClassDivideNumber"],i["EstablishedUniversity"],i["EstablishedDepartment"],i["ProfessorNames"],i["Season"],i["ApplicantsMax"],i["ApplicantsCurrent"],i["IsUntact"],i["Schedule"],i["Credit"],i["Rate1"],i["Rate2"],i["Rate3"],i["Rate4"],i["Rate5"],i["Rate6"],i["Rate7"],i["Rate8"],i["Rate9"],i["PriorSubject"],i["SubsequentSubject"]))
                                                                                                                                                                                                                                                                                        print("Inserting [%s, %s] to 강의"%(i["SubjectName"], i["ClassCode"])) #삽입 성공
                                                                                                                                                                                                                                                                                                    except mysqldb.IntegrityError:
                                                                                                                                                                                                                                                                                                                        print("%s already in 강의"%(i["ClassCode"])) #이미 삽입한 값



                                                                                                                                                                                                                                                                                                                        # In[4]:


                                                                                                                                                                                                                                                                                                                        mydb.commit()


                                                                                                                                                                                                                                                                                                                        # In[5]:


                                                                                                                                                                                                                                                                                                                        cursor.close()
                                                                                                                                                                                                                                                                                                                        json_file.close()
                                                                                                                                                                                                                                                                                                                        print("Done")


                                                                                                                                                                                                                                                                                                                        # In[ ]:




