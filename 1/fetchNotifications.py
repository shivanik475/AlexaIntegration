import logging
import os
import requests
import json
from logging.handlers import RotatingFileHandler

def getLoginToken():
	APIURL = 'https://acrobatjstestresults.corp.adobe.com/dashboard/api/getAuthToken.php';
	result = sendRequest(APIURL , {} , {} );
	#print(result);
	return (result);
	
def sendRequest(url , header , data1 , method='GET'):
	response =  requests.post(url, json=data1, headers=header);
	
	jsonData = response.text;
	#print(jsonData)
	return jsonData;
	
def fetchNotifications(token):
	url = 'https://notify-stage.adobe.io/ans/v2/notifications/search'
	args = {"locale":"en_US","criteria":
    {"AND":[{"OR":[{"AND":[{"field":"type","value":"com.adobe.behance.v1","operator":"EQ"},{"field":"sub-type","value":"invitation.coown.project","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.behance.v1","operator":"EQ"},{"field":"sub-type","value":"invitation.coown.collection","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.stormcloud.v1","operator":"EQ"},{"field":"sub-type","value":"sharing.invite","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.designlibrary.v1","operator":"EQ"},{"field":"sub-type","value":"sharing.invite","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.anywhere.production.v1","operator":"EQ"},{"field":"sub-type","value":"sharing.invite","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.accp.review.v1","operator":"EQ"},{"field":"sub-type","value":"activity.inform.review.deadline_reminder.version1","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.dc.sendandtrack.v1","operator":"EQ"},{"field":"sub-type","value":"parcel.completed","operator":"EQ"}]},
    {"AND":[{"field":"type","value":"com.adobe.spark.v1","operator":"EQ"},{"field":"sub-type","value":"sharing.invite","operator":"EQ"}]}]},
    {"field":"state","value":"EXPIRED","operator":"NE"}]}}
	#print(token);
	
	header = {
	    'Authorization': 'Bearer ' + token,
	    'x-adobe-app-id': 'dc-web-app',
	    'x-api-key': 'dc-stage-virgoweb',
	    #'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
	   # 'Origin': 'https://dc.stage.acrobat.com',
       #'Accept': 'application/json',
       # 'Content-Type':'application/json',
	   # 'Sec-Fetch-Site': 'cross-site',
	   # 'Sec-Fetch-Mode': 'cors',
	   # 'Sec-Fetch-Dest': 'empty',
	    #'Referer': 'https://dc.stage.acrobat.com/',
	    #'Accept-Language': 'en-US,en;q=0.9',
	   # 'Connection': 'keep-alive',
        #'Content-length':'1279',
        #'Accept-Encoding':'gzip, deflate'
	}
	
	resp = sendRequest(url , header , args , 'Post');
	return resp;
    
## Create Logger object

log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
dir_path = os.path.dirname(os.path.realpath(__file__))
logFile = dir_path+'/logs/log.txt'
my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024*1024, backupCount=20, encoding=None, delay=0)
my_handler.setFormatter(log_formatter)
my_handler.setLevel(logging.INFO)
app_log = logging.getLogger('root')
app_log.setLevel(logging.INFO)
app_log.addHandler(my_handler)
	
app_log.info("Fetching Login Token");
token = getLoginToken();
notifications = fetchNotifications(token);
#print(notifications);
with open('notifications.txt','w') as outfile:
    outfile.write(notifications.replace("\\n",""))
exit();