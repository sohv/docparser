from paddleocr import PaddleOCR
import cv2
import numpy as np

ocr = PaddleOCR(
    use_angle_cls=False,
    lang='en',
    use_gpu=False,
    enable_mkldnn=True,
    cpu_threads=4
)

def preprocess_image(img_path):
    image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    
    max_dimension = 1024
    h, w = image.shape
    if max(h, w) > max_dimension:
        scale = max_dimension / max(h, w)
        image = cv2.resize(image, None, fx=scale, fy=scale)
    
    thresh = cv2.threshold(
        image,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]
    
    return thresh

def extract_text_from_image(img_path, lang='en'):
    preprocessed_img = preprocess_image(img_path)
    
    result = ocr.ocr(
        preprocessed_img,
        det=False,
        cls=False,
        rec_batch_num=1
    )
    
    extracted_lines = [line for res in result for line in res]
    return extracted_lines

def test_ocr():
    test_image_path = "images/figure-65.png"
    print(extract_text_from_image(test_image_path))

if __name__ == "__main__":
    test_ocr()
    

'''
To-do
- Resolve Numpy conflicting versions
- Optimize the OCR process
- Reduce the chunks and CPU threads
'''