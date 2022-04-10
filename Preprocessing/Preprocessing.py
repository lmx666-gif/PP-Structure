import cv2
from matplotlib import pyplot as plt
import os

path_all_jpg = '..\\Data\\exp_pic'  # 存放文件目录
jpg_folder_all = os.listdir(path_all_jpg)  # 所有的文件列表
#print(jpg_folder_all)
ind =0
i=0
for file_name in jpg_folder_all:
    file=os.path.join(path_all_jpg,file_name)
    pic_file=os.listdir(file)
    for pic_name in pic_file:
        #print(pic_name)
        img_path = os.path.join(path_all_jpg, file_name)
        img_path = os.path.join(img_path,pic_name)
        #print(img_path)
        #print(pic_name)
        image = cv2.imread(img_path)
        # 将输入图像转为灰度图
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # 对灰度图使用ostu算法
        ret1, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        # 双边滤波
        img_bilater = cv2.bilateralFilter(th1, 9, 75, 75)
        if not os.path.exists('..\\Data\\exp_bilater\\' + str(ind)):
            os.makedirs('..\\Data\\exp_bilater\\' + str(ind))
        pic_path='..\\Data\\exp_bilater\\' + str(ind)
        print(pic_path)
        output_path=os.path.join(pic_path,str(i))
        output_path=output_path+'.png'
        cv2.imwrite(output_path, img_bilater)

        print("结束检测", i, "个文件!", "=========", img_path)
        i=i+1
    ind = ind + 1


