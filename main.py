
# import streamlit as st
# from bson import ObjectId
# from pymongo import MongoClient
# from streamlit_extras.switch_page_button import switch_page

# # Initialize session state variables if they don't already exist
# if 'selected_template' not in st.session_state:
#     st.session_state.selected_template = None
# if 'template_content' not in st.session_state:
#     st.session_state.template_content = None
# if 'template_content_str' not in st.session_state:
#     st.session_state.template_content_str = ""

# # MongoDB connection setup
# @st.cache_resource()
# def mongodb_template_connection():
#     """
#     Establishes a connection to the MongoDB chat database.
#     Uses the database and collection names from Streamlit secrets.
#     Returns the collection for templates.
#     """
#     client = MongoClient(st.secrets["MONGODB_CHAT"]) 
#     db = client[st.secrets["MONGO_DB"]]
#     collection = db["templates"]
#     return collection

# def get_templates():
#     templates = collection.find()
#     return list(templates)

# def set_template(template_name, template_content):
#     st.session_state.selected_template = template_name
#     st.session_state.template_content = template_content
#     st.session_state.template_content_str = ', '.join([f"{key}: {value}" for key, value in template_content.items()])
#     st.success(f"{template_name} selected")
#     switch_page("chatbot")

# def remove_template(template_id):
#     collection.delete_one({"_id": ObjectId(template_id)})
#     st.success("Template removed successfully!")
#     st.experimental_rerun()

# def add_custom_template(template_name, content):
#     template = {
#         "type": "customised",
#         "name": template_name,
#         "content": content
#     }
#     collection.insert_one(template)
#     st.success(f"Custom template '{template_name}' added successfully!")
#     st.experimental_rerun()

# # Start of the template selection interface
# st.title("Select a Template")
# st.write("Please choose a template from the options below or")

# create_custom_template_expander = st.expander("Create your customised template")

# st.logo('utils/AMILI-Logo-chopped.png', link="https://www.amili.asia/")
# st.html('<style>[alt=Logo] { height: 3rem; }</style>')

# collection = mongodb_template_connection()
# templates = list(collection.find())

# # Display templates with selection and removal options
# col1, col2 = st.columns(2)
# for idx, template in enumerate(templates):
#     col = col1 if idx % 2 == 0 else col2
#     with col:
#         with st.form(f'template{idx}'):
#             st.markdown(f"### {template['name']}")
#             for key, value in template['content'].items():
#                 st.markdown(f"**{key}**: {value}")
#             button_col1, button_col2 = st.columns(2)
#             with button_col1:
#                 if st.form_submit_button('Select'):
#                     set_template(template['name'], template['content'])
#             if template['type'] == 'customised':
#                 with button_col2:
#                     if st.form_submit_button('Remove'):
#                         remove_template(template['_id'])

# # Form for creating custom templates inside the expander
# with create_custom_template_expander:
#     st.markdown("## Create a Custom Template")

#     with st.form("custom_template_form"):
#         template_name = st.text_input("Template Name", "")
        
#         st.markdown("### Demographic Information")
#         age = st.text_input("Age", "")
#         gender = st.text_input("Gender", "")
#         race = st.text_input("Race", "")
#         bmi = st.text_input("BMI", "")
        
#         st.markdown("### Clinical Information")
#         disease = st.text_input("Disease", "")
#         supplement = st.text_input("Supplement", "")
        
#         if st.form_submit_button("Add Custom Template"):
#             content = {}
#             if age:
#                 content["Age"] = age
#             if gender:
#                 content["Gender"] = gender
#             if race:
#                 content["Race"] = race
#             if bmi:
#                 content["BMI"] = bmi
#             if disease:
#                 content["Disease"] = disease
#             if supplement:
#                 content["Supplement"] = supplement
            
#             if template_name and content:
#                 add_custom_template(template_name, content)
#             else:
#                 st.error("Template Name and at least one field must be filled in to create a custom template.")

# # Display selected template and its content (for debugging purposes)
# if st.session_state.selected_template:
#     st.write(f"**Selected Template**: {st.session_state.selected_template}")
#     st.write("**Template Content**:")
#     for key, value in st.session_state.template_content.items():
#         st.write(f"- **{key}**: {value}")
#     st.write(f"**Template Content String**: {st.session_state.template_content_str}")
# else:
#     st.write("No template selected yet.")

# ############################################# 
# # Navigation Handling: The set_template function sets the template and triggers navigation to the chatbot page.
# # Chatbot Page: The chatbot.py file checks for the selected template and displays chat messages, handling input for new messages.
# # If users navigate directly to the chatbot page without selecting a template, they will be prompted to go back and select a template.
# # Global Context Handling: Routing Agent craft Natural Language query that incorporate user query and global context


import streamlit as st

st.title("My Streamlit Mobile App")
st.write("Welcome to the mobile version of my app!")

# Add more components like buttons, inputs, visualizations here

st.markdown("<style>{}</style>".format(open("assets/styles.css").read()), unsafe_allow_html=True)
