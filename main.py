from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import data
import time
import datetime

options = Options()
options.add_argument("--disable-infobars")

options.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block
    "profile.default_content_setting_values.geolocation": 2,          # 1:allow, 2:block
    "profile.default_content_setting_values.notifications": 2         # 1:allow, 2:block
  })

print("Here's the sequence\n")

for i in range(len(data.timing)):
    print("{}'s meeting at {} with code {}".format(data.subject[i],data.timing[i],data.code[i]))


print("\nSequence starting in 10 Seconds")
time.sleep(10)

driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://meet.google.com/')

def login():
    try:
        sign_in_button = driver.find_element_by_xpath("//a[@event-action='sign in']")
        sign_in_button.click()
        driver.implicitly_wait(15)
        email_input = driver.find_element_by_xpath("//input[@type='email']")
        email_input.send_keys(data.email)
        email_input.send_keys(Keys.ENTER)
        password_input = driver.find_element_by_xpath("//input[@name='password']")
        password_input.send_keys(data.password)
        password_input.send_keys(Keys.ENTER)
        print("Login Successful")
    except:
        print("Login Failed")


def enter_meeting(code):
    try:
        code_input = driver.find_element_by_xpath("//input[@placeholder='Enter a code or link']")
        code_input.send_keys(code)
        code_input.send_keys(Keys.ENTER)
        microphone = driver.find_element_by_xpath("//div[@class='sUZ4id']")
        microphone.click()
        video = driver.find_element_by_xpath("//div[@class='GOH7Zb']")
        video.click()
        join_button = driver.find_element_by_xpath("//div[@role='button']//span[contains(text(), 'Ask to join')]")
        join_button.click()
        print("Successfully joined the meeting with code {}".format(code))
    except:
        print("Error joining the meeting")

def exit_meeting():
    try:
        driver.get('https://meet.google.com/')
        print("Meeting Left")
    except:
        print("Error leaving the meeting")


def time():
    right_now = datetime.datetime.now()
    current_time = right_now.strftime("%H:%M")
    return current_time


def start():
    timing = data.timing
    leaving = data.leave_timing
    class_attended = 0
    login()
    while len(leaving) != 0:
        if time() in timing:
            enter_meeting(data.code[timing.index(time())+class_attended])
            timing.pop(timing.index(time()))
            class_attended += 1
        if time() in leaving:
            exit_meeting()
            leaving.pop(leaving.index(time()))

start()
print("\n\nSequence Completed.")

