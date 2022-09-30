import requests
import json 
import random 
import time

url_querycourse = "https://querycourse.ntust.edu.tw/querycourse/api/courses"
EventName = "stockLINE"
key = ""

CourseNo = input("CourseNo:")
payload = {"Semester": "1082","CourseNo": CourseNo,"CourseName": "","CourseTeacher": "","Dimension": "","CourseNotes": "","ForeignLanguage": 0,"OnlyGeneral": 0,"OnleyNTUST": 0,"OnlyMaster": 0,"OnlyUnderGraduate": 0,"OnlyNode": 0,"Language": "zh"}
#request
while(True):
	localtime = time.asctime( time.localtime(time.time()) )
	print(localtime + " requests post ::" + url_querycourse)
	req = requests.post(url_querycourse,data=payload)
	data=req.text
	data=json.loads(data)
	available = int(data[0]["AllStudent"]) - int(data[0]["ChooseStudent"])
	if(available > 0):
		value={"value1":data[0]["CourseNo"],
					"value2":data[0]["CourseName"],
					"value3":str( available )}
		url = "https://maker.ifttt.com/trigger/" + EventName + "/with/key/" + key
		print(localtime + " requests post ::" + url)
		print(localtime + " data ::" + data[0]["CourseName"])
		#requests.post(url,data=value)
	time.sleep(random.uniform(1,3))