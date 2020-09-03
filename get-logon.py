import http.client
import mimetypes
import os,ssl
import pdb

# just to ignore cert ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

# open previous file auth-tid.txt
file1=open('auth-tid.txt','r')
authtid=file1.read()
file1.close

file1=open('sessionid.txt','r')
sessionid=file1.read()
file1.close()

headers = {
  'Content-Type': 'text/plain'
}

# still have issue because when posting, it looks like \ become \\
conn = http.client.HTTPSConnection("54.254.145.25")

payloaddict2={
  "id": "tas-search-auth-logon",
  "jsonrpc": "2.0",
  "method": "get",
  "params": [
    {
      "apiver": 3,
      "url": "/logview/adom/root/logsearch/",
      "limit": 1000
    }
  ],
  "session": "xx"
}

payloaddict2['session']=sessionid
payloaddict2['params'][0]['url']="/logview/adom/root/logsearch/"+str(authtid)
#print(payloaddict2['params'][0]['url'])
strfinal=str(payloaddict2).replace("\\\\","\\")
conn.request("POST", "/jsonrpc", strfinal, headers)
res = conn.getresponse()
data = res.read()
#print(data)
dataku=eval(data)


for dataitem in dataku['result']['data']:
  print (dataitem['itime']+" "+dataitem['srcip']+" "+dataitem['user']+" "+dataitem['action'])
#pdb.set_trace()

