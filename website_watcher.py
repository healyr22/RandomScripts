import datetime
import requests
import time
from bs4 import BeautifulSoup
import slack_sdk
from slack_sdk.errors import SlackApiError
from selenium import webdriver
import os
from urllib.request import Request, urlopen
import urllib.request

url = "https://www.bestbuy.ca/en-ca/product/nvidia-geforce-rtx-4070-12gb-gddr6x-video-card/17034430" # Replace with the URL you want to monitor

SLACK_BOT_TOKEN = "" # Replace with your bot token
SLACK_CHANNEL_ID = "C0530BE8LGJ" # Replace with your channel ID

driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
driver.get(url)
old_content = driver.page_source
driver.close()

client = slack_sdk.WebClient(token=SLACK_BOT_TOKEN)

while True:
    driver = webdriver.Chrome(executable_path = 'chromedriver.exe')
    driver.get(url)
    new_content = driver.page_source
    driver.close()
    
    soup_old = BeautifulSoup(old_content, 'html.parser')
    span_old = soup_old.find('div', id='delivery')
    
    soup_new = BeautifulSoup(new_content, 'html.parser')
    span_new = soup_new.find('div', id='delivery')
    
    if span_old != span_new:
        print("Website content has changed!")
        message = "Website content has changed! Was {} ....... but now is {}".format(old_content, new_content)
        try:
            response = client.chat_postMessage(
                channel=SLACK_CHANNEL_ID,
                text=message
            )
            print("Slack notification sent")
        except SlackApiError as e:
            print("Error sending Slack notification: {}".format(e))
        
        old_content = new_content
    else:
        print("Found no difference at " + str(datetime.datetime.now()))
    
    time.sleep(60) # Wait for N minutes before checking again
