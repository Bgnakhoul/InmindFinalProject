from collections.abc import AsyncIterable
from datetime import date, datetime, timedelta
from typing import Any, List, Literal

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter


memory = MemorySaver()

load_dotenv() 


################################################################################

# Code from: https://medium.com/@saurabhp.iitkgp/simple-rag-q-a-with-your-pdf-file-using-langgraph-824a831032f0

folder_path = Path(r"C:\Users\bachi\Downloads\InmindFinalProject\resumes")   
# 1) Load all PDFs in the folder
loader = DirectoryLoader(str(folder_path), glob="*.pdf", loader_cls=PyPDFLoader)
docs = loader.load()

# 2) Split into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=300)
chunks = splitter.split_documents(docs)

# 3) Embed + store
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

db = FAISS.from_documents(chunks, embeddings)

# ###########################################################################


@tool()
def best_candidates_from_resumes(requirements: str) -> Dict[str, Any]:
    """
    Find the most qualified candidates for the job description provided.
    Returns: {"Candidates_ID_numbers": [list of candidate IDs]}
    """
    # # 4) Retrieve best matches
    results = db.similarity_search_with_score(query = requirements, k=5)
    if not results:
        return {"error": "No candidates matched."}
    sources = [doc.metadata.get("source", "") for doc, _ in results]

    return {
        "Candidates_ID_numbers": [sources],
    }


class ResponseFormat(BaseModel):
    """Respond to the user in this format."""

    status: Literal["input_required", "completed", "error"] = "input_required"
    message: str


class search_agent_RAG:
    """search_agent_RAG - is a specialized assistant for resumes evaluation."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    SYSTEM_INSTRUCTION = ("You are search_RAG_agent a specialized candidate matching agent. "
        "Your sole purpose is to use the 'best_candidates_from_resumes' tool to find matching candidates based on the parsed job description."
        "Make sure to pass the correct parameter to the tool. 'requirements' should be a string containing the parsed job description."
        "The 'best_candidates_from_resumes' tool will return a list of candidate IDs that match the job description provided."
        "You will return the results in a structured format with status and message (eg. The candidates matching the job description are: [list of candidate IDs]).")

    def __init__(self):
        self.model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")  
        self.tools = [best_candidates_from_resumes] 

        self.graph = create_react_agent(
            self.model,
            tools=self.tools,
            checkpointer=memory,
            prompt=self.SYSTEM_INSTRUCTION,
            response_format=ResponseFormat,
        )

    def invoke(self, query, context_id):
        config: RunnableConfig = {"configurable": {"thread_id": context_id}}
        # today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}." {today_str}\n\n
        augmented_query = f"User query: {query}"
        self.graph.invoke({"messages": [("user", augmented_query)]}, config)
        return self.get_agent_response(config)

    async def stream(self, query, context_id) -> AsyncIterable[dict[str, Any]]:
        # today_str = f"Today's date is {date.today().strftime('%Y-%m-%d')}." {today_str}\n\n
        augmented_query = f"User query: {query}"
        inputs = {"messages": [("user", augmented_query)]}
        config: RunnableConfig = {"configurable": {"thread_id": context_id},"recursion_limit": 3}

        for item in self.graph.stream(inputs, config, stream_mode="values"):
            message = item["messages"][-1]
            if (
                isinstance(message, AIMessage)
                and message.tool_calls
                and len(message.tool_calls) > 0
            ):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Searching for matching candidates...",
                }
            elif isinstance(message, ToolMessage):
                yield {
                    "is_task_complete": False,
                    "require_user_input": False,
                    "content": "Finding matching candidates...",
                }
                

        yield self.get_agent_response(config)

    def get_agent_response(self, config):
        current_state = self.graph.get_state(config)
        structured_response = current_state.values.get("structured_response")
        if structured_response and isinstance(structured_response, ResponseFormat):
            if structured_response.status == "input_required":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "error":
                return {
                    "is_task_complete": False,
                    "require_user_input": True,
                    "content": structured_response.message,
                }
            if structured_response.status == "completed":
                return {
                    "is_task_complete": True,
                    "require_user_input": False,
                    "content": structured_response.message,
                }

        return {
            "is_task_complete": False,
            "require_user_input": True,
            "content": (
                "We are unable to process your request at the moment. "
                "Please try again."
            ),
        }
