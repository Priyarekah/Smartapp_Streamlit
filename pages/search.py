import streamlit as st
from services.transport_service import get_travel_options

# def search_page():
#     st.title("Find your route")
#     start = st.text_input("Starting Location")
#     destination = st.text_input("Destination")
    
#     travel_mode = st.selectbox("Mode of Transportation", ["Driving", "Public Transport", "Walking"])
#     if st.button("Search"):
#         results = get_travel_options(start, destination, travel_mode)
#         st.write("Here are your travel options:")
#         st.json(results)


# Search Page
def search_page():
    st.title("Search Locations")
    start_location = st.text_input("Starting Location")
    destination_location = st.text_input("Destination Location")

    if st.button("Search"):
        if start_location and destination_location:
            # Logic for querying transportation options would go here
            st.success("Searching for options...")
            st.session_state.page = 'travel_comparison'  # Redirect to comparison page
        else:
            st.error("Please enter both locations.")

    if st.button("Back to Landing"):
        st.session_state.page = 'landing'