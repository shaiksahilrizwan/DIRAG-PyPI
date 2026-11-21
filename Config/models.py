from pydantic import BaseModel,Field
from typing import Optional
class QueryClassifier(BaseModel):
    isRAGRequired:bool=Field(description="This field is True if the User Query required additional information that can be fetched from Vector Store else False")
    query:str|None=Field(description="The Query that needes to be used for Semantic Retrieval of Data for answering the User's question and this field is optional mark it as None if the user's question doesn't require context/external Information")