class Chat():
    "Chat Class to handel Chat History and more"
    def __init__(self,system_prompt:str):
        self.chat_hist=[('system',system_prompt)]
        self.human_message=None
        self.ai_message=None
    def add_human_message(self,human_message:str):
        self.chat_hist.append(('human',human_message))
        self.human_message=human_message
    def add_ai_message(self,ai_message:str):
        self.chat_hist.append(('ai',ai_message))
        self.ai_message=ai_message
    def get_chat_history(self):
        return self.chat_hist