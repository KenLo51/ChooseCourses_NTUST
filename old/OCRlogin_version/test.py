import requests
import json 

def GetCourseList(UserName , Password):
	Courses = []
	headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
	session = requests.Session()
	session.post('https://querycourse.ntust.edu.tw/querycourse/api/login',headers=headers,data = {"Account":UserName,"Password":Password,"Language":"zh-tw"})
	sleep(1)
	req = session.get('https://querycourse.ntust.edu.tw/querycourse/api/course',headers=headers)
	text = req.text
	li =text.split('<SelectCourseDTO>')
	del li[0]
	i=0
	for course_str in li:
		data = {}
		data["CourseName"] = course_str[course_str.find('<CourseName>')+12 : course_str.find('</CourseName>')] 
		data["CourseNo"] = course_str[course_str.find('<CourseNo>')+10 : course_str.find('</CourseNo>')] 
		Courses.append( data )
		i = i + 1
	return(Courses)
	session.close()

def GetCourseData(CourseNo):
	payload = {"Semester": "1082","CourseNo": CourseNo,"CourseName": "","CourseTeacher": "","Dimension": "","CourseNotes": "","ForeignLanguage": 0,"OnlyGeneral": 0,"OnleyNTUST": 0,"OnlyMaster": 0,"OnlyUnderGraduate": 0,"OnlyNode": 0,"Language": "zh"}
	req = requests.post(url_querycourse,data=payload)
	data=req.text
	data=json.loads(data)
	return data

