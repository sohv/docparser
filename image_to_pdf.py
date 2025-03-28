from PIL import Image
from reportlab.pdfgen import canvas
import os

def convert_image_to_pdf(image_path, output_path=None):
    try:
        img = Image.open(image_path)
        if output_path is None:
            output_path = os.path.splitext(image_path)[0] + '.pdf'
        img_width, img_height = img.size
        
        # create a new PDF
        c = canvas.Canvas(output_path, pagesize=(img_width, img_height)) 
        # draw the image on the PDF
        c.drawImage(image_path, 0, 0, img_width, img_height)
        # save the PDF
        c.save()
        return output_path
        
    except Exception as e:
        print(f"Error converting image to PDF: {str(e)}")
        return None

if __name__ == "__main__":
    image_path = "images/sample.jpg"
    pdf_path = convert_image_to_pdf(image_path)
    
    if pdf_path:
        print(f"PDF created successfully at: {pdf_path}")
    else:
        print("Failed to create PDF")