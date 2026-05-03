from typing import TypedDict, Dict
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate

class State(TypedDict):
  query: str
  category: str
  sentiment: str
  response:str

def categorize(state: State, llm) -> State:
    query = state["query"]
    prompt = f"""
      "Categroize  the given in any of the one of the following categories:"
      "Technical, Billing, General. Query:{query}"
    """
    response = llm.invoke(prompt).content

    return {"category": response}

def sentiment(state: State, llm) -> State:
    query = state["query"]
    prompt = f"""
      "Analyze the sentiment of the customer based on the given query:"
      "Response in either 'Position', 'Neutral' and 'Negative'. Query:{query}"
    """
    response =  llm.invoke(prompt).content

    return {"sentiment": response}

def handle_technical(state: State, llm) -> State:
    query = state["query"]
    prompt = f"""
      "Provide a technical support response to the customer based on the given query:"
      "Query:{query}"
    """
    response = llm.invoke(prompt).content

    return {"response": response}

def handle_billing(state: State, llm) -> State:
    query = state["query"]
    prompt = f"""
      "Provide a billing support response to the customer based on the given query:"
      "Query:{query}"
    """
    response = llm.invoke(prompt).content

    return {"response": response}

def handle_general(state: State, llm) -> State:
    query = state["query"]
    prompt = f"""
      "Provide a general support response to the customer based on the given query:"
      "Query:{query}"
    """
    response = llm.invoke(prompt).content

    return {"response": response}

def escalate(state: State) -> State:
  return {"response":"This issue is moved to a human user who will handle and resolve the issue."}

def router_query(state: State) -> State:
  if state["sentiment"] == "Negative":
    return "escalate"
  elif state["category"] == "Technical":
    return "handle_technical"
  elif state["category"] == "Billing":
    return "handle_billing"
  else:
    return "handle_general"
  
workflow = StateGraph(State)

def get_workflow(llm):

    workflow.add_node("categorize",lambda state: categorize(state, llm))
    workflow.add_node("sentiment",lambda state:sentiment(state, llm))
    workflow.add_node("handle_technical",lambda state:handle_technical(state, llm))
    workflow.add_node("handle_billing",lambda state:handle_billing(state, llm))
    workflow.add_node("handle_general",lambda state:handle_general(state, llm))
    workflow.add_node("escalate",lambda state:escalate(state))

    workflow.add_edge("categorize","sentiment")
    workflow.add_conditional_edges(
        "sentiment",
        router_query,{
                        "handle_technical": "handle_technical",
                        "handle_billing": "handle_billing",
                        "handle_general": "handle_general",
                        "escalate": "escalate"
                    })

    workflow.add_edge("handle_technical",END)
    workflow.add_edge("handle_billing",END)
    workflow.add_edge("handle_general",END)
    workflow.add_edge("escalate",END)

    workflow.set_entry_point("categorize")
    app= workflow.compile()
    return app

def run_customer_service(query: str, model) -> Dict[str, str]:
  workflow = get_workflow(model)
  result = workflow.invoke({"query": query})
  return{
      "category": result["category"],
      "sentiment": result["sentiment"],
      "response": result["response"]
  }
  