import requests
class LineNotify():
	def __init__(self,token=None):
		self.token = token
		self.enable = True

	def Message(self, msg):
			if(self.enable):
				print('\n--lineNotify enable')
				try:
					headers = {
					"Authorization": "Bearer " + self.token, 
					"Content-Type" : "application/x-www-form-urlencoded"
					}
					payload = {'message': msg}
					requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
					return 'done'
				except:
					print('\n--lineNotify Err')
					return 'lineNotify Err'
			else:
				print('\n--lineNotify disable')
				return 'LineNotify disable'
