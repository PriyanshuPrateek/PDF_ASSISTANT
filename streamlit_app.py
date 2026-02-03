import os
import streamlit as st
from langchain_groq import ChatGroq
from config import groq_api_key,model_name
from rag.loader import load_documents
from rag.splitter import split_documents
from rag.embedding import get_embeddings
from rag.vector import create_or_load_vectorstore
from rag.retriever import get_retriever
#from memory.memory import save_chat, get_chat_history
from prompts.prompt import build_prompt


# Page Config

st.set_page_config(page_title="ASSISTANT", layout="wide")
st.title("📚 PEEK INTO PDF")



# Session State Initialization
if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "loaded_file" not in st.session_state:
    st.session_state.loaded_file = None

if "chat_ui" not in st.session_state:
    st.session_state.chat_ui = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = ""



# Sidebar UI

with st.sidebar:
    st.header("Controls")

    if st.session_state.loaded_file:
        st.write("📄 Current Document:")
        st.write(st.session_state.loaded_file)

    if st.button("🧹 Clear Chat"):
        st.session_state.chat_ui = []



# File Upload
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file is not None:

    # Only rebuild if a new file is uploaded
    if st.session_state.loaded_file != uploaded_file.name:

        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())

        st.success("PDF uploaded successfully")

        with st.spinner("Processing document..."):

            document = load_documents("temp.pdf")
            texts = split_documents(document)
            embeddings = get_embeddings()
            vectorstore = create_or_load_vectorstore(texts, embeddings)
            st.session_state.retriever = get_retriever(vectorstore)

        st.session_state.loaded_file = uploaded_file.name
        st.session_state.chat_ui = []  # reset chat for new document
        st.success("Document ready for chat!")



# Chat Section

if st.session_state.retriever:

    llm = ChatGroq(
        groq_api_key= groq_api_key,
        model_name=model_name
    )

    user_query = st.chat_input("Ask something about the document...")

    if user_query:

        st.session_state.chat_ui.append(("user", user_query))

        chat_history = st.session_state.chat_history

        if user_query.strip().lower() in ["thankyou", "thank you", "thanks"]:
            response = "You're welcome 😊"
        else:
           
            full_query = chat_history + "\nUser: " + user_query

            docs = st.session_state.retriever.invoke(full_query)
            context = "\n\n".join([doc.page_content for doc in docs])

            prompt = build_prompt(chat_history, context, user_query)

            result = llm.invoke(prompt)
            response = result.content
            st.session_state.chat_history += f"\nUser: {user_query}\nAssistant: {response}"

        # Store assistant response
        st.session_state.chat_ui.append(("assistant", response))

    # Display Chat History
   
    for role, message in st.session_state.chat_ui:
        with st.chat_message(role):
            st.markdown(message)
