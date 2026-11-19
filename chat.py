from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import os
import json
from exceptions import SessionSaveError,InvalidSession
class Chat():
    "Chat Class to handel Chat History and more"
    def __init__(self,system_prompt:str=None):
        self.chat_hist=[]
        if system_prompt:
            self.chat_hist=[('system',system_prompt)]
        self.human_message=None
        self.ai_message=None
        self.writable_chat_hist=[]
    def add_human_message(self,human_message:str):
        self.chat_hist.append(('human',human_message))
        self.human_message=human_message
        self.writable_chat_hist.append({'human':human_message})
    def add_ai_message(self,ai_message:str):
        self.chat_hist.append(('ai',ai_message))
        self.ai_message=ai_message
        self.writable_chat_hist.append({'ai':ai_message})
    def get_chat_history(self):
        return self.chat_hist
    def get_chat_prompt(self):
        return ChatPromptTemplate(self.get_chat_history())
    def save_new_session(self):
        if not(os.path.isdir('sessions')):
            os.mkdir('sessions')
        try:
            with open(f'{os.getcwd()}'+'\\sessions\\'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.json','w+') as fp:
                json.dump(self.writable_chat_hist,fp,ensure_ascii=False)
        except Exception as e:
            raise SessionSaveError('Unable to Save Session')
    def load_session(self,session_id:str):
        try:
            data=None
            print(f'{os.getcwd()}'+"\\sessions\\"+session_id+".json")
            with open(f'{os.getcwd()}'+'\\sessions\\'+session_id+'.json','r+', encoding='utf-8') as fp:
                data=json.load(fp)
            if data:
                for element in data: 
                    for key,value in element.items():
                        if key=='system':
                            self.chat_hist.append((key,value))
                        if key=='ai':
                            self.add_ai_message((key,value))
                        elif key=='human':
                            self.add_human_message((key,value))
                        else:
                            pass
            else:
                raise InvalidSession('No Session Data Found !')
        except FileNotFoundError as e:
            raise InvalidSession('Session not found')
        except json.JSONDecodeError as e:
            raise InvalidSession('Corrupt Session Data')