import os
from time import sleep
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

if __name__ == '__main__':
    try:
        load_dotenv()
        driver = webdriver.Chrome()
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
        driver.close()
        print('Feito.')
    except WebDriverException as e:
        print('ERRO FATAL!')
        print(e.args)
        print(e.msg)
        print(e.stacktrace)
        print(e.screen)
        print('-')
