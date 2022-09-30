import browser_cookie3
from selenium import webdriver

def getCookiesDicts(domain):
	cookies = browser_cookie3.chrome(domain_name = domain)
	#print(type(cookies))
	cookie_list = []
	for cookie in cookies:
		new = {'name' : cookie.name, 'value' : cookie.value, 'path' : cookie.path, 'domain' : cookie.domain, 'secure' : cookie.secure==1, 'expiry' : cookie.expires}
		cookie_list.append(new)
	#print(cookie_list)
	return cookie_list


driver = webdriver.Chrome()
#driver.get('https://www.ntust.edu.tw/')
#driver.add_cookie({"domain": "courseselection.ntust.edu.tw", "name": "ASP.NET_SessionId", "path": "/", "secure": False, "value": "ve1lwei3ffcu4xe4uijtaybw"})
cookies = getCookiesDicts('ntust.edu.tw')
for cookie in cookies:
	try:
		driver.set_page_load_timeout(1000)
		driver.get(cookie['domain'])
		print('Domain :: ', cookie['domain'])
	except:
		pass
	driver.add_cookie(cookie)
#cookies = getCookiesDicts('.google.com')
#for cookie in cookies:
#	driver.add_cookie(cookie)

#driver.get('https://courseselection.ntust.edu.tw/ChooseList/D01/D01')