from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
from random import randrange
import os
import time
import datetime
import sys
import re
import json

userInput = True
urls = {
    "bestbuy": [],
    "newegg": []
}
global attempts
attempts = 1
mode = input("Select 1 for args, 2 for manual input (1 default): ")
global timeoutAttempts
timeoutAttempts = 0

def getWebsite(url):
    if re.search("bestbuy", url):
        return "bestbuy"
    elif re.search("newegg", url):
        return "newegg"
    else:
        return False

if mode == "2":
    while userInput:
        url = input("Enter Bestbuy or Newegg URL (press enter when done): ")
        if url == "":
            userInput = False
        else: 
            site = getWebsite(url)
            if site != False:
                urls[site].append(url)
            else:
                print("{0} is not a bestbuy or newegg url. Please enter valid url".format(url))
else:
    argList = sys.argv[2:]
    for url in argList:
        site = getWebsite(url)
        if site != False:
            urls[site].append(url)
        else:
            print("{0} is not a bestbuy or newegg url.".format(url))
# Program that allows for wait
def callInStock():
    global timeoutAttempts
    timeoutAttempts = 0
    global attempts 
    attempts += 1
    checkInStock()

#Checks each url to see if item is in stock
def checkInStock():
    currTime = datetime.datetime.now()
    print("[{0}] Attempt {1}, checking...".format(currTime, attempts))
    # Checks length of urls array
    length = len(urls)
    if length<=0:
        print("No URLS")
        return
    
    #initializes 
    options = Options()
    options.headless = True
    driver=webdriver.Firefox(options=options, executable_path="geckodriver.exe")
    driver.set_page_load_timeout(15)
    try:
        #loops through urls
        for site in urls:
            for url in urls[site]:
                #makes request to page
                driver.get(url)
                if site == "bestbuy":
                    cart_button = driver.find_element_by_class_name("fulfillment-add-to-cart-button") 
                    item_name = driver.find_element_by_class_name("sku-title") 
                    status = cart_button.text #Gets the text of the cart button
                    name = item_name.text #Gets item name

                    #Checks if item is sold out
                    if status=="Coming Soon" or status=="Sold Out":
                        currTime = datetime.datetime.now()
                        print("[{0} ({3})] {2} - {1}".format(currTime, name, status, site))
                    else:
                        currTime = datetime.datetime.now()
                        print("[{1}] Needs Checking! - {0}".format(name, currTime))
                        command = "start firefox -new-window {0}".format(url)
                        os.system(command)
                        driver.close()
                        driver.quit()
                        sys.exit()
                elif site == "newegg":
                    cart_button = driver.find_element_by_id("ProductBuy") 
                    item_name = driver.find_element_by_class_name("product-title") 
                    status = cart_button.text #Gets the text of the cart button
                    name = item_name.text #Gets item name
                    #Checks if item is sold out
                    if status=="SOLD OUT":
                        currTime = datetime.datetime.now()
                        print("[{0} ({3})] {2} - {1}".format(currTime, name, status, site))
                    else:
                        currTime = datetime.datetime.now()
                        print("[{1}] Needs Checking! - {0}".format(name, currTime))
                        command = "start firefox -new-window {0}".format(url)
                        os.system(command)
                        driver.close()
                        driver.quit()
                        sys.exit()
        #Closes the headless windows
        driver.close()
        driver.quit()
        #Calls wait function.
        callInStock()
    except TimeoutException as e:
        global timeoutAttempts
        timeoutAttempts+=1
        if timeoutAttempts == 3:
            print("Timeout limit exceeded, ending program.")
            sys.exit()
        else:
            currTime = datetime.datetime.now()
            print("[{0}] Page Timed Out. Trying Again...".format(currTime))
            driver.quit()
            checkInStock()
    except:
        print("Exiting Program... (Either something went wrong or you ctrl+c)")
        sys.exit()

checkInStock()

