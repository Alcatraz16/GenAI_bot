from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from pydantic import BaseModel, Field

class CoverLetterState(TypedDict):
    job_title: str
    job_description: str
    resume_bullets: str
    cover_letter: str

def create_bullets(state: CoverLetterState, model) -> CoverLetterState:

    job_title = state['job_title']
    job_description = state['job_description']
    prompt = f"""
        Your task is to generate strong, concise, and achievement-oriented resume bullet points based on the provided job title and job description.

        Guidelines:
        1. Use action verbs (e.g., Developed, Led, Optimized, Implemented).
        2. Keep each bullet point concise (1 line max).
        3. Maintain professional tone and clarity.

        Input:
        - Job Title: {job_title}
        - Job Description: {job_description}

        Output:
        - Generate 5 resume bullet points tailored to the role.
        """
    resume_bullets = model.invoke(prompt).content

    return {'resume_bullets':resume_bullets}
    
def create_cover_letter(state: CoverLetterState, model) -> CoverLetterState:
    #get title and outline, gen blog and return state
    job_title = state['job_title']
    job_description = state['job_description']
    resume_bullets = state['resume_bullets']
    prompt = f"""
    Your task is to generate a tailored cover letter using the provided job title, job description and resume bullet points.

    Guidelines:
    1. Write in a professional, confident, and engaging tone.
    2. Align skills and experience closely with the job description requirements.
    3. Avoid copying bullet points verbatim—paraphrase and connect them into a narrative.
    4. Keep the letter concise (100 words max).
    Input:
    - Job Title: {job_title}
    - Job Description: {job_description}
    - Resume Bullet Points: {resume_bullets}

    Output:
    - A well-structured cover letter clearly in 2 paragraphs.
    """
    cover_letter = model.invoke(prompt).content

    return {'cover_letter': cover_letter}

def get_workflow(model):
    graph = StateGraph(CoverLetterState)

    graph.add_node("create_bullets",lambda s: create_bullets(s,model))
    graph.add_node("create_cover_letter",lambda s: create_cover_letter(s,model))

    graph.add_edge(START,"create_bullets")
    graph.add_edge("create_bullets","create_cover_letter")
    graph.add_edge("create_cover_letter",END)

    return graph.compile()

def handle_cover_letter(job_title: str, job_description: str, model):
    workflow = get_workflow(model)
    initial_state = {
        "job_title": job_title,
        "job_description": job_description,
        "resume_bullets": "",
        "cover_letter": ""
    }

    result = workflow.invoke(initial_state)

    return {
            "status": "success",
            "resume_bullets": result.get("resume_bullets", ""),
            "cover_letter": result.get("cover_letter", "")
        }