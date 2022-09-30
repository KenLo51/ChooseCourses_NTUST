##import###############################################################
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
from time import sleep
from json import loads

import module
##contest###############################################################
#DES_key = b'jc7oe4f8'

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
Line_token = ''
##function###############################################################
##init###############################################################
#WhiteListing = module.getWhiteListing(DES_key , url_getWhiteListing)

try:
	fail = open('Config.ini','r')
	fail.close()
	
except:
	module.creatConfig()

try:
	config = module.readConfig()

except:
	print('\n--Err Config.ini')
	exit()
##main###############################################################
print(config['CourseNo'])
module.ChooseCourses(config,WhiteListing)
input("press ENTER to close")
exit()