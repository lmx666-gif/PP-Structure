from imutils.perspective import four_point_transform
import imutils
import cv2
import numpy as np


def Get_Outline(input_dir):
    image = cv2.imread(input_dir)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 75, 200)
    return image, gray, edged


def Get_cnt(edged):  # 轮廓检测 获取四角点
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    docCnt = None

    if len(cnts) > 0:
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            peri = cv2.arcLength(c, True)  # 轮廓按大小降序排序
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)  # 获取近似的轮廓
            if len(approx) == 4:  # 近似轮廓有四个顶点
                docCnt = approx
                break
    return docCnt

def start(imagePath):
    img = cv2.imread(imagePath)
    cv2.imshow("src", img)
    grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imageHeight, imageWidth = grayImage.shape[0:2]
    print(imageWidth,", ", imageHeight)
    # 进行一次自适应阈值提升边界识别度，参数可根据不同图片适当调整，特别是左后一个参数
    binaryImage = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 35, 10)
    cv2.imshow("binaryImage", ~binaryImage)
    binaryImage = ~binaryImage
    # 这里我本来准备进行形态学操作的，可根据图片质量来取舍是否需要进行该操作，有些图片操作会好点
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    # binaryImage = cv2.erode(binaryImage, kernel, iterations=1)
    # binaryImage = cv2.dilate(binaryImage, kernel, iterations=1)
    cv2.imshow("binaryImage", binaryImage)
    # 查找轮廓
    contours, hierarchy = cv2.findContours(~binaryImage, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # 画轮廓
    cv2.drawContours(img, contours, 0, (0, 0, 255), 1)
    cv2.imshow("imgray", img)
    cnt = 0
    for i in range(len(contours)):
        arclen = cv2.arcLength(contours[i], True)
        epsilon = max(3, int(arclen * 0.02))
        # 每个轮廓进行多边形拟合，计算其面积，变数，周长等信息
        approx = cv2.approxPolyDP(contours[i], epsilon, True)
        # 计算面积
        area = cv2.contourArea(contours[i])
        print("area = ", area)
        # 计算最小包围矩阵，这里没太多印象，要不要无所谓
        rect = cv2.minAreaRect(contours[i])
        print("rect = ", rect)
        # 获取最小包围矩阵的四个点
        box = np.int0(cv2.boxPoints(rect))
        print("box = ", box)
        h = int(rect[1][0])
        w = int(rect[1][1])
        if min(h, w) == 0:
            rotion = 0
        else:
            rotion = max(h, w) / min((h, w))
        imageArea = imageWidth * imageHeight
        # 这里是删选轮廓的判断，长款比太大的不要，面积太小的不要，太大的也不要，如果是想得到四边形，那么后面的shap[0]就是去这个轮廓的边数，我这里取四边形，满足条件的轮廓画出来
        if rotion < 10 and area > imageArea * 0.2 and area < imageWidth * imageHeight *0.99 and approx.shape[0] == 4:
                # 对满足条件的轮廓画出轮廓的拟合多边形
            print("满足")
            cv2.polylines(img, [approx], True, (0, 255, 0), 1)
            cv2.circle(img, (approx[0][0][0], approx[0][0][1]), 3, (0, 0, 255), 2)
            cv2.putText(img, str(1), (approx[0][0][0], approx[0][0][1]), cv2.FONT_HERSHEY_PLAIN,
                1.0, (0, 0, 0), thickness=1)
            cv2.circle(img, (approx[1][0][0], approx[1][0][1]), 3, (0, 0, 255), 2)
            cv2.putText(img, str(2), (approx[1][0][0], approx[1][0][1]), cv2.FONT_HERSHEY_PLAIN,
                1.0, (0, 0, 0), thickness=1)
            cv2.circle(img, (approx[2][0][0], approx[2][0][1]), 3, (0, 0, 255), 2)
            cv2.putText(img, str(3), (approx[2][0][0], approx[2][0][1]), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0, 0, 0), thickness=1)
            cv2.circle(img, (approx[3][0][0], approx[3][0][1]), 3, (0, 0, 255), 2)
            cv2.putText(img, str(4), (approx[3][0][0], approx[3][0][1]), cv2.FONT_HERSHEY_PLAIN,
                            1.0, (0, 0, 0), thickness=1)
            cv2.imshow("polylines", img)

if __name__ == "__main__":
    input_dir = "..\\Data\\exp_pic\\0\\_img1.png"
    start(input_dir)
    cv2.waitKey(0)
    cv2.destroyAllWindows()