import math
from dotenv import load_dotenv

load_dotenv()

from langchain_core.tools import tool
from langchain_tavily import TavilySearch
from database import save_memory, search_memory
from rag import retrieve_from_rag

CURRENT_THREAD_ID = "default"

def set_current_thread_id(thread_id: str):
    global CURRENT_THREAD_ID
    CURRENT_THREAD_ID = thread_id


web_search = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="advanced"
)


@tool
def calculator(expression: str) -> str:
    """
    Useful for simple math calculations.
    Input should be a valid math expression.
    Example: 2 + 2, math.sqrt(16), 10 * 5
    """
    try:
        allowed = {
            "abs": abs,
            "round": round,
            "min": min,
            "max": max,
            "pow": pow,
            "math": math
        }
        # Evaluate the expression safely
        result = eval(expression, {"__builtins__": {}}, allowed)
        return str(result)
    
    except Exception as e:
        return f"Error evaluating expression: {e}"



@tool
def search_uploaded_documents(query: str) -> str:
    """
    Search uploaded documents for relevant information.
    Use this when the user asks about uploaded PDFs, DOCX, TXT, notes, files, or
    """

    return retrieve_from_rag(
        query=query,
        thread_id=CURRENT_THREAD_ID
    )



@tool
def remember_this(memory: str) -> str:
    """
    Save important information to long-term memory.
    Use when the user wants to remember something for future reference.
    """

    return save_memory(
        thread_id=CURRENT_THREAD_ID, 
        memory=memory
    )


@tool
def recall_memory(query: str) -> str:
    """
    Recall important information from long-term memory.
    Use when the user wants to retrieve previously saved information.
    """

    return search_memory(
        thread_id=CURRENT_THREAD_ID, 
        query=query
    )

tools = [
    calculator,
    search_uploaded_documents,
    remember_this,
    recall_memory,
    web_search
]