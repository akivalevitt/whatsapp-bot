import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

from app.utils import aiPart

from dotenv import load_dotenv
from dotenv import set_key

from flask import current_app, jsonify

import os

def runBot(message):
        
    #member = eval(aiPart.dictOfBankDetails(message))
    member=message
    print(message)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    
    driver.get("https://www.fnb.co.za/")

    soup= BeautifulSoup(driver.page_source, features='lxml')

    username = driver.find_element("xpath",'//*[@id="user"]')
    password = driver.find_element("xpath",'//*[@id="pass"]')

    username.send_keys(member["Username"])
    password.send_keys(os.getenv("PASS"))
    

    loginButton = driver.find_element("xpath",'//*[@id="OBSubmit"]')
    loginButton.click()

    time.sleep(2)
    # print("\nTESTING TIMER\n")
    # time.sleep(4)
    # myname = driver.find_element("xpath",'//*[@id="welcomeContainer"]/div')
    # print(myname.text)
    # cookies = driver.get_cookies()
    # # pickle.dump(cookies,open("cookies.pkl","wb"))
    # print(cookies)

    headings=soup.find_all(name='h2')
    for heading in headings:
        print(heading.getText())

        # Wait for the element to be present before attempting to find it
    onceOffButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="whatsNewContainer"]/ul/li[2]/a'))
    )
        

    # # paymentsButton = driver.find_element("xpath",'//*[@id="shortCutLinks"]/span[3]')
    # paymentsButton = driver.find_element("xpath",'//*[@id="newsLanding"]/div[3]/ul/li[4]/div')
    # paymentsButton.click()
    # time.sleep(2)


    # onceOffButton = driver.find_element("xpath",'//*[@id="subTabsScrollable"]/div[2]')
    # onceOffButton.click()
        

    onceOffButton = driver.find_element("xpath",'//*[@id="whatsNewContainer"]/ul/li[2]/a')
    onceOffButton.click()

    time.sleep(1)

    accountRecipientName = driver.find_element("xpath",'//*[@id="accountRecipientName"]')
    branchSearchCode= driver.find_element("xpath",'//*[@id="branchSearchCode"]')
    accountNumber = driver.find_element("xpath",'//*[@id="accountNumber"]')
    accountHowMuch = driver.find_element("xpath",'//*[@id="accountHowMuch"]')
    accountTheirReference = driver.find_element("xpath",'//*[@id="accountTheirReference"]')
    accountMyReference = driver.find_element("xpath",'//*[@id="accountMyReference"]')
    methodContactInput0 = driver.find_element("xpath",'//*[@id="methodContactInput0"]')


    accountRecipientName.send_keys(member["Account Info"]["name"])
    branchSearchCode.send_keys(member["Account Info"]["branch code"])
    accountNumber.send_keys(member["Account Info"]["account number"])
    accountHowMuch.send_keys(member["Amount"])
    accountTheirReference.send_keys(member["Name"])
    accountMyReference.send_keys('Ai automation')
    methodContactInput0.send_keys('akl343434@gmail.com')

    
    time.sleep(1)
    select = driver.find_element("xpath",'//*[@id="fromAnrfn_dropId"]')
    select.click()


    time.sleep(1)
    accountselection = driver.find_element("xpath",'//*[@id="fromAnrfn_parent"]/div[2]/div[2]/ul/li[2]')
    accountselection.click()

    print("\nSUCCESS BIG BIG BIG SUCCESS\n")
    print("\nSUCCESS BIG BIG BIG SUCCESS\n")
    print("\nSUCCESS BIG BIG BIG SUCCESS\n")
    print("\nSUCCESS BIG BIG BIG SUCCESS\n")

    # NB ONLY UNCOMMENT FOR ACTUAL PAYMENT
    time.sleep(1)
    pay = driver.find_element("xpath",'//*[@id="mainBtnHref"]')
    pay.click()

    # only deactivate at end

    time.sleep(1)
    confirm = driver.find_element("xpath",'//*[@id="footerButtonsContainer"]/div[3]/a')
    confirm.click()

    time.sleep(30)
    logout= driver.find_element("xpath",'//*[@id="headerButton_"]')
    logout.click()

    return member


