from selenium import webdriver
import time

browser = webdriver.Chrome(executable_path="./chromedriver")

try:
    browser.get('https://shimo.im/')
    time.sleep(1)
    btm1 = browser.find_element_by_xpath('//*[@id="homepage-header"]/nav/div[3]/a[2]/button')
    btm1.click()
    time.sleep(3)

    print("login page start")
    browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('15727667323')
    browser.find_element_by_xpath('//input[@name="password"]').send_keys('re1234')
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="root"]/div/div[2]/div/div/div/div[2]/div/div/div[1]/button').click()
    time.sleep(10)
    # TODO: 图像识别图片中的汉字，并按照给定循序依次点击，最后点击确认按钮

except Exception as e:
    print(e)
finally:
    browser.close()

