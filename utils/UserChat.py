class UserChat:
    def __init__(self):
        # Initialize properties
        self.user_question = None
        self.sql = None
        self.plot_code = None
        self.sql_result = None
        

class UserChatList:
    def __init__(self):
        # Initialize properties
        self.chat_history = []
        
    def AddHistory(self,chat):
        self.chat_history.append(chat)
        
        
    
