import numpy as np
import cv2
import base64


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
