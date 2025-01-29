from paddleocr import PaddleOCR
import cv2
import numpy as np
import platform

'''
def get_device_info():
    """
    Check if Apple Silicon GPU is available
    Returns:
        tuple: (use_gpu boolean, device_type string)
    """
    is_mac = platform.system() == 'Darwin'
    
    is_arm = platform.machine() == 'arm64'
    use_gpu = is_mac and is_arm
    device_type = "Apple Silicon GPU (Metal)" if use_gpu else "CPU"
    return use_gpu, device_type

# Initialize device settings
use_gpu, device_type = get_device_info()
print(f"Using device: {device_type}")
'''

def preprocess_image(img_path):
    """
    Preprocess image with thresholding for better OCR results
    Args:
        img_path (str): Path to the image file
    Returns:
        numpy.ndarray: Preprocessed image
    """
    image = cv2.imread(img_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # adaptive thresholding
    thresh = cv2.adaptiveThreshold(
        gray, 
        255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        11, 
        2
    )
    
    return thresh

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