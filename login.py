import http.client
import mimetypes
import os

# just to ignore cert ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
# export PYTHONHTTPSVERIFY=0
# using all hardcoded URL, user and pass, login to FAZ

conn = http.client.HTTPSConnection("54.254.145.25")
payloaddict = {
  "method": "exec", "params": [
 {
   "data": {
   "user": "apiuser",
   "passwd": "password123", },
   "url": "/sys/login/user" }
] 
}	
headers = {
  'Content-Type': 'text/plain'
}

while True:
  conn.request("POST", "/jsonrpc", str(payloaddict), headers)
  res = conn.getresponse()
  data = res.read()
  # print(data.decode("utf-8"))
  x=eval(data);
  sessionid=x['session'];
  print(sessionid)
  if ('\\' not in sessionid) :
    break

# above is a trick temporary to make sure we get session id without character \
# unsafe way, just for poc to get the session
print("Session to use next is "+sessionid);

# write session for next use
file1 = open("sessionid.txt","w")
file1.write(sessionid)
file1.close

