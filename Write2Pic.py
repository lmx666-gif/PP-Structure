from PIL import Image, ImageDraw, ImageFont
import cv2
from paddleocr import PaddleOCR,draw_ocr
#图片路径
img_path='Data/exp_pic/0/_img1.png'
ocr =PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=False,
               rec_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/rec/ch/ch_ppocr_server_v2.0_rec_infer',
               cls_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/cls/ch_ppocr_mobile_v2.0_cls_infer',
               det_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/det/ch/ch_ppocr_server_v2.0_det_infer/')
result=ocr.ocr(img_path,cls=True)
for line in result:
    print(line)
#内容都在line里，boxes里面存放了文本四个角的坐标，我们可以通过左上角坐标来定位文本开始写的位置
#boxes[i][0][0]和boxes[i][0][1]表示左上角点
#txts[i]表示对应的文本内容
image = Image.open(img_path).convert('RGB')
boxes=[line[0] for line in result]
txts=[line[1][0] for line in result]
scores=[line[1][1] for line in result]
#打开一张图片
img=cv2.imread(img_path)
h,w,c=img.shape
# 新建一张宽高都为200，底色为白色的图片
image = Image.new('RGB', (w, h),"White")
# 引入PIL库中的模块
draw = ImageDraw.Draw(image)
# 引入字体样式(第一个参数为字体样式，具体的可以在自己电脑中C:\Windows\Fonts下找；第二个参数为字体的大小)
font = ImageFont.truetype(r'C:\Windows\Fonts\simhei.ttf',24)
# 放置到指定位置(第一个100，代表距离图片左边距；第二个100代表距离图片顶部距离；text是定义的文字；fill设置字体颜色值;font是字体引入和大小的变量名称)
i=0
for txt in txts:
    if((boxes[i][1][0]-boxes[i][0][0])>(boxes[i][3][1]-boxes[i][0][1])):
        draw.text((boxes[i][0][0],boxes[i][0][1]),txt,fill='#666',font=font)
    elif((boxes[i][1][0]-boxes[i][0][0])<(boxes[i][3][1]-boxes[i][0][1])):
        j=0
        for str in txt:
            draw.text((boxes[i][0][0],boxes[i][0][1]+25*j),str,fill='#666',font=font)
            j=j+1
    i=i+1
image.show()
