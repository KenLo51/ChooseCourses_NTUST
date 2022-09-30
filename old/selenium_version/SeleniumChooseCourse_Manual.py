from selenium import webdriver	#pip install selenium
#from selenium.webdriver.common.keys import Keys	#pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import LineNotify

def newDriver():
	cookies = driver.get_cookies()
	print(cookies)
	driver = webdriver.Chrome()
	driver.get('https://courseselection.ntust.edu.tw/')
	for cookie in cookies:
		driver.add_cookie(cookie)
	driver.get('https://courseselection.ntust.edu.tw/')

def AutoChooseCourses(browser, CourseNo, AlertTimeout = 100 , sleep=5, ):
	n=0
	errTimes=0
	browser.get("https://courseselection.ntust.edu.tw/First/A06/A06")
	while(True):
		browser.get("https://courseselection.ntust.edu.tw/First/A06/A06")
		if(errTimes > 20):
			print('error return')
			return 'UnknowErr'
		try:
			print("add", CourseNo[n] )
			Input_CourseNo = browser.find_element_by_xpath("//input[@name='CourseText']")
			Input_CourseNo.send_keys(CourseNo[n])
			browser.find_element_by_id("SingleAdd").click()
			print('wait alert')
			WebDriverWait(browser, AlertTimeout).until(EC.alert_is_present())
			alert = driver.switch_to.alert
			message = alert.text 
			print('alert-', message)
			if(message in '這門課已經在您的選課表或已經修過'):
				print("\n--Success "+str(CourseNo[n]))
				del CourseNo[n] 
			if('課程人數額滿' in message):
				print("\n--Fail  ")
			else:
				print("\n--CourseNo" + str(n) + "Err")
				#del CourseNo[n]
			alert.accept()


			print('next courseID')
			n=n+1
			if(n>=len(CourseNo)):
				n=0
			errTimes=0
		except:
			errTimes=errTimes+1
			print('error' , errTimes)
			time.sleep(10)

def Login(browser, Userdata, notify):
	try:
		browser.switch_to.alert().accept
	except:
		pass
	url = {'Login':'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'}
	browser.get('https://courseselection.ntust.edu.tw/')
	if(browser.current_url in 'https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection'):
		if("https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection" in browser.current_url):
			print("Login...")
		UserName_Entry = browser.find_element_by_name("UserName")
		UserName_Entry.send_keys(Userdata['username'])
		password_Entry = browser.find_element_by_name("Password")
		password_Entry.send_keys(Userdata['password'])
		LogIn_Button = browser.find_element_by_id('btnLogIn')
		LogIn_Button.click()
		notify.Message('Auto Choose Course need to login')
		while(True):
			if(browser.current_url in "https://courseselection.ntust.edu.tw/"):
				time.sleep(5)
				break
		print('Login Success')
		notify.Message('Course Selection Login Success')
	



if __name__ == '__main__':
	config=None
	with open('config.json',mode = 'r',encoding='utf8') as j:
		d=j.read()
		config = json.loads(d)

	lineNotify = LineNotify.LineNotify(config['line_token'])


	driver = webdriver.Chrome()
	print(config)
	cookies=None
	while(True):
		try:
			with open('cookies.json',mode='r') as f:
				cookies = json.load(f)
			driver.get('https://stuinfosys.ntust.edu.tw/NTUSTSSOServ/SSO/Login/CourseSelection')
			for cookie in cookies:
				print('addcokie',cookie['name'])
				driver.add_cookie(cookie)
			time.sleep(3)
			driver.get('https://courseselection.ntust.edu.tw/')
			break
		except:
			pass
		Login(driver, config, lineNotify)
		with open('cookies.json',mode='w') as f:
			f.write(json.dumps( driver.get_cookies() ))
		AutoChooseCourses(driver, config['courseNo'])
	driver[0].close()
