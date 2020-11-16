from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import os
from random import randrange
import time
import datetime

url = input("Enter Bestbuy URL: ")

def callInStock():
    seconds=randrange(10)
    print("sleeping for {0} seconds".format(seconds))
    time.sleep(seconds)
    checkInStock()

def checkInStock():
    
    options = Options()
    options.headless = True
    driver=webdriver.Firefox(options=options, executable_path="geckodriver.exe")
    driver.get(url)
    cart_button = driver.find_element_by_class_name("fulfillment-add-to-cart-button")
    item_name = driver.find_element_by_class_name("sku-title")
    status = cart_button.text
    name = item_name.text

    if status=="Sold Out":
        currTime = datetime.datetime.now()
        print("[{0}] Not in stock - {1}".format(currTime, name))
        driver.quit()
        callInStock()
    else:
        print("In stock!")
        command = "start firefox -new-window {0}".format(url)
        os.system(command)
        driver.quit()

checkInStock()