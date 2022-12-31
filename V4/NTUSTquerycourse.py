# std libraries
import requests
import os
from requests.adapters import HTTPAdapter
import typing
import json
import time
import multiprocessing as mp
import threading
import queue

#
import browser_cookie3

# user libraries
import config

class Querycourse():
    def __init__(self):
        # course and user datas
        # self.cookies = browser_cookie3.chrome()
        self.cookies = None
        self.courseList = []
        # read from file
        if os.path.exists("userdata.json"):
            with open('userdata.json', mode="r", encoding="utf8") as f:
                self.courseList = json.load(f)

        # multiprocessing variables
        self.chooseCouresTasks = []
        self.chooseCouresQueues = []

    def saveUserdata(self) -> typing.NoReturn:
        with open('userdata.json', mode="w", encoding="utf8") as f:
            json.dump(self.courseList, f)

    def checkLogin(self) -> bool:
        page = requests.get(url=config.ntust_querycourseLoginUrl, cookies=self.cookies)
        data = json.loads( page.content.decode("utf8") )
        return data["Success"]

    def checkAddLogin(self, url) -> bool:
        receiveData = requests.get(url, cookies=self.cookies, timeout=5).content.decode('utf8')
        if "<title>台灣科技大學系統登入(NTUST Login)</title>" in receiveData:
            return False
        return True

    # get course detial by course-ID
    def getCourseDetial(self, courseID : str) :
        payload = { "semester":"1112",
                    "course_no":courseID,
                    "language":"zh"}
        page = requests.get(url=config.ntust_coursedetialsUrl, params=payload)
        detals = json.loads( page.content.decode("utf8") )
        return detals

    def getViewlist(self):
        page = requests.get(url=config.ntust_viewcourseUrl, cookies=self.cookies)
        data = json.loads( page.content.decode("utf8") )
        return data
        
    def getSemesters(self):
        page = requests.get(url=config.ntust_semestersInfoUrl)
        data = json.loads( page.content.decode("utf8") )
        return data[0]["Semester"]


    chooseTaskFlag = False
    # start nTasks process to adding course in courseIdList.
    def startChooseCoures(self, nTasks : int, courseIdList : typing.List, url : str, delay = 5) -> typing.NoReturn:
        self.chooseCouresQueues.clear()
        self.chooseCouresTasks.clear()
        print("creating task")

        #q = mp.Queue()
        #self.chooseCouresTask(q, courseIdList, url, delay)
        for i in range(nTasks):
            q = queue.Queue()
            porc = threading.Thread(target=self.chooseCouresTask, args=(q, courseIdList, url, delay))
            porc.start()

            self.chooseCouresQueues.append(q)
            self.chooseCouresTasks.append(porc)
        self.chooseTaskFlag = True
        
    # stop all tasks
    def stopChooseCoures(self)->typing.NoReturn:
        for q in self.chooseCouresQueues:
            q.put("stop")
        threading.Thread(target=self.waitToStopTask).start()

    def waitToStopTask(self):
        for p in self.chooseCouresTasks:
            p.join()
        self.chooseTaskFlag = False

    def chooseCouresTask(self, q:mp.Queue, courseIdList:typing.List, url:str, delay:float)->typing.NoReturn:
        cookies = browser_cookie3.chrome()
        session = requests.Session()
        session.mount('http://', HTTPAdapter(max_retries=3))
        session.mount('https://', HTTPAdapter(max_retries=3))

        errCounter = 0
        while True:
            if not q.empty():
                if q.get() == "stop":
                    break
            try:
                #try to join new course
                for courseID in courseIdList:
                    print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
                    print(f"try to join {courseID}")
                    payload = {"CourseNo":courseID, "type": 3}
                    session.post(url, data = payload, cookies = cookies, timeout=5)
                    time.sleep(delay)
            
                errCounter = 0
            except:
                errCounter += 1
                # reload cookies
                if(errCounter>=5):
                    cookies = browser_cookie3.chrome()
                # unknow error
                if(errCounter>=10):
                    print(f"{time.asctime( time.localtime(time.time()) )} -- ",end='')
                    print("unknow error")
                    break