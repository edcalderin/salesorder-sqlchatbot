import streamlit as st

st.title("SQL Chatbot")

# User input
user_query = st.text_area(
    "Enter your SQL-related query:", "List Top 10 Employees by Salary?"
)

if st.button("Submit"):
    try:
        # Processing user input
        st.write("Response:")
        st.json("Example response")
    except Exception as e:
        st.error(f"An error occurred: {e}")
