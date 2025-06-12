import os

from dotenv import load_dotenv
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_openai import ChatOpenAI

load_dotenv()


class SQLAgent:
    def __init__(self) -> None:
        self.__llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

        self.__host = os.getenv("MYSQL_HOST")
        self.__user = os.getenv("MYSQL_USER")
        self.__password = os.getenv("MYSQL_PASSWORD")
        self.__database = os.getenv("MYSQL_DATABASE")

    def __explain_result(self) -> RunnableSequence:
        system_message = SystemMessage(
            """You are a data analyst AI. Given a SQL result and the user's
            question, respond with a clear, human-readable explanation of the data."""
        )
        ai_message = AIMessagePromptTemplate.from_template("{results}")
        human_message = HumanMessagePromptTemplate.from_template("{question}")
        prompt = ChatPromptTemplate.from_messages(
            [system_message, ai_message, human_message]
        )
        return prompt | self.__llm | StrOutputParser()

    def create_agent_executor(self, question: str) -> dict[str, str]:
        db_uri: str = f"mysql+mysqlconnector://{self.__user}:{self.__password}@{self.__host}/{self.__database}"
        db: SQLDatabase = SQLDatabase.from_uri(db_uri)

        query_chain = create_sql_query_chain(self.__llm, db=db)
        execute_query = QuerySQLDatabaseTool(db=db)

        results = (query_chain | execute_query).invoke({"question": question})

        explain_chain = (
            RunnableLambda(lambda _: {"question": question, "results": results})
            | self.__explain_result()
        )
        explanation: str = explain_chain.invoke({})

        return {"explanation": explanation, "results": results}
