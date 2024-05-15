import pymongo
from datetime import datetime, timedelta
from utils.UserChat import UserChatList,UserChat
import pandas as pd

class MongoDBService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = pymongo.MongoClient("mongodb://rahul:rahul@localhost:27017/")
            cls._instance._db = cls._instance._client["chat_history_db"]
            cls._instance._collection = cls._instance._db["chat_history_collection"]
            cls._instance.create_database_if_not_exists()
            cls._instance.create_collection_if_not_exists()
        return cls._instance

    def create_database_if_not_exists(self):
        if self._db.name not in self._client.list_database_names():
            self._client[self._db.name]

    def create_collection_if_not_exists(self):
        if self._collection.name not in self._db.list_collection_names():
            self._db.create_collection(self._collection.name)
    
    # def store_chat_history(self, chat):
    #     print("===== current chat",chat)
    #     chat.sql_result = chat.sql_result.to_dict(orient='records')
        
    #     json_chat = chat.to_json()
    #     print("======= json chat",json_chat)
    #     chat_with_timestamp = {**json_chat, "timestamp": datetime.now()}
    #     self._collection.insert_one(chat_with_timestamp)
    
    def store_chat_history(self, chat):
        # print("===== current chat",chat)
        chat.sql_result = chat.sql_result.to_dict(orient='records')
        # print("before ======= json chat",chat.sql_result)
        
        for record in chat.sql_result:
            for key, value in record.items():
                # print(f"Key: {key}, Value: {value}, Type: {type(value)}")  # Print type of value
                # print("some coniditon checking: ",str(type(value)) == "<class 'datetime.date'>")
                #if isinstance(value, datetime) or (key.lower().endswith('date') and 'date' in key.lower()):  # Check if key contains 'date'
                if isinstance(value, datetime) or str(type(value)) == "<class 'datetime.date'>": #or (key.lower().endswith('date') and 'date' in key.lower()):  # Check if key contains 'date'
                    # print("==== ", key, record[key])    
                    if value is None:
                        record[key] = None
                    else:
                        record[key] = value.isoformat()
                    
        
        json_chat = chat.to_json()
        # print("after ======= json chat",json_chat)
        chat_with_timestamp = {**json_chat, "timestamp": datetime.now()}
        self._collection.insert_one(chat_with_timestamp)

    def retrieve_chat_history_last_hour(self):
        last_hour = datetime.now() - timedelta(hours=1)
        query = {"timestamp": {"$gte": last_hour}}
        return self._collection.find(query)

    def deserialize_user_chat_list(self, json_data):
        user_chat_list = UserChatList()
        for chat_json in json_data:
            user_chat = UserChat()
            user_chat.user_question = chat_json.get('user_question')
            user_chat.sql = chat_json.get('sql')
            user_chat.plot_code = chat_json.get('plot_code')
            # Deserialize DataFrame if available
            df_json = chat_json.get('sql_result')
            if df_json:
                user_chat.sql_result = pd.DataFrame(df_json)
            user_chat_list.AddHistory(user_chat)
        return user_chat_list

    def close_connection(self):
        self._client.close()

# Example usage:
# Create an instance of MongoDBService

