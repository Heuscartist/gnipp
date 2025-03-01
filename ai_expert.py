from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools import WikipediaQueryRun

# Modules for structuring text
from typing import Annotated
from typing_extensions import TypedDict
# LangGraph modules for defining graphs
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

import os
from dotenv import load_dotenv
import google.generativeai as genai



# Load API keys
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)


class State(TypedDict):
    messages: Annotated[list, add_messages]

def build_agentic_graph():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
    graph_builder = StateGraph(State)
    api_wrapper = WikipediaAPIWrapper(top_k_results=1)

    wikipedia_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
    tools = [wikipedia_tool]

    llm_with_tools = llm.bind_tools(tools)

    def chatbot(state: State):
        return {"messages":[llm_with_tools.invoke(state["messages"])]}

    graph_builder.add_node("chatbot",chatbot)
    tool_node = ToolNode(tools=[wikipedia_tool]) 
    graph_builder.add_node("tools", tool_node)
    graph_builder.add_conditional_edges("chatbot", tools_condition)

    graph_builder.add_edge("tools","chatbot") 
    graph_builder.add_edge(START,"chatbot") 
    graph_builder.add_edge("chatbot", END)
    graph = graph_builder.compile()

    return graph

def stream_tool_responses(graph, user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]}):
        for value in event.values():
            response_messages = value["messages"]
            if isinstance(response_messages, list) and len(response_messages) > 0:
                response_text = response_messages[-1].content 
    return response_text

def generate_ai_recommendation_gemini(school_name, has_connectivity, connectivity_summary, tower_summary):
    """Uses LangChain and Gemini AI to generate network infrastructure recommendations."""
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

    prompt_template = ChatPromptTemplate.from_template(
        """
        You are an expert in network infrastructure.

        Analyze and suggest improvements for the following school:

        School Name: {school_name}

        Connectivity:
        - Has Connectivity: {has_connectivity}
        - Connectivity Summary: {connectivity_summary}
        - Tower Summary: {tower_summary}
        """
    )

    chain = (
        {"school_name": RunnablePassthrough(), "has_connectivity": RunnablePassthrough(), "connectivity_summary": RunnablePassthrough(), "tower_summary": RunnablePassthrough()}
        | prompt_template
        | llm
    )

    try:
        response = chain.invoke(
            {
                "school_name": school_name,
                "has_connectivity": has_connectivity,
                "connectivity_summary": connectivity_summary,
                "tower_summary": tower_summary,
            }
        )
        return response.content  # Extract recommendation from LangChain's response
    except Exception as e:
        return f"Error generating recommendation: {e}"
    


# Initialize LLM and vectorstore
def initialize_rag():
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
    vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embedding_function)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 1})
    
    prompt_template = ChatPromptTemplate.from_template(
        """You are an AI assistant helping with information retrieval.
        
        Use the following retrieved context to answer the question accurately.

        Context:
        {context}

        Question:
        {question}

        Answer:
        """
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",  # Stuffing retrieved docs into a single prompt
        return_source_documents=True  # Useful for debugging or citations
    )
    return qa_chain

# Function to query RAG model
def ask_rag_llm(query):
    qa_chain = initialize_rag()
    result = qa_chain.invoke(query)
    return result["result"]