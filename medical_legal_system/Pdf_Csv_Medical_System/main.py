import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
import streamlit as st
import pandas as pd
from langchain_community.document_loaders import CSVLoader
from medical_legal_system.utils.utils import get_model_response


DATA_STORAGE_PATH = "C:/Users/Charvitha Reddy/Downloads/corrected_project/medical_legal_system/storage/medical_legal_records.csv"

def load_csv_data():
    """Load the latest stored CSV directly (no manual upload required)."""
    if os.path.exists(DATA_STORAGE_PATH):
        return CSVLoader(file_path=DATA_STORAGE_PATH, encoding="utf-8").load()
    return None

def main():
    st.title("DataSolace: Medico-Legal Management System")

    documents = load_csv_data()
    
    if documents:
        file_text = "\n".join([doc.page_content for doc in documents])
        user_input = st.text_input("Your Query:")
        
        if user_input:
            response = get_model_response(file_text, user_input)
            st.write(response)
    else:
        st.error("No CSV data found. Please upload a PDF first.")

if __name__ == "__main__":
    main()
