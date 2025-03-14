import streamlit as st
from PyMuPDF import fitz  # PyMuPDF
import pdf2image
import pytesseract
import pandas as pd
import re
import os
from io import BytesIO


CSV_FILE_PATH = "C:/Users/Charvitha Reddy/Downloads/corrected_project/medical_legal_system/storage/medical_legal_records.csv"


pytesseract.pytesseract.tesseract_cmd = r"C:/Users/Charvitha Reddy/Downloads/medical_legal/medical_legal_system/tesseract-ocr-w64-setup-5.5.0.20241111 (1).exe"

# Streamlit Page Configuration
st.set_page_config(page_title="Medico-Legal Document Conversion", page_icon="⚖", layout="wide")

# Sidebar UI
st.sidebar.title("📑 Medico-Legal document conversion")
st.sidebar.info("Upload and manage medico-legal records with AI-powered processing.")
uploaded_file = st.sidebar.file_uploader("📤 Upload a Medico-Legal PDF", type=["pdf"])

# Title and Description
st.markdown("""
    <h1 style='text-align: center; color: #2E86C1;'>Medico-Legal Document Management System </h1>
    <p style='text-align: center; color: #5D6D7E;'>Easily extract, store, and manage medico-legal records in a structured format.</p>
""", unsafe_allow_html=True)

# Function to extract text from a standard PDF
def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read()) as doc:
        for page in doc:
            text += page.get_text("text") + "\n"
    return text.strip()

# Function to extract text from scanned PDFs using OCR
def extract_text_from_scanned_pdf(pdf_file):
    images = pdf2image.convert_from_bytes(pdf_file.read())
    text = ""
    for img in images:
        text += pytesseract.image_to_string(img) + "\n"
    return text.strip()

# Function to parse medico-legal text into structured format
def parse_medico_legal_text(text):
    attributes = [
        "Case ID", "Patient Name", "Age", "Gender", "Case Description",
        "Diagnosis", "Treatment Plan", "Date of Injury", "Doctor's Opinion",
        "Legal Opinion", "Case Status", "Court Case Number",
        "Legal Actions Taken", "Date of Legal Filing"
    ]
    
    case_data = {}
    for attr in attributes:
        pattern = rf"{attr}:\s*(.*)"
        match = re.search(pattern, text, re.IGNORECASE)
        case_data[attr] = match.group(1).strip() if match else ""

    return pd.DataFrame([case_data])

# Function to store extracted data into a CSV file
def append_to_csv(new_data, csv_path):
    if os.path.exists(csv_path):
        existing_data = pd.read_csv(csv_path)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(csv_path, index=False)
    return updated_data

# File Upload Handling
if uploaded_file:
    with st.spinner("🔍 Extracting text from the PDF..."):
        text = extract_text_from_pdf(uploaded_file)
        if not text.strip():
            text = extract_text_from_scanned_pdf(uploaded_file)

    if text:
        df = parse_medico_legal_text(text)
        if not df.empty:
            final_df = append_to_csv(df, CSV_FILE_PATH)
            st.success(" Data successfully extracted and added to the CSV file!")
            
            st.markdown("""
                <h3 style='color: #1ABC9C;'> Extracted Details</h3>
            """, unsafe_allow_html=True)
            for index, row in df.iterrows():
                st.json(row.to_dict())
                
            st.markdown("""
                <h3 style='color: #F39C12;'>📂 Updated Medico-Legal Records</h3>
            """, unsafe_allow_html=True)
            st.dataframe(final_df, use_container_width=True)
        else:
            st.error(" Unable to extract structured information from the document.")
    else:
        st.error(" Unable to extract text. Please check the PDF format.")
