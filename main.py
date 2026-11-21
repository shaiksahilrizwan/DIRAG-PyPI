from langchain_ollama import ChatOllama,OllamaEmbeddings
from langchain_core.output_parsers import StrOutputParser
from Config.configLoader import ConfigLoader
from Exceptions.exceptions import InvalidConfigJson,InvalidDictKeys
from ChatHandler.chat import Chat
from ollama import ResponseError
from rich.prompt import Prompt
from rich.panel import Panel
from rich.console import Console
from typing import Optional
import typer
import click
import os
from Config.directoryLoaderPDF import DirectoryLoaderPDF
from Config.textSpliter import RecursiveTextSplitter
from Config.vectorStoreHandler import VectorStoreHandler
from Config.models import QueryClassifier
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
app = typer.Typer(no_args_is_help=True)


@app.callback()
def main() -> None:
    """DIRAG command line interface."""
    return None

@app.command()
def chat(session_id: str | None = typer.Option(None, "--session")
):
    loader=ConfigLoader()
    try:
        loader=ConfigLoader()
        console=Console()
        if loader.config:
            config=loader.get_config()
        else:
            raise InvalidConfigJson('Malformed Config JSON can not start the chat')
        if config['ollama_url']!='localhost':
            llm=ChatOllama(base_url=config['ollama_url'],model=config['model'])
        else:
            llm=ChatOllama(base_url=config['ollama_url'],model=config['model'])
        if session_id:
            chat_context=Chat()
            chat_context.load_session(session_id)
            for msgs in chat_context.writable_chat_hist:
                print(msgs)
                for key,value in msgs.items():
                    if key=='human':
                        console.print(f'[bold cyan]You:[/]{value}')
                    elif key=='ai':
                        console.print( Panel(
                                                        value,
                                                        title='AI',
                                                        border_style="green"
                                                    ))
                    else:
                        continue
        else:
            chat_context=Chat(system_prompt="You are Useful AI Assistent")
        parser=StrOutputParser()
        classifier_parser=PydanticOutputParser(pydantic_object=QueryClassifier)
        isRagSession=False
        if "embed_model" in config and "collection_name" in config:
            print("Found RAG Configuration, Now checking for Documents....")
            if any(file.lower().endswith(".pdf") for file in os.listdir(os.getcwd())):
                print("Documents Found!")
                isRagSession=True
                folder = "vstore"
                if os.path.isdir(folder) and len(os.listdir(folder)) > 0:
                    print("Vector Store Folder exists and is not empty")
                else:
                    Docloader=DirectoryLoaderPDF(os.getcwd())
                    splitter=RecursiveTextSplitter(100,25)
                    docs=splitter.get_chunks(Docloader.load_all_docs())
                    if config['ollama_url'!='localhost']:
                        emdl=OllamaEmbeddings(base_url=config['base_url'],model=config['embed_model'])
                    else:
                        emdl=OllamaEmbeddings(model=config['embed_model'])
                    vc=VectorStoreHandler(collection_name=config['collection_name'],embed_model=emdl,model=config['embed_model'])
                    vc.save_docs(docs)
            else:
                    print("Documents Not Found Starting Normal Chat")
        #Chat Loop
        while True:
            human_message=Prompt.ask('[bold cyan]You')
            if (human_message.lower())=='exit':
                chat_context.save_new_session()
                break
            chat_context.add_human_message(human_message)
            if isRagSession:
                prompt=PromptTemplate(template="""The User query is :{chat_message} and there is a vector store that contains information related to user query and you need to classify weather this query needs additional information retireval make it strict because 
                                            each retrieval costs money so if there is 50 percent chance 
                                        that normal llm without extra context can answer the question then no need to exxtra source information and give the response in {format_instructions}""",input_variables=['chat_message'],partial_variables={'format_instructions':classifier_parser.get_format_instructions()})
                prompt=prompt.invoke({'chat_message':chat_context.human_message})
                res=llm.invoke(prompt)
                print(res)
                classifier_result=classifier_parser.parse(res.content)
                if classifier_result.isRAGRequired:
                    context_docs=vc.get_docs(classifier_result.query,k=2)
                    context=''
                    for i in context_docs:
                        context+=i.page_content
                    updated_msg=human_message+f",  Use the Information: {context} to answer the question only if this context is useful or else relay on your Knowledge"
                    chat_context.chat_hist.pop()
                    chat_context.writable_chat_hist.pop()
                    chat_context.add_human_message(updated_msg)                
            chat_template=chat_context.get_chat_prompt()
            chain=chat_template|llm|parser
            ai_message=chain.invoke({})
            chat_context.add_ai_message(ai_message)
            console.print( Panel(
                                ai_message,
                                title='AI',
                                border_style="green"
                            ))
            print(chat_context.writable_chat_hist)
            print(chat_context.chat_hist)
    except InvalidDictKeys as e:
        print('Invalid json keys In Configuration file check it and re-run')
    except FileNotFoundError as e:
        print('No Configuration file drag.json found in current Directory')
    except ResponseError as e:
        if e.status_code == 400 and 'exceeds the available context size' in e.error:
            print('Context window exceeded! Use new chat!')
        else:
            print(f'Ollama API error: {str(e)}')
    except Exception as e:
        print(f'Error Occurred: {str(e)}')
    # def existing_chat(session_id:str):
    # finally:
    #     chat_context.save_new_session()

if __name__=='__main__':
    app()