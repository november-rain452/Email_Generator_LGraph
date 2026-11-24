from typing import Annotated, Literal
from typing_extensions import TypedDict
import operator
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langgraph.types import interrupt, Command
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.checkpoint.sqlite import SqliteSaver

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")


class State(TypedDict):
    draft: str
    recipient: str
    sender: str
    feedback: str
    approved: bool
    accepted: Literal["Accepted", "Rejected", "NA"]
    logs: Annotated[list[str], operator.add]


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert email writer. Write concise, direct, and well-structured emails.\n"
            "Rules:\n"
            "- Output ONLY the email (Subject line, greeting, body, sign-off).\n"
            "- Do not include conversational filler or explanations.\n"
            "- Match a professional, clear tone.",
        ),
        (
            "human",
            "Recipient: {recipient}\n"
            "Topic / Key Details: {details}\n"
            "Previous Draft (if revising): {draft}\n"
            "Feedback to apply (if any): {feedback}",
        ),
    ]
)

chain = prompt | llm | StrOutputParser()
