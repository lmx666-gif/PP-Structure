from paddleocr import PaddleOCR,draw_ocr
#img_path='Data/exp_pic/0/_img1.png'
img_path='Data/exp_bilater/0/0.png'
#img_path='img_bilater.jpg'
ocr =PaddleOCR(use_angle_cls=True, lang="ch",use_gpu=False,
               rec_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/rec/ch/ch_ppocr_server_v2.0_rec_infer',
               cls_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/cls/ch_ppocr_mobile_v2.0_cls_infer',
               det_model_dir='C:/Users/limuo/.paddleocr/2.4/ocr/det/ch/ch_ppocr_server_v2.0_det_infer/')
result=ocr.ocr(img_path,cls=True)
#for line in result:
#    print(line)

from PIL import Image

image = Image.open(img_path).convert('RGB')
boxes=[line[0] for line in result]
txts=[line[1][0] for line in result]
scores=[line[1][1] for line in result]
print(boxes)

im_show =draw_ocr(image,boxes,txts,scores)
im_show=Image.fromarray(im_show)
im_show.save('result.jpg')