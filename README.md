🩺 Medico-Legal Records Management System
📘 Overview

The Medico-Legal Records Management System is an AI-powered web application that helps efficiently maintain, organize, and retrieve medico-legal records.
It minimizes search time, reduces manual effort, and ensures secure, structured, and intelligent data handling.

⚙️ Key Features

  🧾 Automated Data Extraction: Extracts data from PDF/CSV medico-legal records using OCR (Tesseract).

  🧠 AI-Powered Querying: Allows users to ask natural language questions using the MedGemini model via LangChain.

  📊 ChromaDB Integration: Stores and searches document embeddings for quick retrieval.

  💬 Interactive Chat Interface: Built with Streamlit for easy user interaction.

  🔍 Data Validation: Detects missing, duplicate, or inconsistent fields automatically.

  🧱 Secure Data Management: Ensures structured access and protection of sensitive medico-legal information.

🧰 Tech Stack
  Component	Technology Used
  Frontend	Streamlit
  Backend	Python  
  LLM Framework	LangChain
  Model	MedGemini (Google Generative AI)
  Database	ChromaDB
  OCR Engine	Tesseract
  Libraries	Pandas, tempfile, PyPDF2, LangChain, Streamlit, ChromaDB
🚀 Project Workflow

  File Upload: User uploads PDF or CSV medico-legal records.
  Data Extraction: System extracts and processes text using OCR.
  Embedding Storage: Records are stored in ChromaDB for semantic search.
  AI Query Handling: User asks queries like
                    “Show records with missing witness details”
                    “Find duplicate case IDs”

                    LLM Response: The MedGemini model provides an accurate and contextual answer.
