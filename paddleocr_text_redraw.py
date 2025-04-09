import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# Load the image
image_path = "/Users/varshini/Desktop/SOP/sample_ocr.jpg"
image = cv2.imread(image_path)

# Convert to RGB for PaddleOCR
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Initialize PaddleOCR with a lower detection threshold
ocr = PaddleOCR(
    use_angle_cls=True, 
    lang="en", 
    det_db_box_thresh=0.3,  # Lower threshold to detect faint/small text
    det_db_unclip_ratio=1.7,  # Expand detection box slightly for better coverage
    rec_algorithm="CRNN",
    det_model_dir="/Users/varshini/Desktop/POCR/ch_ppocr_mobile_v2.0_det_train",  # Use a better detection model
    rec_model_dir="/Users/varshini/Desktop/POCR/en_number_mobile_v2.0_rec_slim_train",  # Use a better recognition model
)

# Perform OCR
results = ocr.ocr(image_path, cls=True)

# Convert image to PIL for drawing
image_pil = Image.fromarray(image_rgb)
draw = ImageDraw.Draw(image_pil)

# Load a font (adjust font path if needed)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font_size = 20
try:
    font = ImageFont.truetype(font_path, font_size)
except:
    font = ImageFont.load_default()

# Draw extracted text in place of the original text
for result in results[0]:  # Iterate over detected text
    bbox, (text, _) = result
    top_left = tuple(map(int, bbox[0]))  # Top-left corner
    bottom_right = tuple(map(int, bbox[2]))  # Bottom-right corner

    # Create a white rectangle to erase original text
    draw.rectangle([top_left, bottom_right], fill="white")

    # Write new text in the same position
    draw.text(top_left, text, fill="black", font=font)

# Save and display the modified image
output_path = "/Users/varshini/Desktop/POCR/cleaned_text_image5.png"
image_pil.save(output_path)

image_pil.show()

print(f"Processed image saved as {output_path}")

