from selenium import webdriver	#pip install selenium
#from selenium.webdriver.common.keys import Keys	#pip install selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from requests.adapters import HTTPAdapter
import time
import json
import sys
import os

if __name__ == '__main__':
	#chooseType = sys.argv[1]
	chooseType = "addandsub"
	
	# %% read config data
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Reading urls")
	urls=None
	with open('urls.json',mode = 'r',encoding='utf8') as jsonFile:
		urls = json.loads(jsonFile.read())

	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Reading userdata")
	userdata=None
	with open('userdata.json',mode = 'r',encoding='utf8') as jsonFile:
		userdata = json.loads(jsonFile.read())
	
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Reading cookies")
	cookies=None
	if os.path.exists('cookies.json') :
		with open('cookies.json',mode = 'r',encoding='utf8') as jsonFile:
			cookies = json.loads(jsonFile.read())
			
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Reading header")
	header=None
	with open('header.json',mode = 'r',encoding='utf8') as jsonFile:
		header = json.loads(jsonFile.read())

	# %% functions
	def login(): # re-login
		driver = webdriver.Chrome()

		#try to login
		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print(f"getting \"{urls[chooseType][0]}\"")

		driver.get(urls[chooseType][0])
		if(driver.current_url in urls['login']):#Login fail
			print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
			print("Login fail")

		while(driver.current_url in urls['login']):#Wait for user login manually
			time.sleep(1)

		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print("Login success")

		#save cookies
		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print("Saving cookies")
		cookies = driver.get_cookies()
		with open('cookies.json',mode='w') as jsonFile:
			jsonFile.write(json.dumps( cookies , indent = 6))

		driver.close()

		return cookies

	def cookies_Dic2Jar(cookies):# convert cookies data structure
		cookie_jar = requests.cookies.RequestsCookieJar()
		for cookie in cookies:
			cookie_jar.set(cookie['name'], cookie['value'], domain=cookie['domain'], path=cookie['path'], secure=cookie['secure'])
		return cookie_jar

	# %% session init
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print("Creating session")
	session = requests.Session()
	session.mount('http://', HTTPAdapter(max_retries=3))
	session.mount('https://', HTTPAdapter(max_retries=3))

	# check login status
	cookie_jar = cookies_Dic2Jar(cookies)
	receiveData = session.get(urls[chooseType][0], cookies = cookie_jar, timeout=5).content.decode('utf8')
	if "<title>台灣科技大學系統登入(NTUST Login)</title>" in receiveData:#relogin
		cookies = login()
	else:
		print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
		print(f"login success")
	cookie_jar = cookies_Dic2Jar(cookies)
	
	courseIdList = userdata["courseNo"]
	print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
	print(f"Pressed Ctrl + C to stop")
	errCounter = 0
	while(True):
		try:
			#check if logout
			receiveData = session.get(urls[chooseType][0], cookies = cookie_jar, timeout=5).content.decode('utf8')
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
				session.post(urls[chooseType][1], data = payload, cookies = cookie_jar, timeout=5)
				time.sleep(userdata["delaytime"])
		
			errCounter = 0

		except KeyboardInterrupt:
			print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
			print("Stop")
			session.close()
			break

		except:
			errCounter += 1
			if(errCounter>=10):
				print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
				print("unknow error")