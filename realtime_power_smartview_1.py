# -*- config:utf-8 -*-
# 파워플래너 실시간(15분 간격) 전력 및 효율 감시

from selenium import webdriver
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
from tkinter import *
import time
import cv2
import os
from PIL import ImageFont
import datetime


root = Tk()

monitor_height = root.winfo_screenheight()
monitor_width = root.winfo_screenwidth()

font_path = 'C:/Windows/Fonts/BareunBatangPro1.ttf'
font = fm.FontProperties(fname=font_path, size=12)

options = webdriver.ChromeOptions()
options.add_argument("headless")
ss = '--window-size='+str(monitor_width)+','+str(monitor_height)
options.add_argument(ss)

options.add_experimental_option('excludeSwitches', ['enable-logging'])

#while True:
#URL_1 = 'https://pp.kepco.co.kr/rm/rm0101.do?menu_id=O010101'
URL_1 = 'https://pp.kepco.co.kr/intro.do'

driver = webdriver.Chrome(executable_path='C:/Python/chromedriver_4664', options=options)
#driver = webdriver.Chrome(executable_path='C:/Python/chromedriver_4664')
#driver.implicitly_wait(5)


driver.get(URL_1)
driver.implicitly_wait(3) # <- 키 포인트

if driver.find_element_by_xpath('//*[@id="notice_title"]') is True:
    driver.find_element_by_xpath('//*[@id="notice_auto_popup"]/div[3]/label').click()
    
#driver.find_element_by_xpath('//*[@id="primary-button"]').click()
driver.implicitly_wait(3) # <- 키 포인트
time.sleep(10)

#driver = webdriver.Chrome(executable_path='C:/Python/chromedriver_4664', options=options)
#driver = webdriver.Chrome(executable_path='C:/Python/chromedriver_4664')

driver.get(URL_1)
driver.implicitly_wait(3) # <- 키 포인트
time.sleep(10)
driver.maximize_window()

# 아이디/비밀번호를 입력해준다.
id = driver.find_element_by_id("RSA_USER_ID")
pwd = driver.find_element_by_id("RSA_USER_PWD")

id.send_keys('0227465025')
pwd.send_keys('a45924592')

# 로그인 버튼을 누르기
driver.find_element_by_xpath('//*[@id="intro_form"]/form/fieldset/input[1]').click()

while True:
    URL_2 = 'https://pp.kepco.co.kr/rm/rm0101.do?menu_id=O010101'
    driver.get(URL_2)
    driver.implicitly_wait(3) # <- 키 포인트
    time.sleep(5)
    
    now = datetime.datetime.now()
    print(now)
    
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(5)
    
    if os.path.isfile('screen_1.png'):
        os.remove('screen_1.png')
    
    driver.save_screenshot('screen_1.png')
    time.sleep(1)
    img_1 = cv2.imread('screen_1.png')
    
    driver.execute_script("window.scrollTo(0, 700)")
    time.sleep(5)
    
    if os.path.isfile('screen_2.png'):
        os.remove('screen_2.png')
    
    driver.save_screenshot('screen_2.png')
    time.sleep(1)
    img_2 = cv2.imread('screen_2.png')

    driver.find_element_by_xpath('//*[@id="day"]').click()
    #driver.implicitly_wait(3) # <- 키 포인트
    time.sleep(5)
    
    if os.path.isfile('screen_3.png'):
        os.remove('screen_3.png')
    
    driver.save_screenshot('screen_3.png')
    time.sleep(1)
    img_3 = cv2.imread('screen_3.png')
    
    #cv2.imshow('money_view', money_view)
    #cv2.imshow('kwh_view', kwh_view)
    #cv2.imshow('sum_view', sum_view)
    
    # 표현시 각 이미지간 지연이 없도록 한번에 처리함.
    
    money_view = img_1[222:510, 452:1132, :]
    x1, y1, c1 = money_view.shape
    
    unit_view = img_1[540:800, 460:830, :]
    x2, y2, c2 = unit_view.shape
    
    kwh_view = img_2[486:850, 452:1450, :]
    x3, y3, c3 = kwh_view.shape
    
    days_view = img_3[486:850, 452:1450, :]
    x4, y4, c4 = days_view.shape
    
    sss = np.ones((x3+x3, y1+y3, 3))*255
    sss[:x1, :y1, :] = money_view
    sss[(x1+int(x2/4)):(x1+x2+int(x2/4)), int(y1/4):(int(y1/4)+y2), :] = unit_view
    sss[:x3, y1:(y1+y3), :] = kwh_view
    sss[x3:(x3+x3), y1:(y1+y3), :] = days_view
    
    res = np.array(sss, dtype=np.uint8)
    img = cv2.resize(res, dsize=(monitor_width, int(monitor_height)))
    
    winname = 'POWER MONITORING by S.H, Kim'
    cv2.namedWindow(winname)   # create a named window
    cv2.moveWindow(winname, 0, 0)   # Move it to (40, 30)
    cv2.imshow(winname, img)
    
    if cv2.waitKey(10000) == 27:
        break

