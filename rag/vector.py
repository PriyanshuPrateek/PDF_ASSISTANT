import os
import shutil
from langchain_community.vectorstores import FAISS

INDEX_PATH = "faiss_index"

def create_or_load_vectorstore(texts, embeddings):
    
    # If index exists, delete it
    if os.path.exists(INDEX_PATH):
        print("Deleting old FAISS index...")
        shutil.rmtree(INDEX_PATH)

    print("Creating new FAISS index...")

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(INDEX_PATH)

    return vectorstore
