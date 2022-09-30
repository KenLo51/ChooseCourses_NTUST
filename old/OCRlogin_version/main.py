##import###############################################################
from selenium import webdriver	#pip install selenium
from selenium.webdriver.common.keys import Keys	#pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from configparser import ConfigParser

from Cryptodome.Cipher import DES
import binascii

import requests
import PIL.Image as Image	#pip install pillow
from pytesseract	import image_to_string#pip install pytesseract
import cv2	#pip install openCV-python
from time import sleep
from json import loads

import NotInWhiteListing

##contest###############################################################
DES_key = b'jc7oe4f8'

UserName = ""
WhiteListing = ("")
Password = ""
CourseNo = [""]
Semester = "1082"
payload = {"Semester": Semester,"CourseNo": "","CourseName": "","CourseTeacher": "","Dimension": "","CourseNotes": "","ForeignLanguage": 0,"OnlyGeneral": 0,"OnleyNTUST": 0,"OnlyMaster": 0,"OnlyUnderGraduate": 0,"OnlyNode": 0,"Language": "zh"}
Cookies = {}
Timeout = 30
sleep_time = 0

url_main="https://courseselection.ntust.edu.tw/"#選課主頁網址
url_login="https://courseselection.ntust.edu.tw/Account/Login"#登入網址
url_AddAndSub = "https://courseselection.ntust.edu.tw/AddAndSub/B01/B01"#加退選網址
url_querycourse = "https://querycourse.ntust.edu.tw/querycourse/api/courses"#課程查詢網址
url_getWhiteListing = 'https://drive.google.com/uc?id=1LF0jgOpSFb8W86cuHkI15VkMlJ5nHy91&export=download'
Line_token = 'deNH5Sf01V4XfHO0HvDqg59TVBaXTRWhezASrqDx9mL'
##function###############################################################
def creatConfig():
	cfg = ConfigParser()
	cfg.write(open('Config.ini','w'))
	cfg.read('Config.ini')

	cfg.add_section('UserName')
	cfg.set('UserName','UserName',input('UserName:'))
	cfg.set('UserName','Password',input('Password:'))

	cfg.add_section('Courses')
	cfg.set('Courses','Semester','1082')
	n=0
	CourseNo = ''
	while(True):
		r = input('Course'+str(n)+'No:')
		CourseNo= CourseNo + ',' + r
		if(len(r)==0):
			break
		n = n+1
	CourseNo = CourseNo[1:len(CourseNo)-1]
	cfg.set('Courses','CourseNo',CourseNo)

	cfg.add_section('LineNotify')
	cfg.set('LineNotify','Line_token',input('Line token:'))

	cfg.add_section('url')
	cfg.set('url','url_main',url_main)
	cfg.set('url','url_login',url_login)
	cfg.set('url','url_AddAndSub',url_AddAndSub)
	cfg.set('url','url_querycourse',url_querycourse)

	cfg.add_section('time')
	cfg.set('time','sleep','0')
	cfg.set('time','Timeout','30')

	cfg.write(open('Config.ini','w'))

def login(browser , UserName , Password , url_main="https://courseselection.ntust.edu.tw/" , url_login="https://courseselection.ntust.edu.tw/Account/Login"):
	VerifyCode = ''
	while(browser.current_url[:len(url_login)] == url_login):#若為登入網址重複嘗試登入
		print("\n--Input_UserName ")
		Input_UserName = browser.find_element_by_id('UserName')#尋找帳號輸入欄位

		for i in range(len(UserName)*2+3):
			Input_UserName.send_keys(Keys.BACKSPACE)#刪除預留文字
			sleep(0.03)

		Input_UserName.send_keys(UserName)#輸入帳號
		print("\n--Input_Password ")
		Input_Password = browser.find_element_by_id('Password')#尋找密碼輸入欄位
		Input_Password.send_keys(Password)#輸入密碼
		Input_VerifyCode = browser.find_element_by_id('VerifyCode')#尋找驗證碼輸入欄位

		for i in range(len(VerifyCode)*2+3):
			Input_VerifyCode.send_keys(Keys.BACKSPACE)#刪除預留文字
			sleep(0.03)

		print("\n--get_cookies ")
		Cookies_list = browser.get_cookies()
		Cookies = {}
		for Cookie in Cookies_list:
			Cookies.setdefault(Cookie['name'],Cookie['value'])
		print(Cookies)#取得cookie用以重新請求驗證碼

		print("\n--get VerifyCode")
		headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
		response = requests.get(url_main+"Account/GetValidateCode",headers=headers,cookies=Cookies,verify=False)#取得驗證碼
		print("\n--Saving  VerifyCode ")
		with open('VerifyCode.jpg','wb') as f:
			f.write(response.content)#輸出驗證碼

		#VerifyCode = input('input VerifyCode::')#輸入驗證碼
		img = cv2.imread('VerifyCode.jpg')#開啟驗證碼圖片
		dst = cv2.fastNlMeansDenoisingColored(img , None , 30 , 10 , 5 , 27)#去除噪點
		cv2.imwrite('VerifyCode_f.jpg',dst)#輸出修改後驗證碼圖片
		image = Image.open('VerifyCode_f.jpg')
		VerifyCode = image_to_string(image)#圖片轉字串

		Input_VerifyCode.send_keys(VerifyCode)#輸入驗證碼
		print("\n--Login...")
		Btn_login=browser.find_element_by_xpath("//input[@type='submit']")#尋找登入按鈕
		Btn_login.click()#點擊

def lineNotifyMessage(token, msg):
	try:
		headers = {
		"Authorization": "Bearer " + token, 
		"Content-Type" : "application/x-www-form-urlencoded"
		}
		payload = {'message': msg}
		requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
		return 0
	except:
		return 1

def getWhiteListing():
	response = requests.get(url_getWhiteListing)
	with open('WhiteListing','wb') as f:
		f.write(response.content)
	des = DES.new(DES_key,DES.MODE_ECB)
	file = open('WhiteListing','rb')
	e_text = file.read()
	file.close()
	e_text = des.decrypt(binascii.a2b_hex(e_text))
	e_text = e_text.decode('utf-8')
	e_text = e_text[:e_text.find('=')]
	return tuple(e_text.split(','))

##init###############################################################
WhiteListing = getWhiteListing()

try:
	fail = open('Config.ini','r')
	fail.close()
	
except:
	creatConfig()

try:
	cfg = ConfigParser()
	cfg.read('Config.ini')

	UserName = cfg['UserName']['UserName']
	Password = cfg['UserName']['Password']

	Semester = cfg['Courses']['Semester']
	CourseNo = cfg['Courses']['CourseNo'].split(',')

	Line_token = cfg['LineNotify']['Line_token']

	url_main = cfg['url']['url_main']
	url_login = cfg['url']['url_login']
	url_AddAndSub = cfg['url']['url_AddAndSub']
	url_querycourse = cfg['url']['url_querycourse']

	sleep_time = float(cfg['time']['sleep'])
	Timeout = float(cfg['time']['Timeout'])

except:
	print('\n--Err Config.ini')
	exit()

print('\n--CourseNo::')
print(CourseNo)
input("press ENTER to continue")
##main###############################################################
browser = webdriver.Chrome(executable_path="chromedriver")#開啟瀏覽器
print("\n--get ::" + url_main)#連線主頁網址 取得cookie(ASP.NET_SessionId)
browser.get(url_main)
print("\n--get ::" + url_login)#連線登入網址
browser.get(url_login)
login(browser,UserName,Password)

browser.get(url_AddAndSub)
if(UserName not in WhiteListing):
	NotInWhiteListing.brabrabra()
	exit()
n = 0
while(True):
	if(len(CourseNo) == 0):break
	try:
		print("\n--Input_CourseNo::  " + CourseNo[n])
		Input_CourseNo = browser.find_element_by_xpath("//input[@name='CourseText']")#尋找課程代碼輸入欄位
		Input_CourseNo.send_keys(CourseNo[n])#輸入課程代碼
		Btn_send=browser.find_element_by_id("SingleAdd")#尋找按鈕
		Btn_send.click()#點擊
		try:
			print("\n--Wait Alert ,timeout = " + str(Timeout))
			WebDriverWait(browser, Timeout).until(EC.alert_is_present())#等待訊息框
			message = browser.switch_to_alert().text
			print('\n--message:: ' + message)
			if(message in '這門課已經在您的選課表或已經修過，請勿重複選課(課碼、課名重複)。'):
				print("\n--Success "+str(CourseNo[n]))
				payload["CourseNo"] = CourseNo[n]
				payload["Semester"] = Semester
				print("\n--get ::" + url_querycourse)
				req = requests.post(url_querycourse,data=payload)#取的課程詳細資料
				data=loads(req.text)
				lineNotifyMessage(Line_token, data[0]["CourseNo"] + "-" + data[0]["CourseName"])
				del CourseNo[n] #刪除以選得課程代碼
			if(message in '課程人數額滿或其他錯誤。'):
				print("\n--Fail  ")
			if(message in '課程不存在!'):
				print("\n--CourseNo" + str(n) + "Err")
				del CourseNo[n] #刪除以選得課程代碼
			browser.switch_to_alert().accept()
			sleep(sleep_time)
		except:
			print("\n--Alert err ")
			if(browser.current_url[:len(url_login)] == url_login):
				browser.get(url_login)
				login(browser,UserName,Password)
				browser.get(url_AddAndSub)
		finally:
			n = n + 1
			if(n >= len(CourseNo)):
				n = 0
	except:
		print("\n--unknow err ")
		browser.get(url_login)
		login(browser,UserName,Password)
		browser.get(url_AddAndSub)

browser.close()
input("press ENTER to close")
exit()