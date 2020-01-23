from selenium import webdriver
from PIL import Image

import IPython.display as Imm

# try:
#     from PIL import Image
# except ImportError:
#     import Image
import pytesseract

import shutil

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import UnexpectedAlertPresentException

import os
import sys

success = False

import time
from threading import Thread

import personalInf

q = None
cookieValue = None
def check():
    while True:
        time.sleep(2)
        
        if cookieValue != None:
            driver.execute_script("countSecond = 3000")
            time.sleep(2)
            # driver.save_screenshot('test.png')
            # print(driver.get_log('browser'))
            if q == "q":
                return
            print('\n\ncookieValue: \n', cookieValue)
            print("\nSet countSecond value = 3000 \nPress \"q\" to exit: ", end="")
        else:
            print("Loading")

t = Thread(target = check)
t.start()

while success != True:
#     driver = webdriver.Chrome()

    chromedriverPath = shutil.which("chromedriver")
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("window-size=1200x600")

    driver = webdriver.Chrome(chromedriverPath, options=options)
    driver.get("http://cos1.ntnu.edu.tw/AasEnrollStudent/LoginCheckCtrl?language=TW") 
    
    driver.save_screenshot('capture.png')
    vfImg = driver.find_element_by_id("imageBoxCmp")

    # left = vfImg.location['x']
    # right = left + vfImg.size['width']
    # top = vfImg.location['y']
    # bottom = top + vfImg.size['height']
    left = vfImg.location['x']+895
    right = left + vfImg.size['width']+50
    top = vfImg.location['y']+215
    bottom = top + vfImg.size['height']+20

    img = Image.open('capture.png')
    img = img.crop((left, top, right, bottom))
    img.save('vfImg.png', 'png')
    os.remove('capture.png')


    code = pytesseract.image_to_string(Image.open('vfImg.png'))
    code = code.lower().translate({ord(i): None for i in '\n '})
    os.remove('vfImg.png')
    # print(code)
    if len(code) != 4 or code.isalpha() != True:
        print("Verification code format does not match !")
        driver.close()
        continue
#     code = code.lower().translate({ord(i): None for i in '\n '})
    # print(code)

    elem_user = driver.find_element_by_id("userid-inputEl")
    elem_user.send_keys(personalInf.studentID)
    elem_pwd = driver.find_element_by_name("password")
    elem_pwd.send_keys(personalInf.password)
    elem_vf = driver.find_element_by_id("validateCode-inputEl")
    elem_vf.send_keys(code)

    try:
        driver.find_element_by_id("button-1016-btnWrap").click()
    except:
        # print("Loading too much time!")
        print("err")
        driver.close()
        continue


    delay = 10 # seconds
    try:
        fastrack = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'button-1017-btnWrap')));
        fastrack.click()
        cookieValue = str(driver.get_cookies()[0]["value"])
        print('cookieValue: \n', cookieValue)
        while True:
            q = input("Press \"q\" to exit: ")

            if q == "q":
                success = True

                # driver.close()
                break

#         driver.close()
    except TimeoutException:
        print("Loading too much time!")
        driver.close()
        print("Reloading Page")
        continue
    except UnexpectedAlertPresentException as err:
        # print("Loading took too much time!")
        # print(type(err))    # the exception instance
        # print("aa", err.args)     # arguments stored in .args
        # print("bb", err.args)
        print("code: ", code)
        print(err)
        driver.close()
        print("Reloading Page")
        continue
    except:
        print("Error")
        driver.close()
        print("Reloading Page")
        continue

try:
    # t.raise_exception()

    # t.join()
    driver.close()
    print("\nClosing browser!!\n")
    # sys.exit()
    
except:
    print("Close browser!!")

