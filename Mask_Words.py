import matplotlib.pyplot as plt
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2
from paddleocr import PaddleOCR,draw_ocr

#找中点
def midpoint(x1, y1, x2, y2):
    x_mid = int((x1 + x2) / 2)
    y_mid = int((y1 + y2) / 2)
    return (x_mid, y_mid)

#获取涂抹后的底层图片
def inpaint_text(img,boxes):
    mask = np.zeros(img.shape[:2], dtype="uint8")
    for box in boxes:
        x0, y0 = box[0][0],box[0][1]
        x1, y1 = box[1][0],box[1][1]
        x2, y2 = box[2][0],box[2][1]
        x3, y3 = box[3][0],box[3][1]
        x_mid0, y_mid0 = midpoint(x0, y0, x3, y3)
        x_mid1, y_mi1 = midpoint(x1, y1, x2, y2)
        thickness = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
        cv2.line(mask, (x_mid0, y_mid0), (x_mid1, y_mi1), 255, thickness)
        img = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    return img

#ocr识别
def OCR(img_path):
    ocr = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=False,
                    rec_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/rec/ch/ch_ppocr_server_v2.0_rec_infer',
                    cls_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/cls/ch_ppocr_mobile_v2.0_cls_infer',
                    det_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/det/ch/ch_ppocr_server_v2.0_det_infer/')
    result = ocr.ocr(img_path, cls=True)
    return result

def main():
    img_path='Data/exp_pic/0/_img1.png'
    result=OCR(img_path)
    #for line in result:
    #    print(line)
    image = Image.open(img_path).convert('RGB')
    boxes = [line[0] for line in result]
    txts = [line[1][0] for line in result]
    scores = [line[1][1] for line in result]
    #我现在应该获取没有文字的图片了,没有文字的图片哈
    img=cv2.imread(img_path)
    mask=inpaint_text(img, boxes)
    img_rgb = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB)
    cv2.imwrite('mask.jpg',mask)
if __name__ == '__main__':
    main()
