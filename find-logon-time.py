import http.client
import mimetypes
import os
import json
import sys
import pdb

# just to ignore cert ssl
# export PYTHONHTTPSVERIFY=0
# find log with 'auth-logon' from event log
# note -> Postman use false meanwhile Python use False , so make sure change this !

file1=open('sessionid.txt','r')
sessionid=file1.read()
file1.close()

payloaddict2 = {
  "id": "tas-search-auth-logon",
  "jsonrpc": "2.0",
  "method": "add",
  "params": [
    {
      "apiver": 3,
      "case-sensitive": False,
      "device": [
        {
          "devname": "FG60EPTK18005389"
        }
      ],
      "filter": "action='auth-logon'",
      "logtype": "event",
      "time-order": "desc",
      "time-range": {
        "end": "2020-07-05T17:16:35",
        "start": "2020-07-01T17:16:35"
      },
      "url": "/logview/adom/root/logsearch"
    }
  ],
  "session": "xx"
}
headers = { 
  'Content-Type': 'text/plain'
}

payloaddict2['session']=sessionid

# still have issue because when posting, it looks like \ become \\
conn = http.client.HTTPSConnection("54.254.145.25")
strpayload = json.dumps(payloaddict2)

#pdb.set_trace()

conn.request("POST", "/jsonrpc", strpayload, headers)
res = conn.getresponse()
data = res.read()
#print(data)

tidsearch = str(dictdata['result']['tid'])
print('tid is '+tidsearch)

