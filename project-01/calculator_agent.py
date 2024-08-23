import os
import sys
import logging
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Type
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents import AgentExecutor

logging.basicConfig(level=logging.ERROR)


class NumbersInput(BaseModel):
    a: float = Field(..., description="First number")
    b: float = Field(..., description="Second number")

class SumTool(BaseTool):
    name: str = "SumTool"
    description: str = "Sum two numbers"
    args_schema: Type[BaseModel] = NumbersInput

    def _run(
        self,
        a: float,
        b: float
    ) -> float:
        return a + b
    
class SubtractionTool(BaseTool):
    name: str = "SubtractionTool"
    description: str = "Subtract two numbers"
    args_schema: Type[BaseModel] = NumbersInput

    def _run(
        self,
        a: float,
        b: float
    ) -> float:
        return a - b
    
class MultiplicationTool(BaseTool):
    name: str = "MultiplicationTool"
    description: str = "Multiply two numbers"
    args_schema: Type[BaseModel] = NumbersInput

    def _run(
        self,
        a: float,
        b: float
    ) -> float:
        return a * b
    
class DivisionTool(BaseTool):
    name: str = "DivisionTool"
    description: str = "Divide two numbers"
    args_schema: Type[BaseModel] = NumbersInput

    def _run(
        self,
        a: float,
        b: float
    ) -> float:
        return a / b

tools = [
    SumTool(),
    SubtractionTool(),
    MultiplicationTool(),
    DivisionTool()
]

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a powerful calculator. You can sum, subtract, multiply and divide numbers.
            """
        ),
        (
            "user",
            "{input}"
        ),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

if len(sys.argv) < 2:
    logging.error("Please provide a prompt using the --prompt flag")
    sys.exit(1)

openai_key = os.environ.get("OPENAI_API_KEY")

if not openai_key:
    logging.error("Please provide an OpenAI API key using the OPENAI_API_KEY environment variable")
    sys.exit(1)

chat_open_ai = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0,
    openai_api_key=openai_key
)

chat_with_tools = chat_open_ai.bind_tools(tools)

agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(x["intermediate_steps"]),
    }
    | prompt
    | chat_with_tools
    | OpenAIToolsAgentOutputParser()
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

user_prompt = sys.argv[sys.argv.index("--prompt") + 1]

result = list(
    agent_executor.stream(
        {
            "input": user_prompt,
        }
    )
)

print(result[-1]["messages"][0].content)

#How to export Environment Variables in ubuntu
#export OPEN
