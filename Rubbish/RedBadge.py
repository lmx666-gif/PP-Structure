#去除印章
import cv2
import numpy as np
import matplotlib.pyplot as plt

#读入图像,三通道
image=cv2.imread("../Preprocessing/stamp.png", cv2.IMREAD_COLOR) #timg.jpeg

#读入图像尺寸
cols,rows,_=image.shape
#缩放比例
ratio=0.3

#缩放后的尺寸
cols=int(ratio*cols)
rows=int(ratio*rows)

#缩放图片
image = cv2.resize(image,(rows,cols)  )

#获得三个通道
Bch,Gch,Rch=cv2.split(image)

#cv2.imshow('Blue channel',cv2.merge([Bch,0*Gch,0*Rch]))
#cv2.imshow('Green channel',cv2.merge([0*Bch,Gch,0*Rch]))
#cv2.imshow('Red channel',cv2.merge([0*Bch,0*Gch,Rch]))


#cv2.imshow('Blue channel',Bch)
#cv2.imshow('Green channel',Gch)
#cv2.imshow('Red channel',Rch)

#cv2.imwrite('Blue channel.jpg',Bch)
#cv2.imwrite('Green channel.jpg',Gch)
#cv2.imwrite('Red channel.jpg',Rch)


#红色通道的histgram
#变换程一维向量
pixelSequence=Rch.reshape([rows*cols,])

#统计直方图的组数
numberBins=256

#计算直方图
plt.figure()
manager = plt.get_current_fig_manager()
#manager.window.showMaximized()
manager.resize(*manager.window.maxsize())
histogram,bins,patch=plt.hist(pixelSequence,numberBins,facecolor='black',histtype='bar') #facecolor设置为黑色

#设置坐标范围
#y_maxValue=np.max(histogram)
#plt.axis([0,255,0,y_maxValue])
#设置坐标轴
#plt.xlabel("gray Level",fontsize=20)
#plt.ylabel('number of pixels',fontsize=20)
#plt.title("Histgram of red channel", fontsize=25)
#plt.xticks(range(0,255,10))
#显示直方图
#plt.pause(0.05)
#plt.savefig("histgram.png",dpi=260,bbox_inches="tight")
#plt.show()


#红色通道阈值
_,RedThresh = cv2.threshold(Rch,160,255,cv2.THRESH_BINARY)

#膨胀操作
element = cv2.getStructuringElement(cv2.MORPH_RECT,(1,1))
erode = cv2.erode(RedThresh, element)

#显示效果
#cv2.imshow('original color image',image)
#cv2.imwrite('scaleimage.jpg',image)

#cv2.imshow("RedThresh",RedThresh)
#cv2.imwrite('RedThresh.jpg',RedThresh)

#cv2.imshow("erode",erode)
cv2.imwrite("erode.jpg", erode)