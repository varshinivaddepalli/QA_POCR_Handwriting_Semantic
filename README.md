# 🧠 Smart PaddleOCR & Hadnwritten Documents Q&A System

Welcome to the **Smart OCR & PDF Q&A Suite** – a dual-script project leveraging **PaddleOCR, Tesseract, PDFPlumber**, and **LLaMA 3.1** to extract, redraw, and intelligently answer queries based on text from **images and PDFs**.

## 🔍 Project Overview

This project contains **two Python scripts**, each addressing a unique but complementary task:

1. `paddleocr_text_redraw.py`: Extracts and **redraws** text on images using **PaddleOCR**, giving a clean, editable version of the original document.

2. `docqa_paddle_tesseract_pdfplumber.py`: A **Streamlit-based interactive app** that accepts image/PDF uploads, extracts data using **OCR and PDF parsers**, and allows users to ask **natural language questions** using the **Meta LLaMA 3.1 model**.

---

## 🗂️ File Breakdown

### 1️⃣ `paddleocr_text_redraw.py`

| 🔍 Input Image (`Input1.png`) | 🎨 Redrawn Output (`Output1.png`) |
|------------------------------|-----------------------------------|
| ![Input](/Input1.png)  | ![Output](/Output1.png)    |

📌 **Purpose:**  
Redraws or replaces existing text in an image with cleanly rendered text at the same positions using OCR.

🛠 **Key Features:**
- Uses **PaddleOCR** with low detection thresholds for faint or small text.
- Supports custom-trained OCR detection and recognition models.
- Converts OpenCV image to PIL format to **overlay clean text**.
- Automatically replaces old text with extracted, readable text.
- Saves the updated image to disk.

🧪 **Use Case:**  
Perfect for cleaning scanned documents, forms, receipts, or documents with faint or distorted text.

📷 **Sample Input:** Scanned image with handwritten or printed text.  
🖼 **Sample Output:** Same image, with clear machine-rendered text replacing the original.

---

### 2️⃣ `docqa_paddle_tesseract_pdfplumber.py`

| 🖼 UI Preview |

| 🔍 Input Image (`Input1.png`) | 🎨 Output (`Output1.png`) |
|------------------------------|-----------------------------------|
| ![Input](/Input1.png)  | ![Output2](/Output2.gif)   |

📌 **Purpose:**  
Interactive tool that **extracts, analyzes, and answers** questions from uploaded **images or PDFs** using AI-powered OCR and LLMs.

🛠 **Key Features:**
- Web-based UI using **Streamlit**.
- Accepts `.jpg`, `.jpeg`, `.png`, and `.pdf` files.
- Dual OCR support: **PaddleOCR** and **Tesseract**.
- Table extraction from PDFs using **PDFPlumber**.
- Contextual Q&A using **Meta LLaMA 3.1 (via Friendli API)**.
- Text redrawing overlay (white background + clean text).
- Toggle for viewing detailed Tesseract OCR data.

🧪 **Use Case:**  
Ideal for students, professionals, or businesses who want to **interact with unstructured documents** – ask questions, extract insights, or digitize content.

💬 **Example Questions You Can Ask:**
- “What is the invoice total?”
- “What date is mentioned in this PDF?”
- “Summarize the contents of this image.”

---

## 🧱 Tech Stack

| Component          | Tech Used                          |
|-------------------|------------------------------------|
| OCR Engine         | PaddleOCR, Tesseract               |
| PDF Parsing        | PDFPlumber                         |
| LLM (Q&A)          | Meta LLaMA 3.1 (via Friendli API)  |
| UI Framework       | Streamlit                          |
| Image Processing   | OpenCV, PIL                        |
| Data Analysis      | Pandas                             |
| Font Handling      | DejaVu Sans                        |

---

## 🚀 How to Run

### 📦 Installation

First, clone the repository:

```bash
git clone https://github.com/varshinivaddepalli/QA_POCR_Handwriting_Semantic.git
cd QA_POCR_Handwriting_Semantic
```

Then, install all required libraries using:

```bash
pip install -r requirements.txt
```

---

### 📌 Prerequisites

Before running the scripts, make sure you have the following set up:

#### ✅ 1. OCR Model Files

Download and place the trained PaddleOCR model files in the following directory structure:

```
/POCR/
├── ch_ppocr_mobile_v2.0_det_train/
└── en_number_mobile_v2.0_rec_slim_train/
```

These are used for text detection and recognition by PaddleOCR.

#### ✅ 2. Tesseract OCR

Make sure **Tesseract OCR** is installed and added to your system’s PATH.

- [Installation Guide](https://github.com/tesseract-ocr/tesseract)
- For **Windows**, ensure the path to `tesseract.exe` is added to the environment variables.

#### ✅ 3. Friendli API Key

To use Meta LLaMA 3.1 for Q&A functionality, you need a valid **Friendli API key**.

1. Replace the following line in `docqa_paddle_tesseract_pdfplumber.py`:

```python
API_KEY = "your_friendli_api_key_here"
```

2. You can get your API key from [Friendli.ai](https://www.friendli.ai/)

---

### ▶️ Running the Scripts

#### 🔁 For Image Redraw:
```bash
python paddleocr_text_redraw.py
```

This will:
- Load your input image
- Perform OCR
- Replace old text with clean, black text
- Save and show the output image

---

#### 🌐 For Document Q&A Web App:
```bash
streamlit run docqa_paddle_tesseract_pdfplumber.py
```

This will:
- Launch a local Streamlit server
- Allow you to upload images or PDFs
- Extract and display the text
- Let you ask questions about the document
- Display AI-generated answers

---

## 📊 Sample Outputs

| Feature               | Output Example                                     |
|-----------------------|----------------------------------------------------|
| Image Redraw          | Clean image with extracted text rendered in place |
| PDF Text Extraction   | Full PDF text + tables in Streamlit                |
| Question Answering    | Answers based on document content                  |
| Tesseract Data Toggle | Table view of detected words with positions        |

---

## 💡 Future Improvements

- Add support for multiple pages in images (TIFF).
- Use FAISS + embeddings for document memory.
- Add multilingual OCR support.
- Enable PDF saving after text redrawing.

---

## 🙌 Credits

- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Meta LLaMA 3.1 via Friendli](https://friendli.ai/)
- [Streamlit](https://streamlit.io/)
- [PDFPlumber](https://github.com/jsvine/pdfplumber)

---

## 🧠 Author

**Varshini Vaddepalli**    
📍 Hyderabad, India

---
