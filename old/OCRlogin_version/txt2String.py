from time import sleep
s1 = '/ / / / / / / / / /'
s2 = '\\ \\ \\ \\ \\ \\ \\ \\ \\ \\ \\'
while(True):
	for i in range(20):
		print(s1[i:])
		sleep(0.01)
	for i in range(20):
		print(s2[:i])
		sleep(0.01)
	#sleep(0.1)