#import##################################################
import requests
import time

url_main="https://courseselection.ntust.edu.tw/"#選課主頁網址
url_login="https://courseselection.ntust.edu.tw/Account/Login"#登入網址

UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
UserName = "B10802034"
Password = "tks673uts"
headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
			,"Accept-Encoding": "gzip, deflate, br"
			,"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
			,"User-Agent":UserAgent
			,"Upgrade-Insecure-Requests":"1"
			,"Referer": "https://courseselection.ntust.edu.tw/"
			}
Cookies={}


session = requests.Session()

print("\n--get ::"+url_main)
headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
			,"Accept-Encoding": "gzip, deflate, br"
			,"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
			,"User-Agent":UserAgent
			,"Upgrade-Insecure-Requests":"1"}
response = session.get(url_main,headers=headers,verify=False)#開啟選課主頁
Cookies.setdefault("ASP.NET_SessionId",response.cookies["ASP.NET_SessionId"])#取得cookie(ASP.NET_SessionId)
print("\n--response.headers ::")
print(response.headers)
with open('main without login.txt','w') as f:
	f.write(response.text)

time.sleep(2)

print("\n--get ::"+url_login)
headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
			,"Accept-Encoding": "gzip, deflate, br"
			,"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
			,"User-Agent":UserAgent
			,"Upgrade-Insecure-Requests":"1"
			,"Referer": url_main}
response = session.get(url_login,headers=headers,verify=False)#開啟登入頁面
Cookies.setdefault("__RequestVerificationToken",response.cookies["__RequestVerificationToken"])#取得cookie(__RequestVerificationToken)
RequestVerificationToken = response.cookies["__RequestVerificationToken"]
print("\n--response.headers ::")
print(response.headers)
with open('login page.txt','w') as f:
	f.write(response.text)

headers={"Accept": "text/css,*/*;q=0.1"
			,"Accept-Encoding": "gzip, deflate, br"
			,"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
			,"User-Agent":UserAgent
			,"Upgrade-Insecure-Requests":"1"
			,"Referer": url_login}
response = session.get(url_main,headers=headers,verify=False)#開啟選課主頁

time.sleep(1)

headers["Accept"] = "image/webp,image/apng,image/*,*/*;q=0.8"
print("\n--get CAPTCHA ::")
response = session.get(url_main+"Account/GetValidateCode",headers=headers,verify=False)#取得驗證碼
with open('CAPTCHA.jpg','wb') as f:
	f.write(response.content)#輸出驗證碼

time.sleep(1)


VerifyCode = input("VerifyCode=")#輸入驗證碼
print("\n--post password ::")
value = {"__RequestVerificationToken":RequestVerificationToken,
												"UserName":UserName,
												"Password":Password,
												"VerifyCode":VerifyCode}
headers={"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
			,"Accept-Encoding": "gzip, deflate, br"
			,"Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7"
			,"User-Agent":UserAgent
			,"Upgrade-Insecure-Requests":"1"
			,"Referer": url_login
			,"Origin":url_main
			,"Cache-Control":"max-age=0"}
response = session.post(url_login,headers=headers,data = value,verify=False)
print("\n--response headers ::")
print(response.headers)

session.close()
input("\n\nSTOP")