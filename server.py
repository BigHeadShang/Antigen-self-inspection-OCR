import paddlehub as hub
# ocr = hub.Module(name="chinese_ocr_db_crnn_mobile")  # 加载移动端的模型，比较轻量
ocr = hub.Module(name="chinese_ocr_db_crnn_server")  # 加载服务端大模型，效果更好
import cv2
import csv
import os
import re
from PIL import Image
# 修改官方读取图片方法，直接对文件夹下图片进行读取识别
# np_images =[cv2.imread(image_path) for image_path in test_img_path]
img_path = './temp/'
imagelist = os.listdir(img_path)
print(len(imagelist))
# np_images =[cv2.imread(os.path.join('./temp/',image_path)) for image_path in imagelist]
np_images = [Image.open(os.path.join('./temp/',image_path)).convert('BGR') for image_path in imagelist if image_path.split('.') != 'DS_Store']
print(np_images[0])
results = ocr.recognize_text(
                    images=np_images,         # 图片数据，ndarray.shape 为 [H, W, C]，BGR格式；
                    use_gpu=False,            # 是否使用 GPU；若使用GPU，请先设置CUDA_VISIBLE_DEVICES环境变量
                    output_dir='./test/',  # 图片的保存路径，默认设为 ocr_result；
                    visualization=True,       # 是否将识别结果保存为图片文件；
                    box_thresh=0.5,           # 检测文本框置信度的阈值；
                    text_thresh=0.5)          # 识别中文文本置信度的阈值；

r='[’!"#$%&\'()*+,-./:：;<=>?@[\\]^_`{|}~\n。！，]+' # 去除英文符号
# line=re.sub(r,'',text)
punctuation = """！？｡＂＃＄％＆＇（）＊＋－／：；＜＝＞＠［＼］＾＿｀｛｜｝～｟｠｢｣､、〃》「」『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘'‛“”„‟…‧﹏"""  # 去除中文符号
re_punctuation = "[{}]+".format(punctuation)

for result in results:
    data = result['data']
    save_path = result['save_path']
    for infomation in data:
        print('text: ', re.sub(re_punctuation,"",infomation['text']), '\nconfidence: ', infomation['confidence'], '\ntext_box_position: ', infomation['text_box_position'])