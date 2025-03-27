# 🔍 A Retrieval-Augmented Generation System  

This project implements a **Retrieval-Augmented Generation (RAG)** system using **FastAPI**, **Streamlit**, **LangChain**, **ChromaDB**, and **SQLite**. The system enables efficient retrieval of relevant documents and enhances responses with LLM-powered generation.

## 🚀 Getting Started  

### 1️⃣ Run the FastAPI Backend  
The FastAPI server handles API requests and document retrieval.  

**Command:**  
```sh
uvicorn api.main:app --reload
```
- The FastAPI app is located in the `api/` folder.

### 2️⃣ Run the Streamlit Frontend  
The Streamlit app provides a user-friendly interface for querying the system.  

**Command:**  
```sh
streamlit run app/app.py
```
- The Streamlit app is located in the `app/` folder.

---

## 🛠️ Tech Stack  

### 🔹 FastAPI  
A high-performance Python web framework used to build the API for querying and retrieving documents.  

### 🔹 Streamlit  
A lightweight Python library for building interactive web applications, used here for the frontend.  

### 🔹 LangChain  
A powerful framework for building applications that integrate LLMs with external data sources, enabling enhanced responses in the RAG pipeline.  

### 🔹 ChromaDB  
An open-source **vector database** for efficient similarity searches, used to store and retrieve document embeddings.  

### 🔹 SQLite  
A lightweight relational database used for structured data storage within the system.  

---

## 📌 Features  
✅ Fast document retrieval using **ChromaDB**  
✅ Seamless API integration with **FastAPI**  
✅ Interactive web interface powered by **Streamlit**  
✅ LLM-powered response generation with **LangChain**  
✅ Lightweight storage with **SQLite**  

---

## 📜 License  
This project is open-source. Feel free to contribute and improve! 🚀