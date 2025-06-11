import os

from dotenv import load_dotenv
from langchain.agents.agent import AgentExecutor
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI

load_dotenv()


class SQLAgent:
    def __init__(self) -> None:
        self.__llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

        self.__host = os.getenv("MYSQL_HOST")
        self.__user = os.getenv("MYSQL_USER")
        self.__password = os.getenv("MYSQL_PASSWORD")
        self.__database = os.getenv("MYSQL_DATABASE")

    def create_agent_executor(self) -> AgentExecutor:
        db_uri: str = f"mysql+mysqlconnector://{self.__user}:{self.__password}@{self.__host}/{self.__database}"
        db = SQLDatabase.from_uri(db_uri)
        return create_sql_agent(
            self.__llm, db=db, agent_type="openai-tools", verbose=True
        )
