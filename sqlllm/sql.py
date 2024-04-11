from dotenv import load_dotenv
import streamlit as st
import os
import sqlite3

import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Genai Key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to Load Google Gemini Model and provide queries as response
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content([prompt[0], question])
    return response.text

# Function to retrieve query from the database
def read_sql_query(sql, db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return rows

# Define Your Prompt
prompt = [
    """
    The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION
    
    For example:
    - How many entries of records are present?
    The SQL command will be something like this: SELECT COUNT(*) FROM STUDENT;
    
    - Tell me all the students studying in Data Science class?
    The SQL command will be something like this: SELECT * FROM STUDENT WHERE CLASS="Data Science";
    
    Note: The SQL code should not have ``` in the beginning or end, and "sql" word in the output.
    """
]

# Streamlit App
st.set_page_config(page_title="SQL Query Bot", layout="wide")

# Header layout
header_col1, header_col2 = st.columns([3, 1])  # Adjust the ratio as needed

# Header content
with header_col1:
    st.header("SQL Query Bot")
with header_col2:
    st.image("bot.jpg", width=300)  # Adjust width as needed

# Input field for user's question
question = st.text_input("Input:", key="input")

# Button to submit the question
submit = st.button("Ask the question")

# if submit is clicked
if submit:
    # Generate response using Gemini model
    response = get_gemini_response(question, prompt)
    
    # Execute SQL query
    query_result = read_sql_query(response, "student.db")
    
    # Display response
    st.subheader("Response:")
    st.code(response)
    
    # Display query result
    st.subheader("Query Result:")
    if query_result:
        for row in query_result:
            st.write(row)
    else:
        st.write("No results found.")

# Add some custom CSS for styling
st.markdown("""
    <style>
        /* Custom CSS styles */
        .stTextInput>div>div>div {
            background-color: #f0f2f6 !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stButton>button {
            background-color: #4CAF50 !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #45a049 !important;
        }
        .stMarkdown>div>div>div {
            background-color: #f0f2f6 !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stMarkdown>div>div>div>div {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stMarkdown>div>div>div>div>div>div>div>div {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
        }
        .stMarkdown>div>div>div>div>div>div>div>div>div>div>div>div {
            background-color: #ffffff !important;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)
