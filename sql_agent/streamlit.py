import streamlit as st

from sql_agent import SQLAgent

sql_agent = SQLAgent()
executor = sql_agent.create_agent_executor()

st.title("SQL Chatbot")

# User input
user_query = st.text_area(
    "Enter your SQL-related query:", "List Top 10 Employees by Salary?"
)

if st.button("Submit"):
    try:
        # Processing user input
        st.write("Response:")
        response = executor.invoke({"input": user_query})
        st.json(response)
    except Exception as e:
        st.error(f"An error occurred: {e}")
