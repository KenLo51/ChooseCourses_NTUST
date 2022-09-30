import requests
Cookies = {'ASP.NET_SessionId':'rm3yor2noank1hk3bifqx2ec'}
url_main="https://courseselection.ntust.edu.tw/"#選課主頁網址
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
num = int(input('num:'))
for i in range(num):
	response = requests.get(url_main+"Account/GetValidateCode",headers=headers,cookies=Cookies,verify=False)#取得驗證碼
	with open('VerifyCode/'+str(i)+'.jpg','wb') as f:
		f.write(response.content)#輸出驗證碼
