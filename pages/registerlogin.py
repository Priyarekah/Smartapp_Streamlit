import streamlit as st 

# Login Page
def registerlogin_page():
    # Display images (ensure paths are correct)
    st.image("/home/priya/Android/Smartapp_Streamlit/assets/images/page2top.png", use_column_width=True)
    st.image("/home/priya/Android/Smartapp_Streamlit/assets/images/page2center.png", use_column_width=True)
  
    # Navigation to Login or Register
    menu = st.radio("Choose an option", ["Register", "Sign In"])
    
    if menu == "Register":
        st.session_state.page = "register"
    elif menu == "Sign In":
        st.session_state.page = "login"
