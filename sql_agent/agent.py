import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chains.sql_database.query import create_sql_query_chain
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
    AIMessagePromptTemplate,
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain_core.runnables import RunnableLambda, RunnableSequence
from langchain_openai import ChatOpenAI

load_dotenv()


class SQLAgent:
    def __init__(self) -> None:
        self.__llm = ChatOpenAI(api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

        few_shot_file: Path = Path(__file__).parent / "few_shot_examples.json"
        self.__few_shot_examples: list[dict] = json.loads(Path.read_text(few_shot_file))

        self.__host = os.getenv("MYSQL_HOST")
        self.__user = os.getenv("MYSQL_USER")
        self.__password = os.getenv("MYSQL_PASSWORD")
        self.__database = os.getenv("MYSQL_DATABASE")
        db_uri: str = f"mysql+mysqlconnector://{self.__user}:{self.__password}@{self.__host}/{self.__database}"
        self.__db: SQLDatabase = SQLDatabase.from_uri(db_uri)

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

    def __get_table_info(self) -> dict:
        return self.__db.get_context()

    def __load_prompt(self) -> FewShotChatMessagePromptTemplate:
        human_message = HumanMessagePromptTemplate.from_template("{input}")
        ai_message = AIMessagePromptTemplate.from_template("{query}")
        example_prompt = ChatPromptTemplate.from_messages([human_message, ai_message])

        template: str = (
            "You are a MySQL expert. Given an input question, create a "
            "syntactically correct MySQL query to run. Unless otherwise specified, do "
            "not return more than {top_k} rows.\n\nHere is the relevant table info: "
            "\n\n{table_info}\n\nBelow are a number of examples of questions and "
            "their corresponding SQL queries."
        )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
            examples=self.__few_shot_examples,
            example_prompt=example_prompt,
            input_variables=["input", "top_k", "table_info"],
        )

        system_prompt = SystemMessage(template)
        human_prompt = HumanMessagePromptTemplate.from_template("{input}")

        return ChatPromptTemplate.from_messages(
            [system_prompt, few_shot_prompt, human_prompt]
        )

    def create_agent_executor(self, question: str) -> dict[str, str]:
        table_info: dict = self.__get_table_info()
        prompt = self.__load_prompt()
        query_chain = create_sql_query_chain(self.__llm, db=self.__db, prompt=prompt)
        execute_query = QuerySQLDatabaseTool(db=self.__db)

        results = (query_chain | execute_query).invoke(
            {"question": question, "table_info": table_info}
        )

        explain_chain = (
            RunnableLambda(lambda _: {"question": question, "results": results})
            | self.__explain_result()
        )
        explanation: str = explain_chain.invoke({})

        return {"explanation": explanation, "results": results}
