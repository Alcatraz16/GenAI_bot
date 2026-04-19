
from langgraph.graph import StateGraph, START, END
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Literal
from dotenv import load_dotenv
from pydantic import BaseModel,Field
import os


class BlogState(TypedDict):
    title: str
    outline: str
    content: str

def create_outline(state: BlogState, model) -> BlogState:
    #fetch title, generate outline, update state.
    title = state['title']
    prompt = f'Generate a detailed outline for a blog on topic - {title}. Generate in 10 short points.Each point shuld be in 10 words.'
    outline = model.invoke(prompt).content

    state['outline']=outline
    return state

def create_blog(state: BlogState, model) -> BlogState:
    #get title and outline, gen blog and return state
    title = state['title']
    outline = state['outline']
    prompt = f'Generate a blog on topic-{title} and the outline for the topic - {outline}. Keep the blog in 1 paragraph and 100 words.'
    blog = model.invoke(prompt).content

    state['content']=blog
    return state

graph = StateGraph(BlogState)

def get_workflow(model):
    graph.add_node("create_outline",lambda state: create_outline( state, model))
    graph.add_node("create_blog", lambda state: create_blog( state, model))

    graph.add_edge(START,"create_outline")
    graph.add_edge("create_outline","create_blog")
    graph.add_edge("create_blog",END)

    workflow=graph.compile()
    return workflow

def generate_blog( title: str, model):
    workflow = get_workflow(model)

    initial_state = {
        "title": title,
        "outline": "",
        "content": ""
    }

    return workflow.invoke(initial_state)