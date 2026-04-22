from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pandas as pd
import io
from dotenv import load_dotenv
import uuid
from GenAI_playground.blog_creator import generate_blog
from GenAI_playground.support_assistant import handle_review
from GenAI_playground.chat_csv import run_csv_chatbot
from GenAI_playground.cover_letter_builder import *
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

app = FastAPI()

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)

csv_store = {}
class TextRequest(BaseModel):
    text: str
    task_type: str  # "blog" or "support"

class QueryRequest(BaseModel):
    file_id: str
    query: str

class CoverLetterRequest(BaseModel):
    job_title: str
    job_description: str


@app.post("/generate")
async def generate_text(request: TextRequest):
    try:
        if request.task_type == "blog":
            result = generate_blog(request.text, model)
            output = result.get("content")

        elif request.task_type == "support":
            result = handle_review(request.text, model)
            output = result.get("response")

        else:
            return JSONResponse(
                status_code=400,
                content={"status": "error", "message": "Invalid task_type"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "output": output
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/generateCoverLetter")
async def generate_text(request: CoverLetterRequest):
    try:
        result = handle_cover_letter(
            job_title=request.job_title,
            job_description=request.job_description,
            model=model
        )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "resume_bullets": result.get("resume_bullets"),
                "cover_letter": result.get("cover_letter")
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

        file_id = str(uuid.uuid4())
        csv_store[file_id] = df

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "file_id": file_id
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/preview")
async def preview_csv(file_id: str):
    try:
        df = csv_store.get(file_id)

        if df is None:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "File not found"}
            )

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "preview": df.head().to_dict(),
                "describe": df.describe().to_dict()
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )



@app.post("/csv/query")
async def query_csv(request: QueryRequest):
    try:
        df = csv_store.get(request.file_id)

        if df is None:
            return JSONResponse(
                status_code=404,
                content={"status": "error", "message": "Invalid file_id"}
            )

        result = run_csv_chatbot(request.query, df, model)

        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "answer": result.get("final_answer"),
                "error": result.get("error")
            }
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )