import time
import streamlit as st
from code_editor import code_editor
from utils.setup import setup_connexion, setup_session_state
from utils.vanna_calls import (
    generate_questions_cached,
    generate_sql_cached,
    run_sql_cached,
    generate_plotly_code_cached,
    generate_plot_cached,
)
from utils.UserChat import UserChat,UserChatList
from utils.mongoUtils import MongoDBService

#---------------- Mongo connection

mongo_service = MongoDBService()

#---------------- Mongo connection

def set_question(question):
    st.session_state["my_question"] = question
    if question not in get_last_asked_questions():
        set_questions_list(question)
    
def get_last_asked_questions():
    if("last_asked_my_questions" in st.session_state):
        return st.session_state["last_asked_my_questions"]
    else:
        return ""
    
def get_all_asked_questions():
    if("user_question" in st.session_state):
        return st.session_state["user_question"]
    else:
        return ""
    
    
def set_questions_list(question):
    if("last_asked_my_questions" not in st.session_state):
        st.session_state.last_asked_my_questions = [question]
        
    else:
        st.session_state["last_asked_my_questions"].append(question)
    

st.set_page_config(layout="wide")
setup_connexion()

# Set up layout for the logo to be in the top-left corner of the sidebar
st.markdown(
    """
    <style>
        .sidebar .logo-container {
            position: absolute;
            top: 10px;
            left: 10px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Display the logo image in the sidebar
st.sidebar.image("https://thewitslab.com/_next/static/media/header-logo.29455862.png?imwidth=828", width=100)

st.sidebar.title("Output Settings")
st.sidebar.checkbox("Show SQL", value=True, key="show_sql")
st.sidebar.checkbox("Show Table", value=True, key="show_table")
st.sidebar.checkbox("Show Chart", value=True, key="show_plot")
# st.sidebar.button("Rerun", on_click=setup_session_state, use_container_width=True)

st.title("WIL AI SQL SERVER")
# st.sidebar.write(st.session_state)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history= UserChatList()




assistant_message_suggested = st.chat_message(
    "assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png"
)
if assistant_message_suggested.button("Click to show suggested questions"):
    st.session_state["my_question"] = None
    questions = generate_questions_cached()
    for i, question in enumerate(questions):
        time.sleep(0.05)
        button = st.button(
            question,
            on_click=set_question,
            args=(question,),
        )


def ChatWithVanna(my_question):
    
    if my_question:
        current_chat = UserChat()
        st.session_state["my_question"] = my_question
        set_question(my_question)
        user_message = st.chat_message("user")
        
        if st.session_state.get("my_question") is not None:
            current_chat.user_question= my_question
        
        user_message.write(f"{my_question}")
        sql = generate_sql_cached(question=my_question)
        
        current_chat.sql = sql
        
        if sql:
            if st.session_state.get("show_sql", True):
                assistant_message_sql = st.chat_message(
                    "assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png"
                )
                assistant_message_sql.code(sql, language="sql", line_numbers=True)

            df = run_sql_cached(sql=sql)
            st.session_state["df"] = df
            
            current_chat.sql_result= df
            
            if st.session_state.get("df") is not None:
                if st.session_state.get("show_table", True):
                    df = st.session_state.get("df")
                    assistant_message_table = st.chat_message(
                        "assistant",
                        avatar="https://ask.vanna.ai/static/img/vanna_circle.png",
                    )
                    if len(df) > 10:
                        assistant_message_table.text("First 10 rows of data")
                        assistant_message_table.dataframe(df.head(10))
                    else:
                        assistant_message_table.dataframe(df)

                code = generate_plotly_code_cached(question=my_question, sql=sql, df=df)
                current_chat.plot_code=code

                if code is not None and code != "":
                    if st.session_state.get("show_chart", True):
                        assistant_message_chart = st.chat_message(
                            "assistant",
                            avatar="https://ask.vanna.ai/static/img/vanna_circle.png",
                        )
                        fig = generate_plot_cached(code=code, df=df)
                        if fig is not None:
                            assistant_message_chart.plotly_chart(fig)
                        else:
                            assistant_message_chart.error("I couldn't generate a chart")

        else:
            assistant_message_error = st.chat_message(
                "assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png"
            )
            assistant_message_error.error("I wasn't able to generate SQL for that question")
        
        mongo_service.store_chat_history(current_chat)
        st.session_state.chat_history.AddHistory(current_chat)
    # get_last_asked_questions
    st.session_state["my_question"]= None
    
    

def CreatingChatHistory(chat_session_object):
    # Retrieve chat history from the last hour
    chat_history_last_hour = mongo_service.retrieve_chat_history_last_hour()
    # for chat in chat_history_last_hour:
    #     print(chat)
    chat_history = mongo_service.deserialize_user_chat_list(chat_history_last_hour)
    st.session_state.chat_history = chat_history
    print(st.session_state.chat_history)
    
    st.sidebar.title("Previously Asked Questions")
    for i in st.session_state.chat_history.chat_history:
        st.sidebar.write("- " + i.user_question)
    # chat_history = chat_session_object.chat_history
    # chat_history = UserChatList()
    
    if not chat_history:  # If chat_history is empty, return
        return
    
    for chat in chat_history.chat_history:
        if chat.user_question:
            user_message = st.chat_message("user")
            user_message.write(chat.user_question)
        
        if chat.sql and st.session_state.get("show_sql", True):
            assistant_message_sql = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
            assistant_message_sql.code(chat.sql, language="sql", line_numbers=True)
        
        if chat.sql_result is not None:
            df = chat.sql_result
            if(st.session_state.get("show_table", True)):
                if len(df) > 10:
                    assistant_message_table = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                    assistant_message_table.text("First 10 rows of data")
                    assistant_message_table.dataframe(df.head(10))
                else:
                    assistant_message_table = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                    assistant_message_table.dataframe(df)
        
        if chat.plot_code and st.session_state.get("show_plot", True):
            fig = generate_plot_cached(code=chat.plot_code, df=df)
            if fig is not None:
                assistant_message_chart = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                assistant_message_chart.plotly_chart(fig)
            else:
                assistant_message_error = st.chat_message("assistant", avatar="https://ask.vanna.ai/static/img/vanna_circle.png")
                assistant_message_error.error("I couldn't generate a chart")

def main():
    
    my_question = st.session_state.get("my_question", default=None)
    
    if my_question is None:
        my_question = st.chat_input(
            "Ask me a question about your data",
        )
    
    CreatingChatHistory(st.session_state.chat_history)
    ChatWithVanna(my_question)
    
    
    for i in get_last_asked_questions():
        st.sidebar.write("- " + i)
        
    # Close MongoDB connection when done
    # mongo_service.close_connection()

if __name__=='__main__':
    main()    