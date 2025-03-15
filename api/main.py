# Entry point for FastAPI application

from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic_models import QueryInput, QueryResponse, DocumentInfo, DeleteFileRquest
from langchain_utils import get_rag_chain
from db_utils import insert_application_logs, get_chat_history, get_all_documents, insert_document_record, delete_document_record
from chroma_utils import index_document_to_chroma, delete_doc_from_chroma

import os
import uuid
import logging
import shutil
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Set up logging
logging.basicConfig(filename='app.log', level=logging.INFO)


# Initialize the FastAPI app
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Chatbot API. Please refer to the documentation for usage instructions."}


# Main endpoints 

## Chat endpoint
@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput):
    session_id = query_input.session_id or str(uuid.uuid4())
    logging.info(f"Session ID: {session_id}, User Query: {query_input.question}, Model: {query_input.model.value}")

    chat_history = get_chat_history(session_id)
    rag_chain = get_rag_chain(query_input.model.value)
    answer = rag_chain.invoke(
        {
            "input": query_input.question,
            "chat_history": chat_history
        }
    )['answer']  # Because the query response is a dictionary set by pydantic_models.py

    insert_application_logs(session_id, query_input.question, answer, query_input.model.value)
    logging.info(f"Session ID: {session_id}, AI Response: {answer}")
    return QueryResponse(answer=answer, session_id=session_id, model=query_input.model)


## Document upload endpoint
@app.post("/upload-doc")
def upload_and_index_document(file: UploadFile = File(...)):
    allowed_extensions = ['pdf', 'docx', 'html']
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}")
    
    temp_file_path = f"temp_{file.filename}"

    try:
        # save the uploaded file to a temporary location
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename)
        success = index_document_to_chroma(temp_file_path, file_id)

        if success:
            return {"message": f"File {file.filename} has been successfully uploaded and indexed.", "file_id": file_id}
        else:
            delete_document_record(file_id)
            raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")
    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

# list all documents endpoint
@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents():
    return get_all_documents()

# delete document endpoint
@app.post("/delete-doc")
def delete_document(request: DeleteFileRquest):
    chroma_delete_success = delete_doc_from_chroma(request.file_id)

    if chroma_delete_success:
        db_delete_scuccess = delete_document_record(request.file_id)
        if db_delete_scuccess:
            return {"message": f"Successfully deleted document with file_id {request.file_id} from the system."}
        else:
            return {"error": f"Deleted from Chroma but failed to delete document with file_id {request.file_id} from the database."}
    else:
        return {"error": f"Failed to delete document with file_id {request.file_id} from Chroma."}