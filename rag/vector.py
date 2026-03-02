import os
import shutil
from langchain_community.vectorstores import FAISS

INDEX_PATH = "faiss_index"

def create_or_load_vectorstore(texts, embeddings):

    if os.path.exists(INDEX_PATH):
        shutil.rmtree(INDEX_PATH)

    vectorstore = FAISS.from_documents(texts, embeddings)
    vectorstore.save_local(INDEX_PATH)

    return vectorstore
