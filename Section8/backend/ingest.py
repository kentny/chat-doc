import os
import shutil
from typing import List
from langchain import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma

from dotenv import load_dotenv
load_dotenv()

vectorestore_qdrant_path = "./vectorestore/local_qdrant"
vectorestore_qdrant_collection_name = "my_documents"
vectorestore_chroma_path = "./vectorestore/local_chroma"

def ingest(file_path: str):
    """Ingest vector data from the file and populate the database"""

    loader = PyPDFLoader(file_path)
    text_splitter = CharacterTextSplitter(separator='。', chunk_size=100, chunk_overlap=20)
    docs = loader.load_and_split(text_splitter=text_splitter)

    for doc in docs:
        print(doc)
        print('======================')

    embeddings = OpenAIEmbeddings()

    # Qdrant.from_documents(
    #     docs,
    #     embeddings, 
    #     path=vectorestore_qdrant_path,
    #     collection_name=vectorestore_qdrant_collection_name,
    # )
    
    # Delete the existing database in vectorestore_chroma_path.
    if os.path.exists(vectorestore_chroma_path):
        shutil.rmtree(vectorestore_chroma_path)
        print("The database has been deleted.")
    else:
        print("The database does not exist.")

    vectordb = Chroma.from_documents(docs, embeddings, persist_directory=vectorestore_chroma_path)
    vectordb.persist()


def generate_answer(query: str) -> str:
    docs = _similarity_search(query)
    for doc in docs:
        print(doc)
        print('======================')
    template = """Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that you don't know, don't try to make up an answer.

    {context}

    Question: {question}
    Answer in JAPANESE:"""
    prompt = PromptTemplate(
        template=template, input_variables=["context", "question"]
    )
    chain = load_qa_chain(ChatOpenAI(temperature=0.7), prompt=prompt)
    
    answer = chain.run(input_documents=docs, question=query)
    print(f'''answer: {answer}''')
    return answer


def generate_answer_with_source(query: str) -> str:
    docs = _similarity_search(query)
    template = """Given the following extracted parts of a long document and a question, create a final answer with references ("SOURCES"). 
    If you don't know the answer, just say that you don't know. Don't try to make up an answer.
    ALWAYS return a "SOURCES" part in your answer.
    Respond in JAPANESE.

    QUESTION: {question}
    =========
    {summaries}
    =========
    FINAL ANSWER IN JAPANESE:"""
    prompt = PromptTemplate(template=template, input_variables=["summaries", "question"])
    chain = load_qa_with_sources_chain(ChatOpenAI(temperature=0.7), prompt=prompt)

    result = chain({"input_documents": docs, "question": query}, return_only_outputs=True)
    answer = result["output_text"]
    print(f'''result: {result}''')
    print(f'''answer: {answer}''')
    return answer


def _similarity_search(query: str) -> List[Document]:
    embeddings = OpenAIEmbeddings()

    # client = qdrant_client.QdrantClient(
    #     path=vectorestore_qdrant_path,
    #     prefer_grpc=True,
    # )
    # qdrant = Qdrant(
    #     client=client,
    #     collection_name=vectorestore_qdrant_collection_name, 
    #     embedding_function=embeddings.embed_query
    # )
    # return qdrant.similarity_search(query, 5)

    vectordb = Chroma(persist_directory=vectorestore_chroma_path, embedding_function=embeddings)
    return vectordb.similarity_search(query, 5)

