import os
from typing import Annotated, TypedDict, List
import chromadb
from chromadb.utils import embedding_functions
from langgraph.graph import StateGraph, START, END
from fastapi.staticfiles import StaticFiles
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class AgentState(TypedDict):
    messages: List[str]
    plot_context: str
    revision_needed: bool

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def prose_writer(state: AgentState):
    try:
        response = client.models.generate_content(
            model="gemma-4-26b-a4b-it",
            contents=f"Context: {state['plot_context']}\nTask: {state['messages'][-1]}"
        )
        return {"messages": state["messages"] + [response.text]}
    except Exception as e:
        return {"messages": state["messages"] + [f"Error: {str(e)}"]}

def critic_editor(state: AgentState):
    last_message = state["messages"][-1]
    needs_fix = len(last_message) < 50
    return {"revision_needed": needs_fix}

def should_continue(state: AgentState):
    if state["revision_needed"]:
        return "writer"
    return "end"

workflow = StateGraph(AgentState)

workflow.add_node("writer", prose_writer)
workflow.add_node("editor", critic_editor)

workflow.add_edge(START, "writer")
workflow.add_edge("writer", "editor")

workflow.add_conditional_edges(
    "editor",
    should_continue,
    {
        "writer": "writer",
        "end": END
    }
)

app = workflow.compile()

def ask_chatbot(user_message: str, plot_context: str = ""):
    initial_state = {
        "messages": [user_message],
        "plot_context": plot_context,
        "revision_needed": False
    }
    result = app.invoke(initial_state)
    return result["messages"][-1]