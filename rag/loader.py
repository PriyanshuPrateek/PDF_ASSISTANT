
from langchain_community.document_loaders import PDFMinerLoader

def load_documents(path):
    loader =  PDFMinerLoader(path)
    return loader.load()