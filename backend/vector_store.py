import os
import toml
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ✅ Load OpenAI API Key from secrets.toml
secrets = toml.load("secrets.toml")
openai_api_key = secrets["openai"]["api_key"]

# ✅ Load PDF
pdf_path = "File/ucb_faq.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# ✅ Split into 50–60 words with 20-word overlap
class WordCountTextSplitter:
    def __init__(self, chunk_size=60, chunk_overlap=20):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents):
        chunks = []
        for doc in documents:
            words = doc.page_content.split()
            start = 0
            while start < len(words):
                end = min(start + self.chunk_size, len(words))
                chunk_text = " ".join(words[start:end])
                chunks.append(doc.__class__(page_content=chunk_text, metadata=doc.metadata))
                start += self.chunk_size - self.chunk_overlap
        return chunks

splitter = WordCountTextSplitter(chunk_size=60, chunk_overlap=20)
docs = splitter.split_documents(pages)

# ✅ Embed and Store in Chroma
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

vectordb = Chroma.from_documents(
    documents=docs,
    embedding=embedding,
    persist_directory="chroma_db"
)

vectordb.persist()
print("✅ Chunks stored in ChromaDB")
print(len(docs))
print(docs[0].page_content)