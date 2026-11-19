from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from configLoader import ConfigLoader
from exceptions import InvalidConfigJson,InvalidDictKeys
from chat import Chat
from ollama import ResponseError
from rich.prompt import Prompt
from rich.panel import Panel
from rich.console import Console
def main(session_id:str=None):
    loader=ConfigLoader()
    try:
        loader=ConfigLoader()
        console=Console()
        if loader.config:
            config=loader.get_config()
        else:
            raise InvalidConfigJson('Malformed Config JSON can not start the chat')
        llm=ChatOllama(base_url=config['ollama_url'],model=config['model'])
        if session_id:
            chat_context=Chat()
            chat_context.load_session(session_id)
        else:
            chat_context=Chat(system_prompt="You are Useful AI Assistent")
        parser=StrOutputParser()
        #Chat Loop
        while True:
            human_message=Prompt.ask('[bold cyan]You')
            if (human_message.lower())=='exit':
                chat_context.save_new_session()
                break
            chat_context.add_human_message(human_message)
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
            print(f'Ollama API error: {e.error}')
    except Exception as e:
        print(f'Error Occurred: {str(e)}')
    # def existing_chat(session_id:str):
    # finally:
    #     chat_context.save_new_session()

if __name__=='__main__':
    main('20261119_144556')