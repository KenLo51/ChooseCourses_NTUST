import requests
url={  "url_main" : "https://courseselection.ntust.edu.tw/",
		 "url_login" : "https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection",
		 "url_addandsub" : "https://courseselection.ntust.edu.tw/AddAndSub/B01/B01",
		 "url_querycourse" : "https://querycourse.ntust.edu.tw/querycourse/api/courses",
		 "url_coursedetials" : "https://querycourse.ntust.edu.tw/querycourse/api/coursedetials"
}
def GetCourseData(Semester, CourseNo, url="https://querycourse.ntust.edu.tw/querycourse/api/coursedetials"):
	payload = {"semester": Semester,"course_no": CourseNo,"language": "zh"}
	headers = {"cookie": "_ga=GA0.0.0.0; _gid=GA0.0.0.0; _gat_gtag_UA_123456789_1=1 "}
	req = requests.get(url, headers = headers,params=payload)
	data = req.text
	print('data: ',data)
	data=data.replace("null","None")
	data = eval(data)[0]
	return data
def GetCourseAvailable(self,Semester=None,CourseNo=None,data=None):
	if(data == None):
		data = self.GetCourseData(Semester,CourseNo)
	else:
		Semester = data["Semester"]
		CourseNo = data["CourseNo"]
	if((Semester!=None) and (CourseNo!=None)):
		try:
			available = data["limit"] - data["ChooseStudent"]
			print("\n%s-%s：%d / %d"%(data["CourseNo"],data["CourseName"],data["ChooseStudent"],data["limit"]))
			return available
		except:
			print("\nGetCourseData dataErr")
			return None
	return None
def InitAvailable(self,Semester,Course_list):
	new_list=[]
	for Course in Course_list:
		a = self.GetCourseAvailable(Semester,Course)
		new_list.append(a)
	return new_list