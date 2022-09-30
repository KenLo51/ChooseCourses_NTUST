import tkinter
import module
import threading


#url_getWhiteListing = 'https://drive.google.com/uc?id=1LF0jgOpSFb8W86cuHkI15VkMlJ5nHy91&export=download'
CourseList = []
config = {}
#WhiteListing = ()
def ChooseCourses_job():
	config['UserName']=UserName_Entry.get()
	config['Password']=Password_Entry.get()
	module.ChooseCourses(config)
def Start():
	for i in range(ChooseList_listbox.size()):
		CourseNo = ChooseList_listbox.get(i)
		CourseNo = CourseNo[0:9]
		try:
			config['CourseNo'][i] =CourseNo
		except:
			config['CourseNo'].append(CourseNo)
	print(config['CourseNo'])
	module.writeConfig(data = config)
	ChooseCourses_thread = threading.Thread(target = ChooseCourses_job)
	ChooseCourses_thread.start()


def InsertCourse():
	Cursor = CourseList_listbox.curselection()
	Course = CourseList_listbox.get(Cursor)
	ChooseList_listbox.insert(0 , Course )
	config['CourseNo'].insert( 0 , Course[0:Course.find(' ')] )
	CourseList_listbox.delete(Cursor)
def RemoveCourse():
	Cursor = ChooseList_listbox.curselection()
	Course = ChooseList_listbox.get(Cursor)
	CourseList_listbox.insert(0 , Course )
	config['CourseNo'].remove( Course[0:Course.find(' ')] )
	ChooseList_listbox.delete(Cursor)

def ImportCoursesList():
	for i in range(CourseList_listbox.size()):
		CourseList_listbox.delete(0)
	config['UserName']=UserName_Entry.get()
	config['Password']=Password_Entry.get()
	CourseList = module.GetCourseList(config['UserName'],config['Password'])
	for i in range(len(CourseList)):
		if(config['CourseNo'].count(CourseList[i]['CourseNo']) == 0):
			CourseList_listbox.insert( i , CourseList[i]['CourseNo'] + '     ' + CourseList[i]['CourseName'])
###init#############################################################################################
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

print(config)
###init#############################################################################################


###GUI#############################################################################################
windows = tkinter.Tk()
windows.title('Course Selection')
windows.geometry('800x600')
windows.resizable(False , False)

config_fm = tkinter.Frame(windows ,height = '40', width = '4')
config_fm.pack(side = 'left' )

UserName_Label = tkinter.Label(config_fm,text='UserName')
UserName_Label.pack( side = 'top' )
UserName_Entry = tkinter.Entry(config_fm)
UserName_Entry.pack( side = 'top' )
UserName_Entry.insert(0,config['UserName'])

Password_Label = tkinter.Label(config_fm,text='Password')
Password_Label.pack( side = 'top' )
Password_Entry = tkinter.Entry(config_fm)
Password_Entry.pack( side = 'top' )
Password_Entry.insert(0,config['Password'])

import_Btn = tkinter.Button(config_fm ,text='ImportCoursesList' , command = ImportCoursesList)
import_Btn.pack( side = 'top' )
#Start_Btn = tkinter.Button(windows ,text='Start' , command = getlis)
Start_Btn = tkinter.Button(config_fm ,text='Start' , height = '2' , width = '5' , command = Start)
Start_Btn.pack( side = 'bottom' )


Course_fm = tkinter.Frame(windows)
Course_fm.pack(side = 'right' )

Course_Label = tkinter.Label(Course_fm,text='待選清單                                                                                       選課清單')
Course_Label.pack( side = 'top' )
CourseList_listbox = tkinter.Listbox(Course_fm , height = '30' , width = '37')
CourseList_listbox.pack( side = 'left')
CourseBtn_fm = tkinter.Frame(Course_fm)
CourseBtn_fm.pack(side = 'left' )
insert_btn = tkinter.Button(CourseBtn_fm ,text='>>Insert>>', command = InsertCourse)
insert_btn.pack( side = 'top')
remove_btn = tkinter.Button(CourseBtn_fm ,text='<<Remove<<', command = RemoveCourse)
remove_btn.pack( side = 'top')
ChooseList_listbox = tkinter.Listbox(Course_fm , height = '30' , width = '37')
ChooseList_listbox.pack( side = 'right')


if(config['CourseNo'][0] != ''):
	for i in range(len(config['CourseNo'])):
		data = module.GetCourseData(config['CourseNo'][i])
		ChooseList_listbox.insert( i , data[0]['CourseNo'] + '     ' + data[0]['CourseName'])

ImportCoursesList()



###GUI#############################################################################################

##main###############################################################








windows.mainloop()