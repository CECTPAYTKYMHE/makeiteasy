import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
pages = convert_from_path('D:/B3.pdf', 500,poppler_path='D:/django/poppler-22.04.0/Library/bin')

for pageNum,imgBlob in enumerate(pages):
    text = pytesseract.image_to_string(imgBlob,lang='rus')

with open(f'{"D:/B3.pdf"[:-4]}_page{pageNum}.txt', 'w') as the_file:
    the_file.write(text)
the_file.close()


# import cv2
# import pytesseract
# from pytesseract import Output
# import csv

# pages = convert_from_path('D:/B3.pdf', 500,poppler_path='D:/django/poppler-22.04.0/Library/bin')

# for pageNum,imgBlob in enumerate(pages):
#     # text = pytesseract.image_to_string(imgBlob,lang='rus')
#     byteIO = io.BytesIO()
#     imgBlob.save(byteIO, format='PNG')
#     byteArr = byteIO.getvalue()
#     # byteArr = np.asarray(imgBlob)
#     nparr = np.frombuffer(byteArr, np.uint8)
#     image = cv2.imdecode(nparr, flags=1)
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

#     pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
#     custom_config = r'--oem 3 --psm 6'
#     details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='rus')

#     total_boxes = len(details['text'])
#     for sequence_number in range(total_boxes):
#         if int(float((details['conf'][sequence_number]))) > 30:
#             (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
#             threshold_img = cv2.rectangle(threshold_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
 
#     parse_text = []

#     word_list = []

#     last_word = ''
#     print(details['text'])
#     for word in details['text']:
#         if word!='':
#             word_list.append(word)
#             last_word = word
#             if (last_word!='' and word == '') or (word==details['text'][-1]):
#                 parse_text.append(word_list)
#                 word_list = []



#     with open('D:/result_text.txt',  'w', newline="") as file:
#         csv.writer(file, delimiter=" ").writerows(parse_text)