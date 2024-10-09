import streamlit as st
from datetime import datetime

# Function to display paper details in a pop-up window
@st.experimental_dialog("Paper Detail", width="small")
def view(df, row):
    column_names = df.columns.tolist()[2:]  # Skip column "_id" and "Rank"

    for column in column_names:
        st.header(column)
        
        if column == "Demographics":
            demographics = df.loc[row, column]
            if demographics != "None":
                st.markdown(f"**Gender:** {demographics[0]}")
                st.markdown(f"**Location:** {demographics[1]}")
            else:
                st.write(demographics)
        elif column == "Disease":
            diseases = df.loc[row, column]
            for disease in diseases:
                st.markdown(f"- {disease}")
        elif column == "Section Details":
            sections = df.loc[row, column]
            for section in sections:
                st.subheader(section[0])
                st.markdown(section[1])
        else:
            st.write(df.loc[row, column])

@st.cache_data
def convert_df(df):
    # Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")

# Display paper in an interactive table
def display_paper_table(df):
    timestamp = datetime.now().time() 
    col1, col2, col3,col4 = st.columns([0.08, 0.70,0.10, 0.12])
    col1.markdown('###### Rank')
    col2.markdown('###### Title')
    col3.markdown('###### Score')
    col4.markdown('###### Detail')
    
    for row in range(len(df)):
        paper_id = df.loc[row, '_id']
        col1, col2, col3,col4 = st.columns([0.08, 0.70,0.10, 0.12])
        col1.write(df.loc[row, 'Rank'])  
        col2.write(df.loc[row, 'Title']) 
        col3.write(df.loc[row, 'Score'])
        col4.button(label="View", key=f"view_{paper_id}_{timestamp}", on_click=view, kwargs={"df": df, "row": row}) 

    st.download_button(
        label="Download paper details",
        data=convert_df(df),
        file_name="paper_detail.csv",
        mime="text/csv",
        key=f"download_{timestamp}"  # Unique key for download button to prevent caching issues
    )
