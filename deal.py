from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException
import os
from random import randrange
import time
import datetime
import sys

userInput = True
urls = []
global attempts
attempts = 1
mode = sys.argv[1]
global timeoutAttempts
timeoutAttempts = 0

if mode == "1":
    argList = sys.argv[2:]
    for url in argList:
        urls.append(url)
elif mode == "2":
    while userInput:
        url = input("Enter Bestbuy URL (press enter when done): ")
        if url == "":
            userInput = False
        else: 
            urls.append(url)
else:
    print("Enter a valid mode arg. Exiting....")
    sys.exit()

# Program that allows for wait
def callInStock():
    global timeoutAttempts
    timeoutAttempts = 0
    global attempts 
    attempts += 1
    seconds=randrange(10)
    print("sleeping for {0} seconds".format(seconds))
    time.sleep(seconds)
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
    driver.set_page_load_timeout(5)
    try:
        #loops through urls
        for url in urls:
            #makes request to page
            driver.get(url)
            cart_button = driver.find_element_by_class_name("fulfillment-add-to-cart-button") 
            item_name = driver.find_element_by_class_name("sku-title") 
            status = cart_button.text #Gets the text of the cart button
            name = item_name.text #Gets item name

            #Checks if item is sold out
            if status=="Sold Out":
                currTime = datetime.datetime.now()
                print("[{0}] Not in stock - {1}".format(currTime, name))
                seconds = randrange(5)
                time.sleep(seconds)
            else:
                currTime = datetime.datetime.now()
                print("[{1}] In stock! - {0}".format(name, currTime))
                command = "start firefox -new-window {0}".format(url)
                os.system(command)
                urls.remove(url)
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