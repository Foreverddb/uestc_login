from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By

import uestc_login
from uestc_login import login


def main():
    # 打开浏览器
    option = webdriver.FirefoxOptions()
    option.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    option.headless = True
    service = Service()
    print('正在打开浏览器')
    driver = webdriver.Firefox(service=service, options=option)
    # 打开网上服务大厅
    print('正在进入网页')
    WAIT = WebDriverWait(driver, 10)
    driver.get('https://eportal.uestc.edu.cn/')

    # 进入统一身份认证界面并返回界面url
    print('正在进入认证界面')
    login_btn = WAIT.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.amp-no-login-zh'))
    )
    login_btn.click()
    print('获取统一身份认证界面网址并返回')
    verify_url = driver.current_url
    driver.close()
    return verify_url


if __name__ == '__main__':
    username = input('请输入您的学号：')
    password = input('请输入您的密码：')
    url = main()
    driver = login(username=username, password=password, url=url, browser=uestc_login.FIREFOX)
    # 示例：打印登陆后得到的cookies
    print(driver.get_cookies())
