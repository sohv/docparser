from paddleocr import PaddleOCR

def extract_text_from_image(img_path, lang='en'):

    ocr = PaddleOCR(lang=lang)
    result = ocr.ocr(img_path, det=False, cls=False)
    
    extracted_lines = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            extracted_lines.append(line)
    
    return extracted_lines

# test the OCR model on a sample image
def test_ocr():
    test_image_path = "images/figure-65.png"
    print(extract_text_from_image(test_image_path))

if __name__ == "__main__":
    test_ocr()