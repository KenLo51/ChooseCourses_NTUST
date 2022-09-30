##import###############################################################
from selenium import webdriver	#pip install selenium
from selenium.webdriver.common.keys import Keys	#pip install selenium

import requests
import PIL.Image as Image	#pip install pillow
import pytesseract	#pip install pytesseract
import cv2	#pip install openCV-python
import time

##contest###############################################################
UserName = "B10802034"
Password = "tks673uts"
Cookies = {}
url_main="https://courseselection.ntust.edu.tw/"#選課主頁網址
url_login="https://courseselection.ntust.edu.tw/Account/Login"#登入網址
url_AddAndSub = "https://courseselection.ntust.edu.tw/AddAndSub/B01/B01"#加退選網址

##function###############################################################
def login(browser , UserName , Password):
	url_main="https://courseselection.ntust.edu.tw/"#選課主頁網址
	url_login="https://courseselection.ntust.edu.tw/Account/Login"#登入網址
	VerifyCode = ''
	while(browser.current_url[:len(url_login)] == url_login):#若為登入網址重複嘗試登入
		print("\n--Input_UserName ")
		Input_UserName = browser.find_element_by_id('UserName')#尋找帳號輸入欄位

		for i in range(len(UserName)+3):
			Input_UserName.send_keys(Keys.BACKSPACE)#刪除預留文字
			time.sleep(0.05)

		Input_UserName.send_keys(UserName)#輸入帳號
		print("\n--Input_Password ")
		Input_Password = browser.find_element_by_id('Password')#尋找密碼輸入欄位
		Input_Password.send_keys(Password)#輸入密碼
		Input_VerifyCode = browser.find_element_by_id('VerifyCode')#尋找驗證碼輸入欄位

		for i in range(len(VerifyCode)+3):
			Input_VerifyCode.send_keys(Keys.BACKSPACE)#刪除預留文字
			time.sleep(0.05)

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
		VerifyCode = pytesseract.image_to_string(image)#圖片轉字串

		Input_VerifyCode.send_keys(VerifyCode)#輸入驗證碼
		print("\n--Login...")
		Btn_login=browser.find_element_by_xpath("//input[@type='submit']")#尋找登入按鈕
		Btn_login.click()#點擊

##main###############################################################
browser = webdriver.Chrome()#開啟瀏覽器
print("\n--get ::" + url_main)#連線主頁網址取得cookie(ASP.NET_SessionId)
browser.get(url_main)
print("\n--get ::" + url_login)#連線登入網址
browser.get(url_login)
login(browser,UserName,Password)