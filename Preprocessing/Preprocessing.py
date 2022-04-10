import cv2
from matplotlib import pyplot as plt

image = cv2.imread('stamp.png')


# 将输入图像转为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 绘制灰度图
plt.imshow(gray,"gray")
plt.title("input image")
plt.xticks()
plt.show()
