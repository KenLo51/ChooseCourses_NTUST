# std libraries
import subprocess
import requests

#
import browser_cookie3

# user libraries
import config
import NTUSTquerycourse
from mainWindow import *


if __name__ == "__main__":
    # subprocess.run([config.browserPath_Chrome, config.ntust_mainUrl])
    #cj = browser_cookie3.chrome()
    #r = requests.get("https://courseselection.ntust.edu.tw/ChooseList/D03/D03", cookies=cj)
    #print(r.content.decode("utf8"))

    # print(NTUSTquerycourse.getCourseDetial("ET3010701"))

    # print(NTUSTquerycourse.getViewlist())

    mw = mainWindow()
    mw.run()
    