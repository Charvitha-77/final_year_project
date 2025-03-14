import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma  # ✅ NEW (correct)
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
import google.generativeai as genai

os.environ["GOOGLE_API_KEY"] = "AIzaSyAiKQRtNpdWFKkFtZSymD0Zl3l2HUzTzUw"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def get_model_response(file, query):
    """Processes a file, retrieves relevant documents, and generates a response."""
    
    if isinstance(file, list):
        context = "\n\n".join(file)
    elif isinstance(file, str):
        context = file
    else:
        raise ValueError("Invalid file format. Expected string or list of strings.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=568, chunk_overlap=200)
    data = text_splitter.split_text(context)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    searcher = Chroma.from_texts(data, embeddings).as_retriever()

    _template = """
    You have to answer the question from the given prompt.
    Context: {context}?

    Question: {question}

    Answer:
    """
    prompt = PromptTemplate(template=_template, input_variables=["context", "question"])

    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.9)
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    records = searcher.get_relevant_documents(query)

    response = chain.invoke({"input_documents": records, "question": query})
    
    return response
