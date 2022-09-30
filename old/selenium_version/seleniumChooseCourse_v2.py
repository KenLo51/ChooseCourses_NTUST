from selenium import webdriver	#pip install selenium
#from selenium.webdriver.common.keys import Keys	#pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.cookies import RequestsCookieJar
from requests.adapters import HTTPAdapter
import time
import json
import sys


def login():
	#try to login
	driver = webdriver.Chrome()
	driver.get(urls[chooseType])
	if(driver.current_url in urls['login']):#Login fail
		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print("Login fail")
	while(driver.current_url in urls['login']):#Wait for user login manually
		time.sleep(1)

	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Login success")
	#save cookies
	cookies = driver.get_cookies()
	with open('cookies.json',mode='w') as jsonFile:
		jsonFile.write(json.dumps( cookies ))

	driver.close()

	return cookies

if __name__ == '__main__':
	#chooseType = sys.argv[1]
	chooseType = "Adding_or_Dropping"
	#read config data
	urls=None
	with open('urls.json',mode = 'r',encoding='utf8') as jsonFile:
		urls = json.loads(jsonFile.read())
	userdata=None
	with open('userdata.json',mode = 'r',encoding='utf8') as jsonFile:
		userdata = json.loads(jsonFile.read())
	cookies=None
	with open('cookies.json',mode = 'r',encoding='utf8') as jsonFile:
		cookies = json.loads(jsonFile.read())
	header=None
	with open('header.json',mode = 'r',encoding='utf8') as jsonFile:
		header = json.loads(jsonFile.read())

	cookie_jar = requests.cookies.RequestsCookieJar()
	for cookie in cookies:
		cookie_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'], secure=cookie['secure'])


	session = requests.Session()
	session.mount('http://', HTTPAdapter(max_retries=3))
	session.mount('https://', HTTPAdapter(max_retries=3))

	receiveData = session.get(urls[chooseType], cookies = cookie_jar, timeout=5).content.decode('utf8')
	if "<title>台灣科技大學系統登入(NTUST Login)</title>" in receiveData:#relogin
		cookies = login()
	else:
		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print(f"login success")

	courseIdList = userdata["courseNo"]
	cookie_jar = requests.cookies.RequestsCookieJar()
	for cookie in cookies:
		cookie_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'], secure=cookie['secure'])
	
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print(f"Pressed Ctrl + C to stop")
	while(True):
		try:
			#check if logout
			receiveData = session.get(urls[chooseType], cookies = cookie_jar, timeout=5).content.decode('utf8')
			if "<title>台灣科技大學系統登入(NTUST Login)</title>" in receiveData:#relogin
				cookies = login()

			#delete selected id
			receiveData = receiveData[receiveData.rfind("選課清單</span>"):]
			delId = []
			for courseID in courseIdList:
				if(courseID in receiveData):
					print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
					print(f"{courseID} has selected")
					delId.append(courseID)
			for courseID in delId:
				courseIdList.remove(courseID)

			#
			if(len(courseIdList) == 0):
				print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
				print(f"No more course can select")
				break

			#try to join new course
			for courseID in courseIdList:
				print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
				print(f"try to join {courseID}")
				payload = {"CourseNo":courseID, "type": 3}
				session.post(urls["ExtraJoin"], data = payload, cookies = cookie_jar, timeout=5)
				time.sleep(1)
		except KeyboardInterrupt:
			print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
			print(f"stop by keyboard interrupt")
			sys.exit()
		except:
			print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
			print(f"unkunw error")