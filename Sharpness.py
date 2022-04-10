import cv2
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from skimage.io import imshow, imread
from skimage.color import rgb2yuv, rgb2hsv, rgb2gray, yuv2rgb, hsv2rgb
from scipy.signal import convolve2d

def multi_convolver(image, kernel, iterations):
    for i in range(iterations):
        image = convolve2d(image, kernel, 'same', boundary = 'fill',
                           fillvalue = 0)
    return image

def convolver_rgb(image, kernel, iterations=1):
    img_yuv = rgb2yuv(image)
    img_yuv[:, :, 0] = multi_convolver(img_yuv[:, :, 0], kernel,
                                       iterations)
    final_image = yuv2rgb(img_yuv)

    fig, ax = plt.subplots(1, 2, figsize=(17, 10))

    ax[0].imshow(image)
    ax[0].set_title(f'Original', fontsize=20)

    ax[1].imshow(final_image);
    ax[1].set_title(f'YUV Adjusted, Iterations = {iterations}',
                    fontsize=20)

    [axi.set_axis_off() for axi in ax.ravel()]

    fig.tight_layout()

    return final_image


dog = imread('stamp.png')
plt.figure(num=None, figsize=(8, 6), dpi=80)
imshow(dog);


sharpen = np.array([[0, -1, 0],
                    [-1, 5, -1],
                    [0, -1, 0]])
final_image = convolver_rgb(dog, sharpen, iterations = 2)

cv.namedWindow('SHARPNESS')
cv.imshow('SHARPNESS',final_image)

cv.waitKey()
cv.destroyAllWindows()
cv2.imwrite("stamp_sharpess.png",final_image*255)