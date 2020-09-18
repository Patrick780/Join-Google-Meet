from selenium import webdriver
from datetime import datetime
import time
import pause

USERNAME = ""
PASSWORD = ""

mosc_metting_url = "https://meet.google.com/wiz-wqmp-qui"
mosc_class_days = [1, 2, 3]
mosc_class_time = [12, 8, 12]

vlsi_meeting_url = "https://meet.google.com/zej-uoht-yxa"
vlsi_class_days = [2, 4, 5]
vlsi_class_time = [13, 14, 14]

year = int(datetime.today().strftime('%Y'))
month = int(datetime.today().strftime('%m'))
date = int(datetime.today().strftime('%d'))
hour = int(datetime.today().strftime('%H'))
day = datetime.today().weekday() + 1
mosc_joining_time = 0
vlsi_joining_time = 0


def join_meeting(google_meet_url):
    driver = webdriver.Chrome()
    
    # Google login
    driver.get('https://accounts.google.com/signin')
    
    username = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div["
        "1]/div/div[1]/div/div[1]/input")
    username.send_keys(USERNAME)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]").click()
    time.sleep(3)
    
    password = driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div["
        "1]/div[1]/div/div/div/div/div[1]/div/div[1]/input")
    password.send_keys(PASSWORD)
    driver.find_element_by_xpath(
        "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button/div[2]").click()
    time.sleep(3)
    
    # Join meeting
    time.sleep(5)
    driver.get(google_meet_url)
    time.sleep(3)
    
    try:
        close_popup = driver.find_element_by_css_selector("#yDmH0d > div.llhEMd.iWO5td > div > "
                                                          "div.g3VIld.B2Jb7d.Up8vH.hFEqNb.J9Nfi.iWO5td > "
                                                          "div.R6Lfte.es33Kc.TNczib.X1clqd > div.bZWIgd > div > span "
                                                          "> span > svg")
        close_popup.click()
        time.sleep(1)
    except:
        pass
    try:
        dismiss = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div[3]/div/span/span")
        dismiss.click()
        time.sleep(1)
    except:
        pass
    
    driver.find_element_by_xpath(
        "/html/body/div[1]/c-wiz/div/div/div[5]/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span/span").click()
    time.sleep(1)
    
    print("You're in the class..")
    time.sleep(3600)
    driver.find_element_by_xpath("/html/body/div[1]/c-wiz/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div").click()
    
    driver.close()


def join_mosc(mosc_joining_time):
    print("MOSC class is at " + str(mosc_joining_time) + " IST. Waiting..")
    pause.until(datetime(year, month, date, mosc_joining_time))
    # join_meeting(mosc_metting_url)


def join_vlsi(vlsi_joining_time):
    print("VLSI class is at " + str(vlsi_joining_time) + " IST. Waiting..")
    pause.until(datetime(year, month, date, vlsi_joining_time))
    # join_meeting(vlsi_meeting_url)


if not mosc_class_days.__contains__(day) and not vlsi_class_days.__contains__(day):
    print("Chill.. There are no classes today!")
    exit()

mosc = False
vlsi = False
if mosc_class_days.__contains__(day):
    mosc_joining_time = mosc_class_time[mosc_class_days.index(day)]
    if hour >= mosc_joining_time + 1:
        print('MOSC class was at ' + str(mosc_joining_time) + ' IST. It\'s already over')
    else:
        mosc = True

if vlsi_class_days.__contains__(day):
    vlsi_joining_time = vlsi_class_time[vlsi_class_days.index(day)]
    if hour >= vlsi_joining_time + 1:
        print('VLSI class was at ' + str(vlsi_joining_time) + ' IST. It\'s already over')
    else:
        vlsi = True

if not mosc and not vlsi:
    print("No more classes today!")
    exit()
if vlsi and not mosc:
    join_vlsi(vlsi_joining_time)
    print("VLSI class over!")
    exit()
if mosc and not vlsi:
    join_mosc(mosc_joining_time)
    print("MOSC class over!")
    exit()
else:
    if vlsi_joining_time < mosc_joining_time:
        join_vlsi(vlsi_joining_time)
        print("VLSI class over!")
        join_mosc(mosc_joining_time)
        print("MOSC class over!")
        exit()
    else:
        join_mosc(mosc_joining_time)
        print("MOSC class over!")
        join_vlsi(vlsi_joining_time)
        print("VLSI class over!")
        exit()
