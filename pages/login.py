import json
import pandas as pd
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import dill,io
from llm.query import generate_response  
from utils.setting import display_setting 
from utils.table import display_paper_table 
from utils.db import get_conversations, get_messages, update_conversation, delete_topic, insert_topic, sort_by_date 
import matplotlib.figure
# Initialize session state variables
if 'selected_template' not in st.session_state:
    st.session_state['selected_template'] = None
if 'template_content' not in st.session_state:
    st.session_state['template_content'] = None
if 'template_content_str' not in st.session_state:
    st.session_state['template_content_str'] = ""
if 'chat_history' not in st.session_state:
    st.session_state["chat_history"] = []
if "pending_response" not in st.session_state:
    st.session_state["pending_response"] = None
if "settings" not in st.session_state:
    st.session_state["settings"] = [0.8,10]
if "model" not in st.session_state:
    st.session_state["model"] = "gemini-flash"

def accept(id, data):
    update_conversation(id, "user", data["query"])
    update_conversation(id, "assistant", data["response"])
    st.session_state["pending_response"] = None
    print("User accecpt. Saved to MongoDB. ##############################")

def reject(data):
    st.session_state["pending_response"] = None
    print("User reject response. Discarded reponse: ##############################\n", data)

def display_query_response(query, response):
    with st.chat_message('user'):
        st.markdown(query)
    with st.chat_message('assistant'):
        if isinstance(response, pd.DataFrame):
            if 'DOI' in response.columns:
                display_paper_table(response)  
            else:
                st.write(response) 
        elif isinstance(response,matplotlib.figure.Figure):
            st.write(response)
        else:
            st.markdown(response)

# Set UI of the page
st.title("Bio Research Q&A Chatbot")
st.write("“Bio Database Library” ― Amili")
st.logo('utils/AMILI-Logo-chopped.png', link="https://www.amili.asia/")
st.html('<style>[alt=Logo] { height: 3rem; }</style>')
button_style = "<style>.stButton > button {width: 100%;}</style>"
st.markdown(button_style, unsafe_allow_html=True)

# Check if a template is selected; if not, prompt the user to select one
if not st.session_state['selected_template'] or not st.session_state['template_content_str']:
    st.warning("No template selected. Please go back to the template selection page.")
    if st.button("Go to Template Selection"):
        switch_page("main")
else:
    st.markdown("**Selected Template Content ―** " + st.session_state['template_content_str'])

    with st.sidebar:
        display_setting() 
        st.sidebar.title("Topics")

        # Creation of new topic
        new_topic = st.text_input("Create new topic")
        if st.button('Create'):  
            message = "Hello, what would you like to find out regarding " + new_topic
            if len(new_topic) < 1:
                st.warning("Please input valid topic name")
            else:
                insert_topic("assistant", new_topic, message)
                st.rerun()

        # Retrieve conversation history and allow topic selection
        conversations = get_conversations()

        # Sort the list using sorted and the custom function
        sorted_conversations = sorted(conversations, key=sort_by_date, reverse=True)

        conversation_labels = [(conv['_id'], conv['topic']) for conv in sorted_conversations]
        selected_conversation_id, selected_conversation_label = st.sidebar.selectbox(
            "Select existing topic", conversation_labels, format_func=lambda x: x[1]
        )
        conversation_history = get_messages(selected_conversation_id)
        st.session_state["chat_history"] = conversation_history  

        # Delete current topic
        if st.button('Delete Topic'):
            topic = selected_conversation_label
            if topic:
                message = delete_topic(topic)
                st.write(message)
            st.rerun()

    # Display chat history messages
    for message in st.session_state['chat_history']: 
        with st.chat_message(message['role']):
            content = message['message_content']
            # Display graph if data type is bytes
            if message['role'] == 'assistant'and type(content)==bytes:
                try:
                    figure = dill.loads(content)
                    st.write(figure)
                except:
                    st.markdown(content)
            # Display paper table if DOI is present in content
            elif message['role'] == 'assistant':
                # If it is a dataframe format
                try:
                    df = pd.json_normalize(json.loads(content))
                    # DOI is unique to Research Papers, we can use this to format research papers separately
                    if 'DOI' in content:
                        display_paper_table(df)
                    else:
                        st.write(df)
                except ValueError as e:
                    st.markdown(content)
            else:
                st.markdown(content) 

# Chatbot interface
    if not st.session_state["pending_response"]:
        if user_query := st.chat_input("Ask any question related to patient profiles or research papers"):
            purpose, response = generate_response(user_query)
            display_query_response(user_query, response)
            st.session_state["pending_response"] = {"query": user_query, "response": response}
    
            st.write("Approve or reject the assistant's response before asking another question")
            col1, col2 = st.columns(2)
            col1.button('Accept', on_click=accept, kwargs={"id": selected_conversation_id, "data": st.session_state["pending_response"]})
            col2.button('Reject', on_click=reject, kwargs={"data": st.session_state["pending_response"]})
    
    else:
        history = st.session_state["pending_response"]
        display_query_response(history["query"], history["response"])

        st.warning("No feedback given. Please respond to the assistant's message.")
        st.write("Approve or reject the assistant's response before asking another question")
        col1, col2 = st.columns(2)
        col1.button('Accept', on_click=accept, kwargs={"id": selected_conversation_id, "data": st.session_state["pending_response"]})
        col2.button('Reject', on_click=reject, kwargs={"data": st.session_state["pending_response"]})