import streamlit as st
from api_utils import upload_document, list_documents, delete_document

def display_sidebar():
    # Model selection
    model_options = ["gpt-4o", "gpt-4o-mini"]
    st.sidebar.selectbox("Select Model", options=model_options, key="model")

    # Document upload
    st.sidebar.header("Document Upload")
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["pdf", "docx", "html"])
    if uploaded_file is not None: # If a file is uploaded
        if st.sidebar.button("Upload"):
            with st.spinner("Uploading document..."):
                upload_response = upload_document(uploaded_file)
                if upload_response:
                    st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully with ID {upload_response['file_id']}.")
                    st.session_state.documents = list_documents()  # Refresh the list after uploa

    # Document list
    st.sidebar.header("Document List")
    if st.sidebar.button("Refresh Document List"):
        with st.spinner("Refreshing document list..."):
            st.session_state.documents = list_documents()

    # Initialize documents list if not present
    if "documents" not in st.session_state:
        st.session_state.documents = list_documents()   


    # View documents list in sidebar
    documents = st.session_state.documents
    if documents:
        for doc in documents:
            st.sidebar.text(f"{doc['filename']} (ID: {doc['id']}), Uploaded: {doc['upload_timestamp']}")

        # Delete document
        selected_file_id = st.sidebar.selectbox("Select a document to delete", options=[doc['id'] for doc in documents], format_func=lambda x: next(doc['filename'] for doc in documents if doc['id'] == x))

        if st.sidebar.button("Delete selected document"):
            with st.spinner("Deleting document..."):
                delete_response = delete_document(selected_file_id)
                if delete_response:
                    st.sidebar.success(f"Document with ID {selected_file_id} deleted successfully.")
                    st.session_state.documents = list_documents() # Refresh the list after delete
                else:
                    st.sidebar.error(f"Failed to delete document with ID {selected_file_id}.")
                    
            
