import fitz
import time
import numpy as np
import cv2 as cv
import re
import os
def pdf2pic(path, pic_path):
    '''
    # 从pdf中提取图片
    :param path: pdf的路径
    :param pic_path: 图片保存的路径
    :return:
    '''
    #t0 = time.clock()
    # 使用正则表达式来查找图片
    checkXO = r"/Type(?= */XObject)"
    checkIM = r"/Subtype(?= */Image)"
    # 打开pdf
    doc = fitz.open(path)
    # 图片计数
    imgcount = 0
    lenXREF = doc.xref_length()

    # 打印PDF的信息
    print("文件名:{}, 页数: {}, 对象: {}".format(path, len(doc), lenXREF - 1))
    # 遍历每一个对象
    for i in range(1, lenXREF):
        # 定义对象字符串
        text = doc.xref_object(i)
        isXObject = re.search(checkXO, text)
        # 使用正则表达式查看是否是图片
        isImage = re.search(checkIM, text)
        # 如果不是对象也不是图片，则continue
        if not isXObject or not isImage:
            continue
        imgcount += 1
        # 根据索引生成图像
        pix = fitz.Pixmap(doc, i)
        # 根据pdf的路径生成图片的名称
        new_name = "_img{}.png".format(imgcount)
        new_name = new_name.replace(':', '')
        # 如果pix.n<5,可以直接存为PNG
        if pix.n < 5:
            pix.save(os.path.join(pic_path, new_name))
        # 否则先转换CMYK
        else:
            pix0 = fitz.Pixmap(fitz.csRGB, pix)
            pix0.save(os.path.join(pic_path, new_name))
            pix0 = None
        # 释放资源
        pix = None
        #t1 = time.clock()
        #print("运行时间:{}s".format(t1 - t0))
        print("提取了{}张图片".format(imgcount))

if __name__ == '__main__':
    # pdf路径
    datadir="..\\Data\\exp"
    pdf_path=os.path.join(datadir)
    aba=os.listdir(pdf_path)
    ind=0
    for pdf in aba:
        # 创建保存图片的文件夹
        print(pdf)
        pdf_path=os.path.join(datadir)
        print(pdf_path)
        pdf_path=os.path.join(datadir,pdf)
        print(pdf_path)
        if not os.path.exists('..\\Data\\exp_pic\\' + str(ind)):
            os.makedirs('..\\Data\\exp_pic\\' + str(ind))
        pic_path='..\\Data\\exp_pic\\' + str(ind)
        print(pic_path)
        m = pdf2pic(pdf_path, pic_path)
        ind=ind+1