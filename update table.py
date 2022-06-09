#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
# coding: utf-8


# In[2]:


import getpass
import pymysql as mysqldb
import pandas as pd
import json
import os
import requests
import GetClassList
import time
from pathlib import Path
# connect to MySQL server
mydb = mysqldb.connect(host='osp-db-server.mysql.database.azure.com', user='KSC',
                       passwd='1q2w3e4r@@', db='knubus')
cursor = mydb.cursor()


# In[3]:


folder = './jsons/2022/0/simple'
files = os.listdir(folder)
for file in files:
    with open(folder+file, 'r') as json_file:    
        json_data = json.load(json_file)
        json_line = json_data
        print(len(json_line))

        for i in json_line:
            sql_update = "update 강의 set ApplicantsCurrent = %s where ClassCode = %s"

            try:
                cursor.execute(sql_update, (i[ApplicantsCurrent], i[ClassCode]))
                print("Inserting [%s, %s] to 강의"%(i["SubjectName"], i["ClassCode"])) #업데이트 성공
                
            except mysqldb.IntegrityError:
                print("%s already updated"%(i["ClassCode"])) #이미 업데이트한 값



# In[5]:


mydb.commit()


# In[6]:


cursor.close()
json_file.close()
print("Done")


# In[ ]:




