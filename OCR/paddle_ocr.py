from paddleocr import PaddleOCR


def extract_text_from_image(img_path, lang='en'):
    ocr = PaddleOCR(lang=lang, use_angle_cls = True)
    result = ocr.ocr(img_path)
    detected_texts = [line[1][0] for line in result[0]]
    final_text = " ".join(detected_texts)
    return final_text