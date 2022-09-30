#import##################################################
import json 
import urllib.request as req
import urllib.parse as parse
import requests
import random 
import time
import urllib3

UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"
UserName = "B10802034"
Password = "tks673uts"
Cookies=""
def add_cookie(Cookies="",addCookie=""):
	if(addCookie=="") :
		return ""
	B=addCookie.find("=")
	while(B != -1):
		E=addCookie.find(";",B)
		
		if(Cookies==""):
			Cookies = addCookie[:E]
		else:
			Cookies = Cookies+";"+addCookie[:E]
		if(addCookie[E+1:E+6] == " path"):
			return Cookies
		B=addCookie.find("=",E)


#url = "https://courseselection.ntust.edu.tw/" #選課主頁網址
#url = "https://courseselection.ntust.edu.tw/Account/Login" #登入網址

request = req.Request(url="https://courseselection.ntust.edu.tw/",
									headers={"user-agent":UserAgent})
data = req.urlopen(request)#開啟登入頁面
Cookies = add_cookie(Cookies,data.getheader("Set-Cookie"))#取得cookie(__RequestVerificationToken)
print("get cookie:"+data.getheader("Set-Cookie"))

request = req.Request(url="https://courseselection.ntust.edu.tw/Account/Login",
									headers={"user-agent":UserAgent})
data = req.urlopen(request)#開啟登入頁面
RequestVerificationToken = data.getheader("Set-Cookie")
RequestVerificationToken = RequestVerificationToken[RequestVerificationToken.find("=")+1:RequestVerificationToken.find(";")]
Cookies = add_cookie(Cookies,data.getheader("Set-Cookie"))#取得cookie(__RequestVerificationToken)
print("get cookie:"+data.getheader("Set-Cookie"))



request = req.Request(url="https://courseselection.ntust.edu.tw/Account/GetValidateCode",
									headers={"User-Agent":UserAgent,
													"cookie":Cookies})
data = req.urlopen(request)#取得驗證碼
with open('CAPTCHA.jpg','wb') as f:
	f.write(data.read())#輸出驗證碼



VerifyCode = input("VerifyCode=")#輸入驗證碼
value = {"__RequestVerificationToken":RequestVerificationToken,
												"UserName":UserName,
												"Password":Password,
												"VerifyCode":VerifyCode}
#data = parse.urlencode(vlaue).encode("utf-8")#密碼轉url格式
#request = req.Request(url="https://courseselection.ntust.edu.tw/Account/Login",
#									headers={"user-agent":UserAgent,
#													"cookie":Cookies,
#													"Referer": "https://courseselection.ntust.edu.tw/Account/Login",
#													"Origin":"https://courseselection.ntust.edu.tw",
#													"sec-fetch-mode":"navigate",
#													"sec-fetch-site":"same-origin",
#													"sec-fetch-user":"?1",
#													"upgrade-insecure-requests":"1",
#													"Connection": "keep-alive"}
#									)
#data = req.urlopen(request,data)#登入

request = req.Request(url="https://courseselection.ntust.edu.tw/",
									headers={"User-Agent":UserAgent,
													"cookie":Cookies})
data = req.urlopen(request)
print(data.read().decode("utf-8"))

#with open('pade.txt','wb') as f:
#	f.write(data.read().decode("utf-8"))

#print(Cookies)
#print(data.read().decode("utf8"))
#print(request.getheaders())
#time.sleep(1)
#request = req.Request(url="https://courseselection.ntust.edu.tw/",
#									headers={"user-agent":user-agent,
#													"cookie":cookies})
#data = req.urlopen(request)

#print(data.read().decode("utf-8"))

#request = req.Request(url="https://courseselection.ntust.edu.tw/Account/LogOff",
#									headers={"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
#													"cookie":"ASP.NET_SessionId=dvm1rwuvoshjvli4akdgt4nk"+str(RequestVerificationToken)+"; _ga=GA1.3.96550728.1581920623; .AspNet.TwoFactorRememberBrowser=b56cPK0IaaSRuLZ8odR2Yp9jOHJxhv_dI2XIelao2V-lnIbzGyNLLD8PWPdjYxe4JUHsa0tjjLR1ePhvmFThh9zljCYBNuGskIHpn_dOH1sbIsblgrsTEZjMjGSQofJiyoFJNnnGAe54SAVEdn5RojUAN5rrf8VtjqzfRnPk2GLf-3PC0jLLTHK3hvJfo0u6SOk2HgU6sIEmWCdO1qgWjnhxq582gpWBFA1By2etVm36vJZciM376Ujtxg1Of9uJFyFNF8xN5YqG213MP7C290rN6R4USjfBYTpPnH2aaH2IS31RtB1HwjuCoewdLx26; .AspNet.ApplicationCookie=RtcO8ddlDiiTBY2jHYtKoTHtoJi-W_AASfpTi6gY_DR4AVAN5NK5Xg2H5fMJVlT8wzojQDLEEglOfMZLLc5hnCZIrgT_GIy8fzCrwWCrRsUzVhucsbEP8dgvrJzxxKHNSt2pLE2vAIb8shh_xxPdn7oGIjI8PdscxnyxMZUcK4RmGqehg0bo6P1xwUTDLzovqGNEqzuNh8HUTsWCZ4j6Qincbyv-jB9DJINqeojmMrmwVM2PvOFsB5lNuFtB4hY8DR3gz0WtLEeCH2t9sYo1pW37gnKtUiiqd0sDj-uorBnH6Ct9rWrhgMQ9t_A98LLzAXiBAyDsc3xgcZF3EY7uhYDQEOozXZxSTQxhJGCkLidUHZ9cmtr1wGRJSGAkf3LFg_0MwZ9SWRiWkbxTefdYQjqf73Iz5tgAojByCJiU33KqEum2-W4P94jXBMxjLWWF"},
#									data = {"__RequestVerificationToken": RequestVerificationToken})
#data = req.urlopen(request)

