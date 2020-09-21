# Author : Pratik Shinde

from selenium import webdriver
from datetime import datetime
import time
import pause
from selenium.webdriver.chrome.options import Options

EMAIL_ID = ""
PASSWORD = ""

subjects = ['MOSC', "wiz-wqmp-qui",
            'VLSI', "zej-uoht-yxa"]
classes = ["monday", "MOSC", 12,
           "tuesday", "MOSC", 8,
           "tuesday", "VLSI", 12,
           "wednesday", "MOSC", 12,
           "thursday", "VLSI", 14,
           "friday", "VLSI", 14]
days = [
    'sunday', 'monday', 'tuesday', 'wednesday',
    'thursday', 'friday', 'saturday']


def join_meeting(lecture, url):
    email_input = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[" \
                  "1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input "
    next_button = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[" \
                  "1]/div/div/button/div[2] "
    password_input = "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[" \
                     "1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input "
    close_button = "#yDmH0d > div.llhEMd.iWO5td > div > div.g3VIld.B2Jb7d.Up8vH.hFEqNb.J9Nfi.iWO5td > " \
                   "div.R6Lfte.es33Kc.TNczib.X1clqd > div.bZWIgd > div > span > span > svg "
    dismiss_button = "/html/body/div[1]/div[3]/div/div[2]/div[3]/div/span/span"
    join_button = "/html/body/div[1]/c-wiz/div/div/div[5]/div[3]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div[" \
                  "1]/span/span "
    end_button = "/html/body/div[1]/c-wiz/div[1]/div/div[5]/div[3]/div[9]/div[2]/div[2]/div"
    
    print('Joining ' + lecture[1] + ' class')
    
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option("prefs", {"profile.default_content_setting_values.media_stream_mic": 2,
                                                     "profile.default_content_setting_values.media_stream_camera": 2,
                                                     "profile.default_content_setting_values.notifications": 2
                                                     })
    driver = webdriver.Chrome(options=chrome_options)
    # driver = webdriver.Chrome(executable_path='C:\chromedriver.exe', options=chrome_options)
    
    # Google login
    driver.get('https://accounts.google.com/signin')
    driver.find_element_by_xpath(email_input).send_keys(EMAIL_ID)
    driver.find_element_by_xpath(next_button).click()
    time.sleep(3)
    driver.find_element_by_xpath(password_input).send_keys(PASSWORD)
    driver.find_element_by_xpath(next_button).click()
    time.sleep(3)

    # Join meeting
    time.sleep(5)
    driver.get("https://meet.google.com/" + url)
    time.sleep(3)
    
    try:
        driver.find_element_by_css_selector(close_button).click()
        time.sleep(1)
    except:
        pass
    try:
        driver.find_element_by_xpath(dismiss_button).click()
        time.sleep(1)
    except:
        pass
    
    driver.find_element_by_xpath(join_button).click()
    time.sleep(1)
    print("You're in the class..")
    time.sleep(3600)
    
    # End meeting
    driver.find_element_by_xpath(end_button).click()
    driver.close()


def queue(lecture):
    # Get calendar details for today
    year = int(datetime.today().strftime('%Y'))
    month = int(datetime.today().strftime('%m'))
    date = int(datetime.today().strftime('%d'))
    hour = int(datetime.today().strftime('%H'))
    
    # Get Google meet url
    url = subjects[subjects.index(lecture[1]) + 1]
    
    if hour < lecture[0]:
        print(lecture[1] + ' class is at ' + str(lecture[0]) + '00 IST. Waiting..')
        # Pause until lecture starts
        pause.until(datetime(year, month, date, lecture[0]))
        join_meeting(lecture, url)
    else:
        join_meeting(lecture, url)


def good_to_go():
    index = 0
    flag = True
    if len(EMAIL_ID) < 1:
        print("Please enter valid Email ID")
    if len(PASSWORD) < 1:
        print("Please enter valid Password")
    while index < len(classes):
        if not days.__contains__(classes[index].lower()):
            print(str(classes[index]) + ' is not a valid day')
            flag = False
        index += 1
        if not subjects.__contains__(classes[index]):
            print(str(classes[index]) + ' is not a valid subject')
            flag = False
        index += 1
        if not 0 < classes[index] < 23:
            print(str(classes[index]) + ' is not a valid time')
            flag = False
        index += 1
    return flag


def todays_schedule():
    # Get calendar details for today
    hour = int(datetime.today().strftime('%H'))
    day = datetime.today().strftime('%A')
    schedule = []
    for item in range(0, len(classes), 3):
        if classes[item] == day.lower():
            class_end_time = classes[item + 2] + 1
            print(classes[item + 1] + ' class ended at ' + str(class_end_time) + '00 IST.') if class_end_time <= hour \
                else schedule.append([classes[item + 2], classes[item + 1]])
    return schedule


#
# Mainline starts here
#

if good_to_go():
    todays_schedule = sorted(todays_schedule())
    print('Chill.. No more classes today !!') if len(todays_schedule) == 0 \
        else [queue(lectures) for lectures in sorted(todays_schedule)]
