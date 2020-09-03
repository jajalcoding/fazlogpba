import http.client
import mimetypes
import os,ssl
import pdb
import json

# just to ignore cert ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

def search_pba():
    file1=open('sessionid.txt','r')
    x=file1.read()
    file1.close()
    payloaddict2 = {
      "id": "tas-search-pba",
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
          "filter": "action='pba-create'",
          "logtype": "event",
          "time-order": "desc",
          "time-range": {
            "end": "2020-08-01T17:16:35",
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

    payloaddict2['session']=x

    # still have issue because when posting, it looks like \ become \\
    conn = http.client.HTTPSConnection(FAZURL)
    strpayload=str(payloaddict2)
    strfinal=strpayload.replace("\\\\","\\")

    conn.request("POST", "/jsonrpc", strfinal, headers)
    res = conn.getresponse()
    data = res.read()
    print(data)

    # write tid to a file
    dictdata=eval(data)
 #   print "TID for search is "+str(dictdata['result']['tid'])
    file1 = open("pba-tid.txt","w")
    file1.write(str(dictdata['result']['tid']))
    file1.close



def get_pba():
    # open previous file auth-tid.txt
    file1=open('pba-tid.txt','r')
    authtid=file1.read()
    file1.close
    file1=open('sessionid.txt','r')
    x=file1.read()
    file1.close()

    headers = {
      'Content-Type': 'text/plain'
    }

    # still have issue because when posting, it looks like \ become \\
    conn = http.client.HTTPSConnection(FAZURL)
  
    payloaddict2={
      "id": "tas-search-pba",
      "jsonrpc": "2.0",
      "method": "get",
      "params": [
        {
          "apiver": 3,
          "url": "/logview/adom/root/logsearch/"
        }
      ],
      "session": "xx"
    }
    payloaddict2['session']=x
    payloaddict2['params'][0]['url']="/logview/adom/root/logsearch/"+str(authtid)
    #print(payloaddict2['params'][0]['url'])

    strpayload=str(payloaddict2)
    strfinal=strpayload.replace("\\\\","\\")

    conn.request("POST", "/jsonrpc", strfinal, headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)
    dataku=eval(data)
    return dataku
    #print(dataku)

def find_logon_time(ipsearch,timesearch):
      # step 1 - search and get the tid
      file1=open('sessionid.txt','r')
      x=file1.read()
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

      payloaddict2['session']=x
      payloaddict2['params'][0]['filter']=payloaddict2['params'][0]['filter']+" and srcip='"+ipsearch+"'"
      payloaddict2['params'][0]['time-range']['end']=timesearch
      conn = http.client.HTTPSConnection(FAZURL)
      strpayload = json.dumps(payloaddict2)
      strfinal=strpayload.replace("\\\\","\\")
      conn.request("POST", "/jsonrpc", strfinal, headers)
      res = conn.getresponse()
      data = res.read()
      #print(data)
      dictdata = eval(data)
      tidsearch = str(dictdata['result']['tid'])
      #print('tid is '+tidsearch)

      # step 2 - get the data from tid
      # limit : 1, just get the biggest time and descending, limit = 1 
      payloaddict3={
        "id": "tas-search-auth-logon",
        "jsonrpc": "2.0",
        "method": "get",
        "params": [
          {
            "apiver": 3,
            "limit": 1,
            "url": "/logview/adom/root/logsearch/"
          }
        ],
        "session": "xx"
      }

      payloaddict3['session']=x
      payloaddict3['params'][0]['url']="/logview/adom/root/logsearch/"+str(tidsearch)
      #print(payloaddict2['params'][0]['url'])
      strpayload = json.dumps(payloaddict3)
      strfinal=strpayload.replace("\\\\","\\")


      conn.request("POST", "/jsonrpc", strfinal, headers)
      res = conn.getresponse()
      data = res.read()
      dataku=eval(data)
      if (dataku['result']['return-lines']>0):
          timelogin=dataku['result']['data'][0]['itime']
      else:
          timelogin=''

      # step 3 - if return-lines > 0 , so search step 2 is found, then let's see if that user have a logged out time, or not ?
      # search first
      # after we get the logged in time in step 2, then will use that time as a start in this query
      # so the query starttime=timelogin endtime must be maximum 
      if (dataku['result']['return-lines']>0):
              payloaddict4 = {
                "id": "tas-search-logout",
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
                    "filter": "action='auth-logout'",
                    "logtype": "event",
                    "time-order": "desc",
                    "time-range": {
                      "end": "2020-09-05T17:16:35",
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

              payloaddict4['session']=x
              payloaddict4['params'][0]['filter']=payloaddict4['params'][0]['filter']+" and srcip='"+ipsearch+"'"
              payloaddict4['params'][0]['time-range']['start']=timelogin
              
              conn = http.client.HTTPSConnection(FAZURL)
              strpayload = json.dumps(payloaddict4)
              strfinal=strpayload.replace("\\\\","\\")

              conn.request("POST", "/jsonrpc", strfinal, headers)
              res = conn.getresponse()
              data = res.read()
              #print(data)
              dictdata = eval(data)
              tidsearch = str(dictdata['result']['tid'])
              #print('tid is '+tidsearch)
      
              payloaddict5={
                "id": "tas-search-auth-logon",
                "jsonrpc": "2.0",
                "method": "get",
                "params": [
                  {
                    "apiver": 3,
                    "limit": 1,
                    "url": "/logview/adom/root/logsearch/"
                  }
                ],
                "session": "xx"
              }

              payloaddict5['session']=x
              payloaddict5['params'][0]['url']="/logview/adom/root/logsearch/"+str(tidsearch)
              #print(payloaddict2['params'][0]['url'])

              strpayload = json.dumps(payloaddict5)
              strfinal=strpayload.replace("\\\\","\\")

              conn.request("POST", "/jsonrpc", strfinal, headers)
              res = conn.getresponse()
              data = res.read()
              datalogout=eval(data)
              if (datalogout['result']['return-lines']>0):
                  timelogout=datalogout['result']['data'][0]['itime']
#                  print(datalogout)
              else:
# meaning never logout
                  timelogout=''
#              pdb.set_trace()


              # step 4
              # logged in and logged out data is completed
              dataku['timelogout']=timelogout
      else:
              dataku['timelogout']=''

      return(dataku)



# main start
# assume login from other module
# assume search_pba will result tid
FAZURL = "54.254.145.25"

print("SEARCH PBA - must login first\n")
search_pba()
print("GET PBA with tid\n")
dataku=get_pba()

for dataitem in dataku['result']['data']:
#  from faz datetime is "2020-07-05T17:16:35" - ISO 8601 ?
  datacari=find_logon_time(dataitem['saddr'],dataitem['itime'])
#  pdb.set_trace()
  if (datacari['result']['return-lines']>0) :
#      print (dataitem['itime']+" "+dataitem['saddr']+" "+dataitem['nat']+" "+dataitem['portbegin']+" "+dataitem['portend']+" "+datacari['result']['data'][0]['user']+"-"+datacari['result']['data'][0]['srcip']+" logged in time:"+datacari['result']['data'][0]['itime'])
      if ( dataitem['itime']>datacari['timelogout'] ):
          if ( datacari['timelogout'] != '' ):
              print (dataitem['itime']+" "+dataitem['saddr']+" "+dataitem['nat']+" "+dataitem['portbegin']+" "+dataitem['portend']+" "+datacari['result']['data'][0]['user']+" login:"+datacari['result']['data'][0]['itime']+" logout: "+datacari['timelogout'] + " ** LAST-KNOWN-LOGON")
          else:
              print (dataitem['itime']+" "+dataitem['saddr']+" "+dataitem['nat']+" "+dataitem['portbegin']+" "+dataitem['portend']+" "+datacari['result']['data'][0]['user']+" login:"+datacari['result']['data'][0]['itime']+" logout: "+datacari['timelogout'] + " ** STILL-LOGON")
      else:
          print (dataitem['itime']+" "+dataitem['saddr']+" "+dataitem['nat']+" "+dataitem['portbegin']+" "+dataitem['portend']+" "+datacari['result']['data'][0]['user']+" login:"+datacari['result']['data'][0]['itime']+" logout: "+datacari['timelogout'])
  else:
      print (dataitem['itime']+" "+dataitem['saddr']+" "+dataitem['nat']+" "+dataitem['portbegin']+" "+dataitem['portend']+" USER NOT FOUND")



