#!/usr/bin/python3

import os
import time
import json
import requests
from requests.auth import HTTPBasicAuth

db_name = os.getenv("DB_NAME")

url = "http://127.0.0.1:3000"
usr = "admin"
pwd = "admin"
api = "/api/datasources"
JSON_Data = {"name": "Smart Campus", "type": "influxdb",
             "access": "proxy", "url": "http://influxdb:8086",
             "password": "", "user": "",
             "database": db_name, "basicAuth": False, "isDefault": True,
             "jsonData": {"keepCookies": []}, "readOnly": False}
             
code=-1
while code != 200:
  try:
    r = requests.post(url + api, auth=HTTPBasicAuth(usr, pwd), json=JSON_Data, timeout=3)
    code = r.status_code
  except:
    time.sleep(3)
    print("Waiting influxdb...")
  
print(r.content)

api="/api/dashboards/db"
JSON_Data = {"dashboard":json.loads(open("dashboard.json").read()),
            "folderId":0,
            "overwrite": True}
JSON_Data['dashboard']['id']=None
r = requests.post(url + api, auth=HTTPBasicAuth(usr, pwd), json=JSON_Data)
print(r.content)

url = "http://127.0.0.1:8081"
usr = "admin"
pwd = "public"
api = "/api/v4/resources"
JSON_Data = {"type": "web_hook", "description": "InfluxDB",
             'config': {"url": "http://influxdb:8086/write?db=smart&precision=s",
                        "method": "POST",
                        "headers": []}}
code=-1
while code != 200:
  try:
    r = requests.post(url + api, auth=HTTPBasicAuth(usr, pwd), json=JSON_Data, timeout=3)
    code = r.status_code
  except:
    time.sleep(3)
    print("Waiting emqx...")
  
resource = json.loads(r.content)
print(r.content)

api = "/api/v4/rules"
JSON_Data = {"rawsql": "SELECT\n  "
                       "nth(1, split(topic,'/')) as node,\n  "
                       "nth(2, split(topic,'/')) as sensor,\n  "
                       "payload.measure.unit as unit,\n  "
                       "payload.measure.value as value,\n  "
                       "payload.timestamp as ts\n"
                       "FROM\n  "
                       "\"+/+\""}
params = {"payload_tmpl": "air,node=${node},sensor=${sensor} value=${value},unit=\"${unit}\" ${ts}",
          "$resource": resource['data']['id']}
JSON_Data['actions'] = [{"params": params, "name": "data_to_webserver"}]
r = requests.post(url + api, auth=HTTPBasicAuth(usr, pwd), json=JSON_Data)
print(r.content)

