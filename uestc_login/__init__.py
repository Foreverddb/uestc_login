from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from uestc_login.img_process import base64_to_img, get_png_edge, template_match, sobel_edge, read


def login(username, password, url='https://idas.uestc.edu.cn/authserver/login'):
    """通过学号和密码进行自动模拟登录，返回登录成功后的 webdriver"""
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
    return driver
