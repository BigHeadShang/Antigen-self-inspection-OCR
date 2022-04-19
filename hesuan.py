import os
import cv2 as cv
import xlrd as xlrd
from PIL import Image
from paddleocr import PaddleOCR,draw_ocr
import xlwt
ocr = PaddleOCR(lang = 'ch')
img_path = './4.11/'
total = xlwt.Workbook(encoding='utf-8')
sheet1 = total.add_sheet("4月11日")
sheet1.write(0, 0, "班级")
sheet1.write(0, 1, "时间")
sheet1.write(0, 2, "学号")
sheet1.write(0, 3, "姓名")
sheet1.write(0, 4, "检测结果")

# rbook = xlrd.open_workbook(r'/Users/shangzhanhao/Desktop/ocr/test.xlsx')
# sheet = rbook.sheet_by_name("4月9日")

i = 1
for filename in os.listdir(img_path):
    print("总量为：",len(os.listdir(img_path)),"当前为：",os.listdir(img_path).index(filename))
    if filename.split('.')[1] == 'jpg' or filename.split('.')[1] == 'jpeg':
        result = ocr.ocr(img_path + filename)
        for line in result:
            print(line)
        img = Image.open(img_path + filename).convert('RGB')
        boxes = [line[0] for line in result]
        txt = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        img = draw_ocr(img,boxes,txt,scores)
        img = Image.fromarray(img)
        for t1 in txt:
            if '2022' in t1:
                sheet1.write(i, 1, t1)
                break
                # else:
                #     sheet1.write(i, 0, str('notime'))
        for t2 in txt:
            if '阴' in t2 or '性' in t2:
                sheet1.write(i, 4, t2)
                break
            # else:
            #     sheet1.write(i, 3, str('未识别'))
            # total.save(r'/Users/shangzhanhao/Desktop/ocr/test.xlsx')
        for t3 in txt:
            if 'M4' in t3:
                if len(t3) == 10:
                    print(t3[:8])
                    sheet1.write(i, 0, str(t3[:8]))
                    sheet1.write(i, 2, t3)
                    temp = txt.index(t3)
                    sheet1.write(i, 3, txt[temp-1])
                    img.save('./test/' + txt[temp-1] + '.jpg')
                    break
            # else:
            #     sheet1.write(i, 1, str('未识别'))
            # total.save(r'/Users/shangzhanhao/Desktop/ocr/test.xlsx')
        # if len(txt) > 2:
        #     sheet1.write(i, 3, str(txt[1]))
        #     if len(txt) > 2:
        #         sheet1.write(i, 2, str(txt[2]))
        #         if len(txt) > 3:
        #             sheet1.write(i, 1, str(txt[3]))
    i += 1

total.save(r'/Users/shangzhanhao/Desktop/ocr/4月11日.xlsx')

