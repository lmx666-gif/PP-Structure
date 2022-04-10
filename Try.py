import cv2
import layoutparser as lp
image = cv2.imread("C:/Users/limuo/Desktop/Documentary/OCR/img_bilater.jpg")
image = image[..., ::-1]

# 加载模型
model = lp.PaddleDetectionLayoutModel(model_path="D://ToeflSoft/ppyolov2_r50vd_dcn_365e_publaynet",
                                threshold=0.5,
                                label_map={0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"},
                                enforce_cpu=True,
                                enable_mkldnn=True)
# 检测
layout = model.detect(image)

# 显示结果
show_img = lp.draw_box(image, layout, box_width=3, show_element_type=True)
show_img.show()

# 接上面代码
# 首先过滤特定文本类型的区域
#text_blocks = lp.Layout([b for b in layout if b.type=='Text'])
#figure_blocks = lp.Layout([b for b in layout if b.type=='Figure'])

# 因为在图像区域内可能检测到文本区域，所以只需要删除它们
#text_blocks = lp.Layout([b for b in text_blocks \
#                  if not any(b.is_in(b_fig) for b_fig in figure_blocks)])

# 对文本区域排序并分配id
#h, w = image.shape[:2]

#left_interval = lp.Interval(0, w/2*1.05, axis='x').put_on_canvas(image)

#left_blocks = text_blocks.filter_by(left_interval, center=True)
#left_blocks.sort(key = lambda b:b.coordinates[1])

#right_blocks = [b for b in text_blocks if b not in left_blocks]
#right_blocks.sort(key = lambda b:b.coordinates[1])

# 最终合并两个列表，并按顺序添加索引
#text_blocks = lp.Layout([b.set(id = idx) for idx, b in enumerate(left_blocks + right_blocks)])

# 显示结果
#show_img = lp.draw_box(image, text_blocks,
#            box_width=3,
#            show_element_id=True)
#show_img.show()