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

def set_question(question):
    st.session_state["my_question"] = question
    if question not in get_last_asked_questions():
        set_questions_list(question)
    
def get_last_asked_questions():
    if("last_asked_my_questions" in st.session_state):
        return st.session_state["last_asked_my_questions"]
    else:
        return ""
    
def set_questions_list(question):
    if("last_asked_my_questions" not in st.session_state):
        st.session_state.last_asked_my_questions = [question]
        
    else:
        st.session_state["last_asked_my_questions"].append(question)
    



st.set_page_config(layout="wide")
setup_connexion()

st.sidebar.title("Output Settings")
st.sidebar.checkbox("Show SQL", value=True, key="show_sql")
st.sidebar.checkbox("Show Table", value=True, key="show_table")
# st.sidebar.button("Rerun", on_click=setup_session_state, use_container_width=True)

st.title("CRC AI SQL SERVICE")
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
        st.session_state.chat_history.AddHistory(current_chat)
    # get_last_asked_questions
    st.session_state["my_question"]= None
    
    

def CreatingChatHistory(chat_session_object):
    chat_history = chat_session_object.chat_history
    
    if not chat_history:  # If chat_history is empty, return
        return
    
    for chat in chat_history:
        if chat.user_question:
            st.markdown(f"<b>User:</b> {chat.user_question}", unsafe_allow_html=True)
        
        if chat.sql:
            st.markdown("```sql\n{}\n```".format(chat.sql))
        
        if chat.sql_result is not None:
            df = chat.sql_result
            if len(df) > 10:
                st.markdown("**First 10 rows of data:**")
                st.dataframe(df.head(10))
            else:
                st.markdown("**Data:**")
                st.dataframe(df)
        
        if chat.plot_code:
            fig = generate_plot_cached(code=chat.plot_code, df=df)
            if fig is not None:
                st.markdown("**Chart:**")
                st.plotly_chart(fig)
            else:
                st.error("I couldn't generate a chart")

def main():
    
    my_question = st.session_state.get("my_question", default=None)
    
    if my_question is None:
        my_question = st.chat_input(
            "Ask me a question about your data",
        )
    
    CreatingChatHistory(st.session_state.chat_history)
    ChatWithVanna(my_question)
    
    st.sidebar.title("Previously Asked Questions")
    for i in get_last_asked_questions():
        st.sidebar.write("- " + i)

if __name__=='__main__':
    main()    