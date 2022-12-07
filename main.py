import argparse
import cv2
import pytesseract
import re
# 設定命令列參數讀取程式
parser = argparse.ArgumentParser()
parser.add_argument('input_video')
parser.add_argument('output_txt')
args = parser.parse_args()

# 使用 cv2 讀取影片並取得影片長度
video = cv2.VideoCapture(args.input_video)
length = int(video.get(cv2.CAP_PROP_FRAME_COUNT))


# 取得影片的每秒幀數
fps = video.get(cv2.CAP_PROP_FPS)


# 設定 pytesseract 的辨識語言為英文
#pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
config = ("-l eng --oem 3 --psm 12 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ")

# 建立一個空的暫存變數，用來記錄已經出現過的文字
text_set = set()
last_text=" "
text_count=0
# 設定輸出檔案
with open(args.output_txt, 'w') as f:
    # 從影片的第一幀開始讀取，每次讀取一幀影像
    for i in range(length):
        #print(i)
        success, image = video.read()
        # 如果讀取影像失敗則跳出迴圈
        if not success:
            break
        if i % 5 == 0 :
            # 裁切圖片
            x=int(0)
            y=int(0)
            w=int(640)
            h=int(360/2)
            image = image[y:y+h, x:x+w]
            # 二元化
            raw_image=image
            image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            ret,image = cv2.threshold(image,240,255,cv2.THRESH_BINARY_INV)
            kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 3))
            image = cv2.erode(image, kernel1)     # 先侵蝕，將白色小圓點移除
            #cv2.imshow('oxxostudio2', img)   # 侵蝕後的影像
            image = cv2.dilate(image, kernel2)    # 再膨脹，白色小點消失
            #cv2.imshow('oxxostudio3', img)   # 膨脹後的影像
            # 使用 pytesseract 辨識圖片中的文字
            text = pytesseract.image_to_string(image, config=config)
            re.match('[A-Z]+$', text.rstrip())
            if text != None and text != last_text :
            	last_text=text
            	text_count=0
            else :
                #last_text=" "
                text_count=text_count+1
            print('text_count:',text_count)
            if text_count >=5 :
            	print("===================")
            	text_set.add(text)
            	print(text_set)
            	 # 將出現時間轉換成秒數
            	time = i / fps
            	f.write('!{} @{}\n'.format(time, text))
            # 如果辨識出文字並且未出現過則將文字及其出現時間寫入檔案

            #if text and text not in text_set:
            if text != None :
                text_set.add(text)
                # 將出現時間轉換成秒數
                time = i / fps
                f.write('!{} @{}\n'.format(time, text))
            
                # 顯示圖片
                cv2.imshow('Video', image)
                cv2.imshow('rawVideo', raw_image)
                # 暫停一段時間，等待使用者按下任意鍵
                # 如果在暫停時間內按下 q 鍵則結束程式
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                test_set.clear()

# 關閉影片播放窗口
cv2.destroyAllWindows()
            
