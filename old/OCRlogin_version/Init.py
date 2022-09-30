from configparser import ConfigParser
def creatConfig():
	cfg = ConfigParser()
	cfg.write(open('myapp.ini','w'))
	cfg.read('myapp.ini')

	cfg.add_section('UserName')
	cfg.set('UserName','UserName',input('UserName:'))
	cfg.set('UserName','Password',input('Password:'))

	cfg.add_section('Courses')
	cfg.set('Courses','Password','1082')
	n=0
	CourseNo = ''
	while(True):
		r = input('Course'+str(n)+'No:')
		CourseNo= CourseNo + ',' + r
		if(len(r)==0):
			break
		n = n+1
	CourseNo = CourseNo[1:]
	cfg.set('Courses','CourseNo',CourseNo)

	cfg.add_section('LineNotify')
	cfg.set('LineNotify','Line_token',input('Line token:'))

	cfg.write(open('myapp.ini','w'))
cfg = ConfigParser()
cfg.read('myapp.ini')