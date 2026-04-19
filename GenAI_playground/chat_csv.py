from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict
from dotenv import load_dotenv
import pandas as pd

class CSVState(TypedDict):
    question: str
    schema: str
    code: str
    result: str
    error: str
    final_answer: str

def get_schema(df):
    schema = "Columns:\n"
    for col, dtype in df.dtypes.items():
        schema += f"- {col} ({dtype})\n"
    return schema

def generate_code(state: CSVState, model, df) -> CSVState:
    question = state["question"]
    
    schema = get_schema(df)
    sample = df.head(3).to_string(index=False)

    prompt = f"""
        You are a Python pandas expert.
        Rules:
        - DataFrame name is df
        - Use only pandas
        - Use correct datatypes
        - Return ONLY Python code
        - Store final output in variable named result
        - Do NOT use markdown

        Schema:
        {schema}

        Sample Data:
        {sample}

        User Question:
        {question}

        Python Code:
        """

    code = model.invoke(prompt).content.strip()

    state["schema"] = schema
    state["code"] = code
    return state

def execute_code(state: CSVState, df) -> CSVState:
    code = state["code"]
    try:
        local_vars = {"df": df}
        exec(code, {}, local_vars)

        state["result"] = str(local_vars.get("result"))
        state["error"] = ""

    except Exception as e:
        state["error"] = str(e)

    return state

def fix_code(state: CSVState, model) -> CSVState:
    error = state["error"]
    question = state["question"]
    code = state["code"]

    prompt = f"""
        Fix the following pandas code.

        Error:
        {error}

        Original Question:
        {question}

        Code:
        {code}

        Return only corrected Python code.
        """

    new_code = model.invoke(prompt).content.strip()

    state["code"] = new_code
    state["error"] = ""
    return state

def generate_answer(state: CSVState, model) -> CSVState:
    question = state["question"]
    result = state["result"]

    try:
        if hasattr(result, "to_string"):
            result_str = result.to_string(index=False)
        else:
            result_str = str(result)
    except:
        result_str = str(result)

    prompt = f"""
                You are a helpful data analyst.Convert the result into a clear and concise natural language answer.
                Guidelines:
                - summarize key insights
                - If result is a single value, answer directly
                - Keep answer under 2 sentences
                User Question:
                {question}
                Result:
                {result_str}
                Answer:
        """

    answer = model.invoke(prompt).content.strip()

    state["final_answer"] = answer
    return state

def decide_next(state: CSVState):
    if state.get("error"):
        return "fix_code"
    return "end"

graph = StateGraph(CSVState)
def get_workflow(model, df):
    graph.add_node("generate_code", lambda state: generate_code(state, model, df))
    graph.add_node("execute_code", lambda state: execute_code(state, df))
    graph.add_node("fix_code", lambda state: fix_code(state, model))
    graph.add_node("generate_answer", lambda state: generate_answer(state, model))

    graph.add_edge(START, "generate_code")
    graph.add_edge("generate_code", "execute_code")

    graph.add_conditional_edges(
        "execute_code",
        decide_next,
        {
            "fix_code": "fix_code",
            "end": "generate_answer"
        }
    )

    graph.add_edge("fix_code", "execute_code")
    graph.add_edge("generate_answer",END)

    workflow = graph.compile()
    return workflow

def run_csv_chatbot(question: str, df: pd.DataFrame, model):
    workflow = get_workflow(model, df)

    initial_state = {
        "question": question,
        "schema": "",
        "code": "",
        "result": "",
        "error": "",
        "final_answer": ""  
    }

    return workflow.invoke(initial_state)