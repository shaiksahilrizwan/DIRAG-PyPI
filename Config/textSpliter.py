from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
class RecursiveTextSplitter():
    def __init__(self,chunk_size:int,chunk_overlap:int):
        self.splitter=RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap)
        self.chunks=None
    def get_chunks(self,docs:list[Document]):
        self.chunks=self.splitter.split_documents(docs)
        return self.chunks
        