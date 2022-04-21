from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
import base64
import cv2
import numpy as np


# 获取透明背景图片的最小外接矩型坐标
def get_png_edge(img):
    rr = np.where(img[:, :] != 0)
    x_min = min(rr[1])
    y_min = min(rr[0])
    x_max = max(rr[1])
    y_max = max(rr[0])

    return {
        'x': [x_min, x_max],
        'y': [y_min, y_max]
    }


# 将base64转为opencv图片
def base64_to_img(uri):
    encoded_data = uri.split(',')[1]
    nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img


# 匹配图片相似，返回x坐标
def template_match(image_bg, image_fg):
    res = cv2.matchTemplate(image_bg, image_fg, cv2.TM_SQDIFF)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return min_loc[0]


# 边缘检测
def sobel_edge(image):
    image_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    abs_x = cv2.convertScaleAbs(image_x)
    image_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    abs_y = cv2.convertScaleAbs(image_y)
    dst = cv2.addWeighted(abs_x, 0.5, abs_y, 0.5, 0)
    return np.asarray(dst, dtype=np.uint8)


# 读取图片并完成高斯滤波和边缘检测
def read(image):
    image = cv2.GaussianBlur(image, (1, 1), 0)
    return sobel_edge(image)


def login(username, password, url):
    print('----------------')
    print('准备开始自动登录')
    option = webdriver.FirefoxOptions()
    option.binary_location = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'
    service = Service()
    print('正在打开浏览器')
    driver = webdriver.Firefox(service=service, options=option)

    print('正在进入网页')
    WAIT = WebDriverWait(driver, 10)
    driver.get(url)

    print('正在获取账号密码输入框')
    username_input = WAIT.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#username'))
    )
    password_input = WAIT.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '#password'))
    )
    print('正在输入账号密码')
    username_input.send_keys(username)
    password_input.send_keys(password)

    login_btn_l = WAIT.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.auth_login_btn'))
    )
    print('点击登录')
    login_btn_l.click()

    print('等待显示验证拼图')
    block = WAIT.until(
        ec.presence_of_element_located((By.CSS_SELECTOR, '.block'))
    )

    print('获取验证拼图图片')
    js_get_block = f'''return document.getElementsByClassName("block")[0].toDataURL("image/png")'''
    base64str_block = driver.execute_script(js_get_block)
    js_get_back = f'''return document.querySelector("#captcha > canvas:nth-child(1)").toDataURL("image/png")'''
    base64str_back = driver.execute_script(js_get_back)

    # 将base64转为img
    bg_img = base64_to_img(base64str_back)
    fg_img = base64_to_img(base64str_block)
    # 对图片进行高斯滤波与边缘检测
    bg = read(bg_img)
    fg = read(fg_img)
    # 得到滑块的边缘
    edge = get_png_edge(fg)
    # 将两图片分别裁切为x轴方向不变，y轴为滑块高度
    fg_image = fg[edge['y'][0]:edge['y'][1], edge['x'][0]:edge['x'][1]]
    bg_image = bg[edge['y'][0]:edge['y'][1], :]
    # 匹配得到滑块最左边坐标
    left = template_match(bg_image, fg_image)
    print('取得拼图最左端x坐标：' + str(left))

    print('正在获取滑块元素')
    slider = WAIT.until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, '.slider'))
    )
    print('正在准备滑动操作')
    actions = ActionChains(driver)
    actions.drag_and_drop_by_offset(slider, left, 0).perform()
    print('滑动完成，自动登录结束')
    print('----------------')
