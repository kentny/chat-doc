import os
import shutil
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from dotenv import load_dotenv
load_dotenv()

from config import vectorestore_chroma_path

def ingest(file_path: str):
    """Ingest vector data from the file and populate the database"""

    loader = PyPDFLoader(file_path)
    text_splitter = CharacterTextSplitter(separator='。', chunk_size=100, chunk_overlap=20)
    docs = loader.load_and_split(text_splitter=text_splitter)

    for doc in docs:
        print(doc)
        print('======================')

    embeddings = OpenAIEmbeddings()
    
    # Delete the existing database in vectorestore_chroma_path.
    if os.path.exists(vectorestore_chroma_path):
        shutil.rmtree(vectorestore_chroma_path)
        print("The database has been deleted.")
    else:
        print("The database does not exist.")

    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=vectorestore_chroma_path)
    vectordb.persist()
