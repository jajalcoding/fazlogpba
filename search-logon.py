import http.client
import mimetypes
import os,ssl
import json
import sys
import pdb

# just to ignore cert ssl
# export PYTHONHTTPSVERIFY=0
# find log with 'auth-logon' from event log
# note -> Postman use false meanwhile Python use False , so make sure change this !
# just to ignore cert ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

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
      "filter": "action='auth-logon' or action='auth-logout'",
      "logtype": "event",
      "time-order": "desc",
      "time-range": {
        "end": "2020-12-31T17:16:35",
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
strfinal = strpayload.replace("\\\\","\\")
conn.request("POST", "/jsonrpc", strfinal, headers)
res = conn.getresponse()
data = res.read()
print(data)

# write tid to a file
dictdata=eval(data)
print ("TID for search is "+str(dictdata['result']['tid']))
file1 = open("auth-tid.txt","w")
file1.write(str(dictdata['result']['tid']))
file1.close
pdb.set_trace()


