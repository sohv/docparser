import easyocr

def extract_text_from_image(img_path, lang_list=['en']):
    reader = easyocr.Reader(lang_list)
    result = reader.readtext(img_path)
    extracted_text = " ".join([text[1] for text in result])
    return extracted_text


