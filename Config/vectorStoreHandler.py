from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from Exceptions.exceptions import VectorStoreSaveError,VectorSearchFail
# from Config.configLoader import ConfigLoader
import os
import json
class VectorStoreHandler():
    def __init__(self,embed_model:OllamaEmbeddings,collection_name:str):
        self.embed_model=embed_model
        try:
            self.vector_store=Chroma(embedding_function=self.embed_model,persist_directory=os.getcwd()+'\\vstore',collection_name=collection_name)
        except Exception as e:
            raise VectorStoreSaveError("Unable to start Vector Store Instance")
        self.collection_name=collection_name
    def save_docs(self,docs):#,collection_name):
        if not(os.path.isdir('vstore')):
            os.mkdir('vstore')
        try:
            # self.collection_name=collection_name
            #self.vector_store=Chroma(embedding_function=self.embed_model,persist_directory=os.getcwd()+'/vstore',collection_name=self.collection_name)
            self.vector_store.add_documents(docs)
            # config=ConfigLoader()
            # old_config=config.get_config()
            # old_config['collection_name']=collection_name
            # with open(f'{os.getcwd()}'+'\\dirag.json','r+') as fp:
            #     json.dump(old_config)
        except Exception as e:
            raise VectorStoreSaveError('Unable to Save Documents in Vector Store')
    def get_docs(self,search_query:str,no_records:int):
        try:
            return self.vector_store.similarity_search(query=search_query,k=no_records)
        except Exception as e:
            raise VectorSearchFail("Failed to get relavent Info")
                    