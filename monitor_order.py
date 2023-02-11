#!/usr/bin python3
# -*- coding: utf-8 -*-
"""
@author: Bill
Command:
    python monitor_order.py
"""

from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys

options = Options()
options.add_argument("--disable-notifications")  
options.add_argument("--headless") 
s=Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, options=options)
browser.set_page_load_timeout(120)

wrong_domain=[]


def login(domain,right_code,browser):
    browser.get(f"https://{domain}/")
    time.sleep(1)
    try:temp=browser.find_element(By.XPATH,'//div[@class="close-button"][1]')
    except NoSuchElementException:
        wrong_domain.append(domain)
        return f"{domain} can't access."
    except : 
        wrong_domain.append(domain)
        return f"{domain}, something wrong."
    temp.click()
    time.sleep(1)
    banner=browser.find_elements(By.XPATH,'//div[@class="class-block-selector"]/div')
    compare_result=compare_banner(banner)
    if compare_result != "Success" : 
        wrong_domain.append(domain)
        return f"{domain},{compare_result}"

    temp=browser.find_element(By.XPATH,'//div[@class="login-wrapper"]/img[2]')
    temp.click()
    time.sleep(1)
    temp=browser.find_element(By.XPATH,'//div[@class="swiper-slide swiper-slide-active"]//form/div[4]//input')
    code=temp.get_attribute('value')
    if code != right_code:
        wrong_domain.append(domain)
        return f"{domain},The code is wrong."
    
    return f"{domain},Completed"


def compare_banner(banner):

    banner_list=list(enumerate(["active electronic","live","qpgame","cpgame","hunter","sports","esports"]))
    
    for index,value in banner_list:
        
        # print("item "+value)
        # print(banner[index].get_attribute('class'))        
        if banner[index].get_attribute('class') != "item "+value : 
            return "The order of the buttons is wrong."

    else : return "Success"

if __name__ == "__main__":

    with open("domain.txt") as f : 
        dlist=[tuple(x.strip().split(' ')) for x in f.readlines()]

    for dm,right_code in dlist:
        try : 
            print(login(dm,right_code,browser))
        except TimeoutException : 
            print(f"{dm} check timeout.")
            wrong_domain.append(dm)
            continue
    print("========================================")
    print(f"Wrong domain : {len(wrong_domain)}")
    print(wrong_domain)
    print("\n")
        



