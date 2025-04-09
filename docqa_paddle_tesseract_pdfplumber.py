import streamlit as st
import cv2
import numpy as np
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import pdfplumber
import pandas as pd
import os
import requests
import json
from io import BytesIO

# Friendli API setup
API_URL = "https://api.friendli.ai/serverless/v1/chat/completions"
API_KEY = "flp_KlaAuMmfSJLERI6a6UNtAy3UZnZjmLiFGv8wY6DF9zW032"  # Replace with your API Key
MODEL_NAME = "meta-llama-3.1-8b-instruct"

# PaddleOCR initialization
ocr = PaddleOCR(
    use_angle_cls=True,
    lang="en",
    det_db_box_thresh=0.3,
    det_db_unclip_ratio=1.7,
    rec_algorithm="CRNN",
    det_model_dir="/Users/varshini/Desktop/POCR/ch_ppocr_mobile_v2.0_det_train",
    rec_model_dir="/Users/varshini/Desktop/POCR/en_number_mobile_v2.0_rec_slim_train",
)

# Function to run PaddleOCR
def run_paddle_ocr(image_path):
    results = ocr.ocr(image_path, cls=True)
    return results

# Function to draw OCR results
def draw_ocr_text(image_rgb, results):
    image_pil = Image.fromarray(image_rgb)
    draw = ImageDraw.Draw(image_pil)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_size = 20

    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    full_text = ""
    for result in results[0]:
        bbox, (text, _) = result
        top_left = tuple(map(int, bbox[0]))
        bottom_right = tuple(map(int, bbox[2]))
        draw.rectangle([top_left, bottom_right], fill="white")
        draw.text(top_left, text, fill="black", font=font)
        full_text += text + " "
    
    return image_pil, full_text

# Function to use pytesseract for detailed OCR
def extract_text_tesseract(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    config = r'--oem 3 --psm 6'
    data = pytesseract.image_to_data(gray, config=config, output_type=pytesseract.Output.DATAFRAME)
    data = data[data.text.notnull()].reset_index(drop=True)
    return data

# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    text_blocks = []
    tables_list = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text_blocks.append(page.extract_text())
            tables = page.extract_tables()
            if tables:
                df = pd.DataFrame(tables[0][1:], columns=tables[0][0])
                tables_list.append(df)

    combined_text = "\n".join(filter(None, text_blocks))
    return combined_text, tables_list

# Function to send query to Friendli API
def ask_llama(prompt, context):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that answers questions based on OCR or PDF-extracted content."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {prompt}"}
        ],
        "temperature": 0.2,
    }

    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"⚠️ Error: {response.status_code} - {response.text}"

# ==== Streamlit UI ====
st.title("📄 Smart OCR & PDF Q&A with Meta LLaMA 3.1")

uploaded_file = st.file_uploader("Upload an Image or PDF", type=["jpg", "jpeg", "png", "pdf"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1].lower()
    context_text = ""
    
    if file_extension in ["jpg", "jpeg", "png"]:
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_path = "temp_uploaded_image.jpg"
        cv2.imwrite(image_path, image)

        # Run OCR
        results = run_paddle_ocr(image_path)
        drawn_image, context_text = draw_ocr_text(image_rgb, results)
        st.image(drawn_image, caption="📝 OCR Annotated Image")

        # Optionally show Tesseract text
        if st.checkbox("Show Tesseract Data"):
            tesseract_data = extract_text_tesseract(image)
            st.write(tesseract_data[['left', 'top', 'width', 'height', 'text']])

    elif file_extension == "pdf":
        temp_path = "temp_uploaded_pdf.pdf"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        
        context_text, tables_list = extract_text_from_pdf(temp_path)
        st.text_area("🧾 Extracted PDF Text:", context_text[:1000], height=200)

        if tables_list:
            st.write("📊 Extracted Tables:")
            for df in tables_list:
                st.dataframe(df)

    # Ask a question
    st.subheader("❓ Ask a question about the document")
    user_question = st.text_input("Your Question")

    if user_question and context_text:
        with st.spinner("Thinking..."):
            answer = ask_llama(user_question, context_text)
        st.markdown("💬 **Answer:**")
        st.success(answer)
