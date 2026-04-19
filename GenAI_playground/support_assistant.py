from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

class ReviewState(TypedDict):
    review : str
    sentiment : Literal["positive","negative"]
    diagnosis : dict
    response : str

class SentimentSchema(BaseModel):
    sentiment: Literal["positive","negative"] = Field(description="Sentiment of the review")

class Diagnosis(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"]
    tone: Literal["angry", "frustrated", "disappointed", "calm"]
    urgency: Literal["low", "medium", "high"]

def find_sentiment(state: ReviewState, model):
    structured_model = model.with_structured_output(SentimentSchema)

    prompt = f"For the following review find out the sentiment:\n{state['review']}"
    sentiment = structured_model.invoke(prompt).sentiment

    return {"sentiment": sentiment}

def check_sentiment(state: ReviewState) -> Literal["positive_response", "run_diagnosis"]:
    if state["sentiment"] == "positive":
        return "positive_response"
    else:
        return "run_diagnosis"
    
def positive_response(state: ReviewState, model):
    prompt = f"""
    Write a warm Thank you message in response of the review:

    '{state["review"]}'

    Also ask the user to give feedback on our website.
    """
    response = model.invoke(prompt).content
    return {"response": response}

def run_diagnosis(state: ReviewState, model):
    structured_model2 = model.with_structured_output(Diagnosis)

    prompt = f"""
    Diagnose the negative review:

    '{state["review"]}'

    Return issue_type, tone and urgency.
    """

    diagnosis = structured_model2.invoke(prompt)
    return {"diagnosis": diagnosis.model_dump()}

def negative_response(state: ReviewState, model):
    diagnosis = state["diagnosis"]

    prompt = f"""
    You are a support assistant.

    The user had a '{diagnosis['issue_type']}' issue,
    sounded '{diagnosis['tone']}' and marked urgency '{diagnosis['urgency']}'.

    Write an empathetic, helpful response.
    """

    response = model.invoke(prompt).content
    return {"response": response}

def get_workflow(model):
    graph = StateGraph(ReviewState)

    graph.add_node("find_sentiment", lambda s: find_sentiment(s, model))
    graph.add_node("positive_response", lambda s: positive_response(s, model))
    graph.add_node("run_diagnosis", lambda s: run_diagnosis(s, model))
    graph.add_node("negative_response", lambda s: negative_response(s, model))

    graph.add_edge(START, "find_sentiment")
    graph.add_conditional_edges("find_sentiment", check_sentiment)

    graph.add_edge("positive_response", END)
    graph.add_edge("run_diagnosis", "negative_response")
    graph.add_edge("negative_response", END)

    return graph.compile()

def handle_review(review: str, model):
    workflow = get_workflow(model)

    initial_state = {
        "review": review,
        "sentiment": "",
        "diagnosis": {},
        "response": ""
    }

    return workflow.invoke(initial_state)