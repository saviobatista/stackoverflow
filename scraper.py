import logging
import os
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from requests import get
from datetime import datetime

if __name__ == '__main__':
    try:
        load_dotenv()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # options.add_experimental_option("detach", True)
        driver = webdriver.Chrome(options=options,service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM,log_level=logging.ERROR).install()))
        driver.get('https://stackoverflow.com/users/login?ssrc=head&returnurl=https%3a%2f%2fstackoverflow.com%2f')
        assert 'Log In - Stack Overflow' in driver.title
        # sleep(1)
        driver.find_element(by=By.ID, value='email').send_keys(os.environ.get('EMAIL'))
        driver.find_element(by=By.ID, value='password').send_keys(os.environ.get('PASSWORD'))
        # click() doesn't work on Mac, but would works for Linux and Windows
        # driver.find_element(by=By.ID, value='submit-button').click()
        driver.execute_script('return document.getElementById("submit-button").click()')
        sleep(1)
        assert 'Stack Overflow - Where Developers Learn, Share, & Build Careers' in driver.title
        # driver.find_element(by=By.XPATH, value='/html/body/header/div/ol[2]/li[2]/a').click()
        driver.execute_script('return document.evaluate(\'/html/body/header/div/ol[2]/li[2]/a\',document,null,XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()')
        sleep(2)
        reputacao = driver.find_element(by=By.XPATH, value='/html/body/header/div/ol[2]/li[2]/a/div[2]/ul/li[1]/span').text
        medals = driver.find_element(by=By.XPATH, value='/html/body/header/div/ol[2]/li[2]/a/div[2]/ul/li[2]/span[2]').text
        driver.close()
        url = 'https://api.callmebot.com/whatsapp.php'
        param = {
            'phone':os.environ.get('PHONE'),
            'text':'Robo stackoverflow em ' + datetime.today().strftime ('%d/%m/%Y') + '\nMedalhas: ' + medals + reputacao,
            'apikey':os.environ.get('APIKEY')
        }
        r = get(url = url, params = param)
    except WebDriverException as e:
        url = 'https://api.callmebot.com/whatsapp.php'
        param = {
            'phone':os.environ.get('PHONE'),
            'text':'Robo stackoverflow em ' + datetime.today().strftime ('%d/%m/%Y') + '\n\nHouve um erro no robo do stackoverflow: ' + str(e),
            'apikey':os.environ.get('APIKEY')
        }
        r = get(url = url, params = param)
