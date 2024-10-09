import streamlit as st

def display_setting():
    """
    Display a settings popover in a Streamlit app for configuring model and other parameters.
    """
    settings_popover = st.popover("Settings")  # Create a popover named "Settings" in Streamlit app

    if settings_popover: 
        with settings_popover: 
            # Model selection
            selected_model = st.selectbox(
                "Model", 
                ("gemini-flash", "gemini-pro", "gemini-mixed")
            )
            st.session_state["model"] = selected_model 
            
            # Accuracy slider
            st.session_state["settings"][0] = st.slider(
                "Accuracy", 
                min_value=0.0,  
                max_value=1.0,  
                step=0.01,  
                value=st.session_state.get("settings", [0.8, 10])[0]  # Default accuracy value from session state or 0.8
            )

            # Number of papers to return input
            st.session_state["settings"][1] = st.number_input(
                "Number of papers to return", 
                min_value=1, 
                value=st.session_state.get("settings", [0.8, 10])[1]  # Default number of papers from session state or 10
            )

            # Display current settings
            accuracy = st.session_state["settings"][0]  
            papers = st.session_state["settings"][1]  
            st.write(f"Accuracy: {accuracy:.2f}")  
            st.write(f"Number of papers to return: {int(papers)}") 
