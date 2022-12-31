import tkinter as tk
import threading

import browser_cookie3

import NTUSTquerycourse
import config

class mainWindow():
    def __init__(self):
        self.Querycourse = NTUSTquerycourse.Querycourse()
        self.mode = ""

        # create window
        self.window = tk.Tk()
        # set title
        self.window.title('ChooseCourses NTUST V4')
        # set window size
        self.window.geometry('800x600')
        self.window.resizable(False, False)

        self.initUI()
        self.updateCourselist()

    def initUI(self):
        
        self.coursesFrame = tk.Frame(self.window, bg = "#505050", width=800, height=460)
        self.coursesFrame.place(x=0, y=0)
        self.initCoursesListlUI()

        self.controlFrame = tk.Frame(self.window, bg="#404040", width=800, height=140)
        self.controlFrame.place(x=0, y=460)
        self.initControlUI()

    def initCoursesListlUI(self):
        canvas=tk.Canvas(self.coursesFrame,width=780,height=460,scrollregion=(0,0,780,460*5), bg = "#505050")
        canvas.place(x = 10, y = 0) #放置canvas的位置
        self.courseListFrame=tk.Frame(canvas, bg = "#505050") #把frame放在canvas裏
        self.courseListFrame.place(x=0, y=100,width=700,height=460*5) #frame的長寬，和canvas差不多的
        self.courseCheckButtons = []
        self.courseCheckButtonsVar = []

        vbar=tk.Scrollbar(canvas,orient=tk.VERTICAL) #豎直滾動條
        vbar.place(x = 760,width=20,height=440)
        vbar.configure(command=canvas.yview)
        hbar=tk.Scrollbar(canvas,orient=tk.HORIZONTAL)#水平滾動條
        hbar.place(x =0,y=440,width=760,height=20)
        hbar.configure(command=canvas.xview)

        canvas.config(xscrollcommand=hbar.set,yscrollcommand=vbar.set) #設置  
        canvas.create_window((700/2,460*5/2), window=self.courseListFrame)  #create_window

    def initControlUI(self):
        # messageLabel for error message
        self.messageVar = tk.StringVar()
        self.messageVar.set("Hello!!")
        messageLabel = tk.Label(self.controlFrame, textvariable=self.messageVar, bg = "#505050", fg="#e0e0e0")
        messageLabel.place(x=0, y=120, width=800, height=20)

        # button for start or stop choose course
        self.startButton = tk.Button(self.controlFrame, text='開始選課', font=("Arial", 20), bg="#404040", fg="#e0e0e0",
                                command=self.startChooseCourse)
        self.startButton.place(x=640, y=5, width=160, height=80)

        threadNumLabel = tk.Label(self.controlFrame, text='執行敘數量:', font=("Arial", 12), bg="#404040", fg="#e0e0e0").place(x=490, y=5, width=110, height=30)
        self.threadNumInput = tk.Spinbox(self.controlFrame, font=("Arial", 12), from_=1, to=10)
        self.threadNumInput.place(x=590, y=5, width=40, height=30)

        addIntervalLabel = tk.Label(self.controlFrame, text='加選間隔(s)', font=("Arial", 12), bg="#404040", fg="#e0e0e0").place(x=490, y=40, width=110, height=30)
        self.addIntervalInput = tk.Spinbox(self.controlFrame, font=("Arial", 12), from_=0, to=60)
        self.addIntervalInput.place(x=590, y=40, width=40, height=30)

        # list to select 課程加退選 or 電腦抽選後選課
        self.modeMenubutton = tk.Menubutton(self.controlFrame, text='課程加退選', font=("Arial", 12), bg="#505050", fg="#e0e0e0")
        self.mode = "課程加退選"
        self.modeMenubutton.menu =  tk.Menu ( self.modeMenubutton, tearoff = 0 )
        self.modeMenubutton["menu"] =  self.modeMenubutton.menu
        def modeMenubuttonCB(s):
            self.modeMenubutton.config(text=s)
            self.mode = s
        self.modeMenubutton.menu.add_radiobutton ( label="電腦抽選後選課", command=lambda s="電腦抽選後選課":modeMenubuttonCB(s))
        self.modeMenubutton.menu.add_radiobutton ( label="課程加退選", command=lambda s="課程加退選":modeMenubuttonCB(s))
        self.modeMenubutton.place(x=640, y=90, width=160, height=20)

        # for manually add a course to list
        tk.Label(self.controlFrame, text="課程代碼:", font=("Arial", 12), bg="#404040", fg="#e0e0e0").place(x=0, y=5, width=80, height=30)
        self.courseIdInput = tk.Entry(self.controlFrame, font=("Arial", 12))
        self.courseIdInput.place(x=80, y=5, width=120, height=30)
        addCourseButton = tk.Button(self.controlFrame, text='新增課程', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                    command=self.addCourse)
        addCourseButton.place(x=200, y=5, width=80, height=30)

        # show semester
        semesters = self.Querycourse.getSemesters()
        tk.Label(self.controlFrame, text=f"學年期:{semesters}", font=("Arial", 12), bg="#404040", fg="#e0e0e0").place(x=280, y=5, width=100, height=30)

        # tools fot select course
        selectAllButton = tk.Button(self.controlFrame, text='選取全部', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=self.selectAll)
        selectAllButton.place(x=0, y=40, width=100, height=30)
        selectInvertButton = tk.Button(self.controlFrame, text='反向選取', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=self.selectInvert)
        selectInvertButton.place(x=100, y=40, width=100, height=30)
        selectDeleteButton = tk.Button(self.controlFrame, text='刪除選取項目', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=self.selectDelete)
        selectDeleteButton.place(x=200, y=40, width=100, height=30)


        # tools with ntust's querycourse page
        importButton = tk.Button(self.controlFrame, text='匯入帶選課程', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=self.importViewList)
        importButton.place(x=0, y=80, width=100, height=30)

        # show weather user logined
        self.loginButton = None
        def loginButtonCB():
            urlDict = {
                "電腦抽選後選課" : config.ntust_prereg2JoinUrl,
                "課程加退選" : config.ntust_adddropJoinUrl
            }
            if self.Querycourse.checkLogin() and self.Querycourse.checkAddLogin(url=urlDict[self.mode]):
                print("成功登入")
                self.loginButton.config(text="成功登入")
            else:
                print("尚未登入")
                self.loginButton.config(text="尚未登入")
        self.loginButton = tk.Button(self.controlFrame, text='尚未登入', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=loginButtonCB)
        self.loginButton.place(x=100, y=80, width=100, height=30)

        # cookies source
        cookieSourceLabel = tk.Label(self.controlFrame, text='Cookies來源:', font=("Arial", 12), bg="#404040", fg="#e0e0e0").place(x=200, y=80, width=100, height=30)
        self.cookieSourceMenubutton = tk.Menubutton(self.controlFrame, text='None', font=("Arial", 12), bg="#505050", fg="#e0e0e0")
        self.cookieSourceMenubutton.menu =  tk.Menu ( self.cookieSourceMenubutton, tearoff = 0 )
        self.cookieSourceMenubutton["menu"] =  self.cookieSourceMenubutton.menu
        def cookieSourceMenubuttonCB(s : str):
            if s == "None":
                self.messageVar.set(f"Please select a browser")
                return
            self.cookieSourceMenubutton.config(text=s)
            try:
                if s=="Chrome":
                    self.Querycourse.cookies = browser_cookie3.chrome()
                if s=="Firefox":
                    self.Querycourse.cookies = browser_cookie3.firefox()
                if s=="Opera":
                    self.Querycourse.cookies = browser_cookie3.opera()
                if s=="Edge":
                    self.Querycourse.cookies = browser_cookie3.edge()
                if s=="Chromium":
                    self.Querycourse.cookies = browser_cookie3.chromium()
                if s=="Brave":
                    self.Querycourse.cookies = browser_cookie3.brave()
                if s=="Vivaldi":
                    self.Querycourse.cookies = browser_cookie3.vivaldi()
                if s=="Safari":
                    self.Querycourse.cookies = browser_cookie3.safari()
                self.messageVar.set(f"Success on loading {s} cookie")
                loginButtonCB()
            except:
                self.messageVar.set(f"Failed to find {s} cookie")
                
        for browserName in ["Chrome", "Firefox", "Opera", "Edge", "Chromium", "Brave", "Vivaldi", "Safari"]:
            self.cookieSourceMenubutton.menu.add_radiobutton ( label=browserName, command=lambda s=browserName:cookieSourceMenubuttonCB(s))
        self.cookieSourceMenubutton.place(x=300, y=80, width=100, height=30)

        def cookieSourceReloadButtonCB():
            browserName = self.cookieSourceMenubutton.cget("text")
            cookieSourceMenubuttonCB(browserName)
        cookieSourceReloadButton = tk.Button(self.controlFrame, text='重新載入Cookies', font=("Arial", 12), bg="#505050", fg="#e0e0e0",
                                command=cookieSourceReloadButtonCB)
        cookieSourceReloadButton.place(x=400, y=80, width=140, height=30)



    def run(self):
        self.window.mainloop()

        # closing
        self.Querycourse.saveUserdata()

        if self.Querycourse.chooseTaskFlag:
            self.Querycourse.stopChooseCoures()
            self.Querycourse.waitToStopTask()
            self.startButton.config(text="開始選課")

    def addCourse(self, courseID = None):
        if courseID is None:
            courseID = self.courseIdInput.get()

        print(courseID)
        try:
            # 整理字串
            courseID = courseID.upper().strip()
            # 取得課程資料
            data = self.Querycourse.getCourseDetial(courseID)[0]
            print(data)
            if "CourseNo" not in data:
                raise

            selectedID = [ courseData['CourseNo'] for courseData in self.Querycourse.courseList ]
            if courseID in selectedID:
                self.messageVar.set(f"課程[{data['CourseNo']}-{data['CourseName']}]以於清單內")
                return

            self.messageVar.set(f"新增課程[{data['CourseNo']}-{data['CourseName']}]")

            # 加入課程清單
            data["autoChoose"] = False
            self.Querycourse.courseList.append(data)

            # 更新GUI
            self.updateCourselist()
        except:
            self.messageVar.set(f"無效課程代碼[{courseID}]")

    def selectAll(self):
        reverse = True
        for courseData in self.Querycourse.courseList:
            reverse = reverse and courseData["autoChoose"]
        for courseData in self.Querycourse.courseList :
            courseData["autoChoose"] = not reverse
        self.updateCourselist()
    
    def selectInvert(self):
        for courseData in self.Querycourse.courseList :
            courseData["autoChoose"] = not courseData["autoChoose"]
        self.updateCourselist()

    def selectDelete(self):
        removeIdices = []
        for i, courseData in enumerate( self.Querycourse.courseList ):
            if courseData["autoChoose"]:
                removeIdices.append(i)
        removeIdices.reverse()
        for removeIdx in removeIdices:
            self.Querycourse.courseList.pop(removeIdx)
        self.updateCourselist()

    def importViewList(self):
        if not self.Querycourse.checkLogin():
            self.messageVar.set("Login Fail")
            return

        # 讀取待選清單
        Semester = self.Querycourse.getSemesters()
        viewListID = []
        for data in self.Querycourse.getViewlist():
            if(data['Semester'] != Semester):
                continue
            viewListID.append(data["CourseNo"])
        
        selectedID = [ courseData['CourseNo'] for courseData in self.Querycourse.courseList ]

        addCount = 0
        errCount = 0
        for courseID in viewListID:
            try:
                data = self.Querycourse.getCourseDetial(courseID)[0]
                if courseID in selectedID:
                    continue
                data["autoChoose"] = False
                self.Querycourse.courseList.append(data)
                addCount = addCount + 1
            except:
                errCount = errCount + 1

        self.messageVar.set(f"已新增{addCount}門課程，{errCount}門失敗")
        self.updateCourselist()

    def updateCourselist(self):
        for chkbtn in self.courseCheckButtons:
            chkbtn.destroy()
        self.courseCheckButtons.clear()
        self.courseCheckButtonsVar.clear()

        for i, courseData in enumerate( self.Querycourse.courseList ):
            showText = f"{courseData['CourseNo']:>10s} {courseData['CourseTeacher']:>6s} {courseData['CourseName']:>20s}"
            newVar = tk.IntVar()
            if courseData['autoChoose']:
                newVar.set(1)
            newChkbtn = tk.Checkbutton(self.courseListFrame, text=showText, font=("Syne Mono", 20), bg = "#505050", fg="#e0e0e0", 
                                        variable=newVar, onvalue=1, offvalue=0,
                                        command=lambda idx=i:self.courseChkbtnCB(idx))
            newChkbtn.grid(row=i, column=0, sticky="W")
            #newChkbtn.pack(side=tk.TOP)

            self.courseCheckButtons.append(newChkbtn)
            self.courseCheckButtonsVar.append(newVar)

    def courseChkbtnCB(self, idx):
        self.Querycourse.courseList[idx]["autoChoose"] = bool(self.courseCheckButtonsVar[idx].get())
        print(self.Querycourse.courseList[idx]["CourseNo"], self.Querycourse.courseList[idx]["autoChoose"])

    def checkLoginStatusTask(self):
        urlDict = {
                "電腦抽選後選課" : config.ntust_prereg2JoinUrl,
                "課程加退選" : config.ntust_adddropJoinUrl
            }
        while self.Querycourse.chooseTaskFlag:
            if self.Querycourse.checkLogin() and self.Querycourse.checkAddLogin(url=urlDict[self.mode]):
                pass
            else:
                self.Querycourse.stopChooseCoures()
                self.Querycourse.waitToStopTask()
                self.startButton.config(text="開始選課")
                break

    def startChooseCourse(self):
        if self.Querycourse.chooseTaskFlag:
            self.Querycourse.stopChooseCoures()
            self.Querycourse.waitToStopTask()
            self.startButton.config(text="開始選課")
        else:
            self.startButton.config(text="停止選課")

            selectedIDs = []
            for i, var in enumerate(self.courseCheckButtonsVar) :
                if var.get():
                    courseData = self.Querycourse.courseList[i]
                    selectedIDs.append(courseData['CourseNo'])

            urlDict = {
                "電腦抽選後選課" : config.ntust_prereg2JoinUrl,
                "課程加退選" : config.ntust_adddropJoinUrl
            }

            thNum = 1
            try:
                thNum = int(self.threadNumInput.get())
            except:
                pass
            addInterval = 5
            try:
                addInterval = float(self.addIntervalInput.get())
            except:
                pass
            self.Querycourse.startChooseCoures( nTasks=thNum,
                                                courseIdList=selectedIDs, 
                                                url=urlDict[self.mode], 
                                                delay=addInterval)

            threading.Thread(target=self.checkLoginStatusTask).start()