from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime
import os
import json
from Exceptions.exceptions import SessionSaveError,InvalidSession
class Chat():
    "Chat Class to handel Chat History and more"
    def __init__(self,system_prompt:str=None):
        self.chat_hist=[]
        self.writable_chat_hist=[]
        if system_prompt:
            self.chat_hist=[('system',system_prompt)]
            self.writable_chat_hist=[{'system':system_prompt}]
        self.human_message=None
        self.ai_message=None
        self.session_id=None
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
            if self.session_id:
                with open(f'{os.getcwd()}'+'\\sessions\\'+self.session_id+'.json','w+', encoding='utf-8') as fp:
                    json.dump(self.writable_chat_hist,fp,ensure_ascii=False)

            else:
                with open(f'{os.getcwd()}'+'\\sessions\\'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.json','w+',encoding='utf-8') as fp:
                    json.dump(self.writable_chat_hist,fp,ensure_ascii=False)
        except Exception as e:
            print(str(e))
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
                            self.chat_hist.append(('system',value))
                            self.writable_chat_hist({'system':value})
                        elif key=='ai':
                            self.add_ai_message(value)
                        elif key=='human':
                            self.add_human_message(value)
                        else:
                            pass
                self.session_id=session_id
            else:
                raise InvalidSession('No Session Data Found !')
        except FileNotFoundError as e:
            raise InvalidSession('Session not found')
        except json.JSONDecodeError as e:
            raise InvalidSession('Corrupt Session Data')