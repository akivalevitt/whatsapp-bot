import time
import pickle
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

from app.utils import aiPart

from dotenv import load_dotenv
from dotenv import set_key

import os

def runBot(message):
        
    #member = eval(aiPart.dictOfBankDetails(message))
    member=message
    print(message)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    #options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    
    driver.get("https://www.fnb.co.za/")

    username = driver.find_element("xpath",'//*[@id="user"]')
    password = driver.find_element("xpath",'//*[@id="pass"]')

    username.send_keys(member["Username"])
    password.send_keys(os.getenv("PASSWORD"))

    loginButton = driver.find_element("xpath",'//*[@id="OBSubmit"]')
    loginButton.click()

    time.sleep(10)
    cookies = driver.get_cookies()
    # pickle.dump(cookies,open("cookies.pkl","wb"))
    print(cookies)

    #paymentsButton = driver.find_element("xpath",'//*[@id="rewardsContainerInner"]/a')
    paymentsButton = driver.find_element("xpath",'//*[@id="newsLanding"]/div[3]/ul/li[4]/div')
    paymentsButton.click()
    time.sleep(2)


    onceOffButton = driver.find_element("xpath",'//*[@id="subTabsScrollable"]/div[3]')
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
    methodContactInput0.send_keys('ak@gmail.com')

    
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
    # time.sleep(1)
    # pay = driver.find_element("xpath",'//*[@id="mainBtnHref"]')
    # pay.click()

    return member


