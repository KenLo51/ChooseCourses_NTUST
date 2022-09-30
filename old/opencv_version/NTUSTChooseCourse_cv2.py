import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
from pytesseract	import image_to_string#pip install pytesseract
from configparser import ConfigParser
import keyboard
import threading




#while(True):
#	img_screen = screenshot_cv2foramt()
#	res = cv2.matchTemplate(img_screen,img_LoginLogo,cv2.TM_CCOEFF_NORMED)


#img_rgb = cv2.imread("target.jpg")
#img_gray = cv2.cvtColor(img_rgb,cv2.COLOR_BGR2GRAY)
#cv2.imshow('img_gray',img_gray)
#template = cv2.imread("template2.jpg")
#template = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
#cv2.imshow('template',template)
#w,h = template.shape[::-1]
#res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
#threshold = 0.8
#loc = np.where(res>threshold)
#print(loc)
#print()
#print(loc[::-1])
#print()
#print(*loc[::-1])
#print()
#print(loc[0][0])
#for pt in zip(*loc[::-1]):
#	cv2.rectangle(img_rgb,pt,(pt[0]+w , pt[1]+h),(0,255,255),2)
#cv2.imshow('result',img_rgb)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

class Main(threading.Thread):
	def writeConfig(ConfigName,data):
		cfg = ConfigParser()
		cfg.add_section('Config')
		cfg.set('Config','CourseIDList',data['CourseIDList'])
		cfg.set('Config','CourseIDList',data['UserID'])
		cfg.set('Config','CourseIDList',data['Password'])
	def readConfig(ConfigName):
		cfg = ConfigParser()
		cfg.read(ConfigName)
		return cfg['Config']
	def __init__(self):
		threading.Thread.__init__(self,daemon=True)
		self.time0=time.time()
		self.CoourseList=['FE1231701','FE2171702']
		self.CoourseList_counter=0
		self.UserID='B10802034'
		self.Password='tks673uts'
		self.img_BrowserIcon = cv2.imread("BrowserIcon.jpg")
		self.img_BrowserAddress = cv2.imread("BrowserAddress.jpg")
		self.img_WinSearchButton = cv2.imread("WinSearchButton.jpg")
		self.img_LoginLogo = cv2.imread("LoginLogo.jpg")
		self.img_UserIDEntry = cv2.imread("UserIDEntry.jpg")
		self.img_CourseselectionLogo = cv2.imread("CourseselectionLogo.jpg")
		self.img_PasswordEntry = cv2.imread("PasswordEntry.jpg")
		self.img_LoginButton = cv2.imread("LoginButton.jpg")
		self.img_AddCourseLogo = cv2.imread("AddCourseLogo.jpg")
		self.img_AddCourseUrlButton0 = cv2.imread("AddCourseUrlButton0.jpg")
		self.img_AddCourseUrlButton1 = cv2.imread("AddCourseUrlButton1.jpg")
		self.img_CourseNumEntry = cv2.imread("CourseNumEntry.jpg")
		self.img_AddCourseButton = cv2.imread("AddCourseButton.jpg")
		self.img_AddCourseAlert = cv2.imread("AddCourseAlert.jpg")
		self.img_NonOpeningDateAlert = cv2.imread("NonOpeningDateAlert.jpg")
		self.img_AlertButton = cv2.imread("AlertButton.jpg")
		self.img_AlertButton_ch = cv2.imread("AlertButton_ch.jpg")
		return
	def screenshot_cv2foramt(self):
		img = ImageGrab.grab()
		img_np = np.array(img)
		screenshot_frame = cv2.cvtColor(img_np , cv2.COLOR_BGR2RGB)
		return screenshot_frame
	def chackExist(self,img,threshold,img_screen=np.array([])):
		if(img_screen.shape[0]<2):
			img_screen = self.screenshot_cv2foramt()
		img_screen = cv2.cvtColor(img_screen,cv2.COLOR_BGR2GRAY)
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_screen,img,cv2.TM_CCOEFF_NORMED)
		loc = np.where(res>threshold)
		return loc[0].shape[0]>0
	def whichPage(self,img_list,threshold):
		out_list=[]
		img_screen = self.screenshot_cv2foramt()
		for img in img_list:
			out_list.append(self.chackExist(img,threshold,img_screen))
		return out_list
	def FindandMove(self,img):
		img_screen = self.screenshot_cv2foramt()
		img_screen = cv2.cvtColor(img_screen,cv2.COLOR_BGR2GRAY)
		img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		res = cv2.matchTemplate(img_screen,img,cv2.TM_CCOEFF_NORMED)
		h,w = img.shape
		threshold = 1
		while(True):
			loc = np.where(res>threshold)
			if(loc[0].shape[0]>0):
				loc =(loc[1][0]+(w//2),loc[0][0]+(h//2))#column , row
				break
			threshold = threshold-0.1
			if(threshold<0.5):
				return
		pyautogui.moveTo(loc)
	def TypeWrite(self,str,delayTime=0.1):
		for c in list(str):
			pyautogui.typewrite(c)
			time.sleep(delayTime)
	def run(self):
		self.FindandMove(self.img_BrowserIcon)
		pyautogui.click()
		time.sleep(0.2)

		while(True):
			case = self.whichPage([self.img_LoginLogo, self.img_CourseselectionLogo,self.img_AddCourseLogo,self.img_AlertButton,self.img_AlertButton_ch],0.75)
			if(case[0]):
				self.FindandMove(self.img_UserIDEntry)
				pyautogui.click()
				self.TypeWrite(self.UserID+'\t'+self.Password+'\n')
				self.time0=time.time()

			elif(case[1]):
				self.FindandMove(self.img_AddCourseUrlButton0)
				pyautogui.click()
				self.FindandMove(self.img_AddCourseUrlButton1)
				pyautogui.click()
				self.time0=time.time()

			elif(case[2]):
				self.FindandMove(self.img_CourseNumEntry)
				time.sleep(0.1)
				pyautogui.click()
				time.sleep(0.1)
				pyautogui.typewrite(self.CoourseList[self.CoourseList_counter])
				print('course :',self.CoourseList[self.CoourseList_counter])
				self.CoourseList_counter = self.CoourseList_counter +1
				if(self.CoourseList_counter>=len(self.CoourseList)):
					self.CoourseList_counter=0
				self.FindandMove(self.img_AddCourseButton)
				pyautogui.click()
				self.time0=time.time()

			elif(case[3]):
				self.FindandMove(self.img_AlertButton)
				pyautogui.click()
				time.sleep(0.1)
				self.time0=time.time()
			
			elif(case[4]):
				self.FindandMove(self.img_AlertButton_ch)
				pyautogui.click()
				time.sleep(0.1)
				self.time0=time.time()

			else:
				if((self.time0 - time.time()) > 5):
					self.FindandMove(self.img_BrowserAddress)
					pyautogui.click()
					pyautogui.typewrite('https://courseselection.ntust.edu.tw/First/A06/A06')
			#if(self.chackExist(self.img_LoginLogo,0.8)):
			#	self.FindandMove(self.img_UserIDEntry)
			#	pyautogui.click()
			#	self.TypeWrite(self.UserID+'\t'+self.Password+'\n')

			#	time.sleep(2)

			#if(self.chackExist(self.img_CourseselectionLogo,0.8)):
			#	self.FindandMove(self.img_AddCourseUrlButton0)
			#	pyautogui.click()

			#	self.FindandMove(self.img_AddCourseUrlButton1)
			#	pyautogui.click()
			#	time.sleep(2)

			#if(self.chackExist(self.img_NonOpeningDateAlert,0.8)):
			#	self.FindandMove(self.img_AlertButton)
			#	pyautogui.click()
			#	time.sleep(2)

#UserID='B10802034'
#Password='tks673uts'
#img_BrowserIcon = cv2.imread("BrowserIcon.jpg")
#img_LoginLogo = cv2.imread("LoginLogo.jpg")
#img_UserIDEntry = cv2.imread("UserIDEntry.jpg")
#img_CourseselectionLogo = cv2.imread("CourseselectionLogo.jpg")
#img_PasswordEntry = cv2.imread("PasswordEntry.jpg")
#img_LoginButton = cv2.imread("LoginButton.jpg")
#img_AddCourseUrlButton0 = cv2.imread("AddCourseUrlButton0.jpg")
#img_AddCourseUrlButton1 = cv2.imread("AddCourseUrlButton1.jpg")
#img_CourseNumEntry = cv2.imread("CourseNumEntry.jpg")
#img_AddCourseButton = cv2.imread("AddCourseButton.jpg")
#img_AddCourseAlert = cv2.imread("AddCourseAlert.jpg")
#img_NonOpeningDateAlert = cv2.imread("NonOpeningDateAlert.jpg")
#img_AlertButton = cv2.imread("AlertButton.jpg")

Main_thread = Main()
Main_thread.start()
Main_thread.join()