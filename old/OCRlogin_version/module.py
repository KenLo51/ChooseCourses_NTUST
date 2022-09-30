from selenium import webdriver	#pip install selenium
from selenium.webdriver.common.keys import Keys	#pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configparser import ConfigParser

#from Cryptodome.Cipher import DES
import binascii

import requests
import PIL.Image as Image	#pip install pillow
from pytesseract	import image_to_string#pip install pytesseract
import cv2	#pip install openCV-python
import numpy

from time import sleep
from json import loads
from sys import exit

def creatConfig(ConfigName = 'Config.ini' , data = {	'UserName':'',
																					'Password':'',
																					'Semester':'1081',
																					'CourseNo':[''],
																					'LineNotify':'',
																					'url_main':"https://courseselection.ntust.edu.tw/",#選課主頁網址
																					'url_login':"https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection",#登入網址
																					'url_AddAndSub':"https://courseselection.ntust.edu.tw/AddAndSub/B01/B01",#加退選網址
																					'url_querycourse':"https://querycourse.ntust.edu.tw/querycourse/api/courses",#課程查詢網址
																					'sleep':'0',
																					'Timeout':'30'}):

	cfg = ConfigParser()
	cfg.write(open('Config.ini','w'))#建立空白ini檔案

	cfg.add_section('UserName')
	cfg.set('UserName','UserName',data['UserName'])
	cfg.set('UserName','Password',data['Password'])

	cfg.add_section('Courses')
	cfg.set('Courses','Semester',data['Semester'])
	n=0
	CourseNo_str = ''
	if(len(data['CourseNo'][0]) > 0 ):
		for CourseNo in data['CourseNo']:
			CourseNo_str= CourseNo_str + ',' + CourseNo
			n = n+1
		CourseNo_str = CourseNo_str[1:len(CourseNo_str)]
	cfg.set('Courses','CourseNo',CourseNo_str)

	cfg.add_section('LineNotify')
	cfg.set('LineNotify','Line_token',data['LineNotify'])

	cfg.add_section('url')
	cfg.set('url','url_main',data['url_main'])
	cfg.set('url','url_login',data['url_login'])
	cfg.set('url','url_AddAndSub',data['url_AddAndSub'])
	cfg.set('url','url_querycourse',data['url_querycourse'])

	cfg.add_section('time')
	cfg.set('time','sleep_time',str(data['sleep']))
	cfg.set('time','Timeout',str(data['Timeout']))
	cfg.write(open(ConfigName,'w'))#寫入ini檔案
	return 0

def readConfig(ConfigName = 'Config.ini'):
	data = {}
	try:
		print('\n--readConfig')
		cfg = ConfigParser()
		cfg.read(ConfigName)
		
		data['UserName'] = cfg['UserName']['UserName']
		data['Password'] = cfg['UserName']['Password']

		data['Semester'] = cfg['Courses']['Semester']
		CourseNo = cfg['Courses']['CourseNo'].split(',')
		data['CourseNo']=CourseNo

		data['LineNotify'] = cfg['LineNotify']['Line_token']
		print('\n--readConfig url')
		data['url_main'] = cfg['url']['url_main']
		data['url_login'] = cfg['url']['url_login']
		data['url_AddAndSub'] = cfg['url']['url_AddAndSub']
		data['url_querycourse'] = cfg['url']['url_querycourse']
		print('\n--readConfig time')
		data['sleep'] = float(cfg['time']['sleep_time'])
		data['Timeout'] = float(cfg['time']['Timeout'])
		return data

	except:
		print('\n--Err Config.ini')
		return data

def writeConfig(ConfigName = 'Config.ini' , data = {}):
	creatConfig(ConfigName , data)

def lineNotifyMessage(token, msg):
	if(len(token) == 0):
		print('\n--lineNotify enable')
		try:
			headers = {
			"Authorization": "Bearer " + token, 
			"Content-Type" : "application/x-www-form-urlencoded"
			}
			payload = {'message': msg}
			requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
			return 0
		except:
			print('\n--lineNotify Err')
			return -1
	else:
		print('\n--lineNotify disable')
		return 1

def getWhiteListing(DES_key , url_getWhiteListing = 'https://drive.google.com/uc?id=1LF0jgOpSFb8W86cuHkI15VkMlJ5nHy91&export=download'):
	try:
		response = requests.get(url_getWhiteListing)
		with open('WhiteListing','wb') as f:
			f.write(response.content)
	except:
		print('\n--request WhiteListing Err')

	try:
		file = open('WhiteListing','rb')
		des = DES.new(DES_key,DES.MODE_ECB)
		e_text = file.read()
		file.close()
		e_text = des.decrypt(binascii.a2b_hex(e_text))
		e_text = e_text.decode('utf-8')
		e_text = e_text[:e_text.find('=')]
		return tuple(e_text.split(','))
	except:
		print('\n--read WhiteListing Err')
		return {}

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
	req = requests.post("https://querycourse.ntust.edu.tw/querycourse/api/courses",data=payload)
	data=req.text
	data=loads(data)
	return data

def login(browser , UserName , Password , url_main="https://courseselection.ntust.edu.tw/" , url_login="https://courseselection.ntust.edu.tw/Account/Login"):
	print("\nlogin")
	VerifyCode = ''
	print("\n"+browser.current_url)
	while(browser.current_url[:len(url_login)] == url_login):#若為登入網址重複嘗試登入
		print("\n--Input_UserName ")
		Input_UserName = browser.find_element_by_name('UserName')#尋找帳號輸入欄位

		for i in range(len(UserName)*2+3):
			Input_UserName.send_keys(Keys.BACKSPACE)#刪除預留文字
			sleep(0.03)

		Input_UserName.send_keys(UserName)#輸入帳號
		print("\n--Input_Password ")
		Input_Password = browser.find_element_by_name('password')#尋找密碼輸入欄位

		for i in range(len(Password)*2+3):
			Input_Password.send_keys(Keys.BACKSPACE)#刪除預留文字
			sleep(0.03)

		Input_Password.send_keys(Password)#輸入密碼
		#Input_VerifyCode = browser.find_element_by_id('VerifyCode')#尋找驗證碼輸入欄位

		#for i in range(len(VerifyCode)*2+3):
		#	Input_VerifyCode.send_keys(Keys.BACKSPACE)#刪除預留文字
		#	sleep(0.03)

		#print("\n--get_cookies ")
		#Cookies_list = browser.get_cookies()
		#Cookies = {}
		#for Cookie in Cookies_list:
		#	Cookies.setdefault(Cookie['name'],Cookie['value'])
		#print(Cookies)#取得cookie用以重新請求驗證碼

		#VerifyCode=''
		#while(True):
		#	print("\n--get VerifyCode")
		#	headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
		#	response = requests.get(url_main+"Account/GetValidateCode",headers=headers,cookies=Cookies,verify=False)#取得驗證碼
		#	print("\n--Saving  VerifyCode ")
		#	#with open('VerifyCode.jpg','wb') as f:
		#	#	f.write(response.content)#輸出驗證碼
		#	nparr = numpy.fromstring(response.content , dtype = 'uint8')
		#	img = cv2.imdecode(nparr , cv2.IMREAD_COLOR)
		#	#img = img[4:16 , 4:75]
		#	#VerifyCode = input('input VerifyCode::')#輸入驗證碼
		#	#img = cv2.imread('VerifyCode.jpg')#開啟驗證碼圖片
		#	dst = cv2.fastNlMeansDenoisingColored(img , None , 30 , 10 , 5 , 27)#去除噪點
		#	#image = Image.fromarray( cv2.cvtColor(img , cv2.COLOR_BGR2RGB) )
		#	image = Image.fromarray( cv2.cvtColor(img , cv2.COLOR_BGR2GRAY) )
		#	VerifyCode = image_to_string(image)#圖片轉字串
			
		#	print("\n VerifyCode::" + str(len(VerifyCode)))
		#	if(len(VerifyCode) == 6):
		#		break
		#	#cv2.imwrite('VerifyCode_f.jpg',dst)#輸出修改後驗證碼圖片
		#	#image = Image.open('VerifyCode_f.jpg')
		

		#Input_VerifyCode.send_keys(VerifyCode)#輸入驗證碼
		print("\n--Login...")
		Btn_login=browser.find_element_by_name("btnLogIn")#尋找登入按鈕
		Btn_login.click()#點擊
	print("\n--Login success!")

def ChooseCourses(data):
	errcnt = 0;
	browser = webdriver.Chrome(executable_path="chromedriver")#開啟瀏覽器
	print("\n--get ::" + data['url_main'])#連線主頁網址 取得cookie(ASP.NET_SessionId)
	browser.get(data['url_main'])
	print("\n--get ::" + data['url_login'])#連線登入網址
	browser.get(data['url_login'])
	login(browser,data['UserName'],data['Password'],data['url_main'],data['url_login'])

	browser.get(data['url_AddAndSub'])
	#if(data['UserName'] not in WhiteListing):
	#	input('not in WhiteListing')
	#	exit()
	n = 0
	while(True):
		if(len(data['CourseNo']) == 0):break

		#try:
		#	print("\n--Input_CourseNo::  " + data['CourseNo'][n])
		#	Input_CourseNo = browser.find_element_by_xpath("//input[@name='CourseText']")#尋找課程代碼輸入欄位
		#	Input_CourseNo.send_keys(data['CourseNo'][n])#輸入課程代碼
		#	Btn_send=browser.find_element_by_id("SingleAdd")#尋找按鈕
		#	Btn_send.click()#點擊
		#	try:
		#		print("\n--Wait Alert ,timeout = " + str(data['Timeout']))
		#		WebDriverWait(browser, data['Timeout']).until(EC.alert_is_present())#等待訊息框
		#		message = browser.switch_to_alert().text
		#		print("\n--Alert text:: " + message)
		#		if(message in '這門課已經在您的選課表或已經修過'):
		#			print("\n--Success "+str(CourseNo[n]))
		#			payload["CourseNo"] = CourseNo[n]
		#			payload["Semester"] = Semester
		#			print("\n--get ::" + url_querycourse)
		#			payload = {"Semester": "1082","CourseNo": data['CourseNo'][n],"CourseName": "","CourseTeacher": "","Dimension": "","CourseNotes": "","ForeignLanguage": 0,"OnlyGeneral": 0,"OnleyNTUST": 0,"OnlyMaster": 0,"OnlyUnderGraduate": 0,"OnlyNode": 0,"Language": "zh"}
		#			req = requests.post(data['url_querycourse'],data=payload)#取的課程詳細資料
		#			data=loads(req.text)
		#			lineNotifyMessage(data['Line_token'], data['CourseNo'][n] + "-" + data['CourseNo'][n])
		#			del data['CourseNo'][n] #刪除以選得課程代碼
		#		if(message in '課程人數額滿或其他錯誤。'):
		#			print("\n--Fail  ")
		#		else:
		#			print("\n--CourseNo" + str(n) + "Err")
		#			del data['CourseNo'][n] #刪除
		#		sleep(data['sleep'])
		#		browser.switch_to_alert().accept()
				
		#		errcnt = 0;
		#	except:
		#		print("\n--Alert err ")
		#		if(browser.current_url[:len(data['url_login'])] == data['url_login']):
		#			browser.get(data['url_login'])
		#			login(browser,data['UserName'],data['Password'])
		#			browser.get(data['url_AddAndSub'])
		#	finally:
		#		n = n + 1
		#		if(n >= len(data['CourseNo'])):
		#			n = 0
		#except:
		#	print("\n--unknow err ")
		#	browser.get(data['url_login'])
		#	login(browser,data['UserName'],data['Password'])
		#	browser.get(data['url_AddAndSub'])
		#	errcnt = errcnt + 1;

		if(errcnt>30):
			return 1



	browser.close()
	return 0