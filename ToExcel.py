from paddleocr import PPStructure,draw_structure_result,save_structure_res
import cv2

img_path = "Data/exp_pic/0/_img1.png"
table_engine= PPStructure(show_log=True,use_gpu=False)

img=cv2.imread(img_path)
result=table_engine(img)
print(result)
save_structure_res(result,"aa","a")