# 🚀 GenAI Playground

A multi-functional Generative AI application built using **LangGraph StateGraphs**, **FastAPI**, and **Streamlit**, powered by **Gemini models**. This project showcases multiple real-world GenAI use cases including blog generation, document Q&A, analytics, and automation tools.
This project is a lightweight prototype (POC) that demonstrates key ideas from production systems and enhancing them by focusing on multi-agent orchestration, intelligent routing and LLM-based response generation.

---

## 📌 Features

### 📝 Blog Generator

* Input: Blog topic
* Output: Fully generated blog content
* Flow:

  * User provides topic
  * LangGraph workflow generates structured blog

---

### 📊 Chat with CSV

* Upload a CSV file
* Performs:

  * Automatic statistical analysis
  * Question-answering using generated Python queries
* Flow:

  * CSV → Analysis → LangGraph generates Python code → Executes → Returns answer

---

### 📄 Chat with PDF (RAG)

* Upload a PDF document
* Uses **Retrieval-Augmented Generation (RAG)**
* Flow:

  * PDF → Chunking → Embeddings (HuggingFace)
  * Stored in **FAISS vector DB**
  * Query → Cosine similarity search → Context retrieval → Answer generation

---

### 💼 Cover Letter Generator

* Input:

  * Job Title
  * Job Description
* Output:

  * Resume bullet points
  * Tailored cover letter
* Built using LangGraph multi-step workflow

---
### 🤖 Multi-Agent Customer Support System

An intelligent **multi-agent AI system** that classifies user queries, analyzes sentiment, and generates appropriate responses using a structured **LangGraph workflow**.

Built with:

* **LangGraph** for multi-agent orchestration
* **LangChain + LLM (Gemini / OpenAI)** for reasoning
* **Streamlit** for interactive UI

### 🚀 Features

* 🧠 **Query Classification** → Technical, Billing, General
* 😊 **Sentiment Analysis** → Positive, Neutral, Negative
* ⚙️ **Multi-Agent Routing System**

  * Technical Support Agent
  * Billing Support Agent
  * General Support Agent
* 🚨 **Automatic Escalation**

  * Negative sentiment → routed to human support
* 💬 Generates **context-aware responses**

### 🧠 System Architecture

This project uses a **multi-agent workflow graph**:

```id="graphflow1"
START
  ↓
Categorize Agent
  ↓
Sentiment Agent
  ↓
        ┌───────────────┬───────────────┬───────────────┐
        ↓               ↓               ↓               ↓
Technical Agent   Billing Agent   General Agent   Escalation Agent
        ↓               ↓               ↓               ↓
                      END
```
---
### 🎧 Support Assistant

* Input: Customer complaint (text)
* Output: Professional response
* Use case: Customer support automation

---

## 🧠 Tech Stack

* **LLM**: Gemini (Google Generative AI)
* **Orchestration**: LangGraph (StateGraphs)
* **Backend**: FastAPI
* **Frontend**: Streamlit
* **Embeddings**: HuggingFace
* **Vector DB**: FAISS
* **Language**: Python

---
### 🏗️ Production Experience & Deployment

While this repository demonstrates a simplified prototype of a multi-agent customer support system, similar architectures have been implemented in real-world client projects with full production-grade practices.

In production environments, these systems included:

* 🐳 **Containerization** using Docker for consistent and scalable deployments
* ⚙️ **CI/CD pipelines** built with GitHub Actions for automated build, test, and deployment workflows
* 🌐 **Cloud deployment** on platforms such as AWS and GCP for high availability and scalability
* 🏗️ **Infrastructure as Code (IaC)** using Terraform for provisioning and managing cloud resources
* 🔐 **Secure secret management** using AWS Secrets Manager.
* 📊 **Monitoring & logging** for observability, debugging, and performance tracking using AWS Putty

This project serves as a **lightweight, modular representation** of those production systems, focusing on core logic such as multi-agent orchestration, routing, and LLM-driven response generation.
---

## 📂 Project Structure

```
GenAI_playground/
│
├── blog_creator.py           # Blog generation workflow
├── chat_csv.py               # CSV analysis + Q&A
├── pdfchat.py               # RAG pipeline for PDFs
├── cover_letter_builder.py  # Cover letter generator
├── support_assistant.py     # Support response generator
│
├── api.py                   # FastAPI backend
├── app_ui.py                # Streamlit UI
├── app.py                   # Entry point (if applicable)
│
├── src/                     # Additional modules/utilities
│
├── .env                     # Environment variables
├── requirements.txt         # Dependencies
└── README.md                # Project documentation
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone <repo-url>
cd GenAI_playground
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Set Environment Variables

Create a `.env` file:

```
GOOGLE_API_KEY=your_api_key_here
```

---

## 🚀 Running the Application

### ▶️ Start FastAPI Backend

```bash
uvicorn api:app --reload
```

### ▶️ Run Streamlit UI

```bash
streamlit run app_ui.py
```

---

## 🧩 Architecture Overview

* Each feature is built using **LangGraph StateGraph workflows**
* Modular design for easy scaling
* Backend handles orchestration via FastAPI
* Streamlit provides interactive UI

---

## ⚡ Future Enhancements

* Add streaming responses
* Multi-model fallback (OpenAI, Anthropic)
* Authentication & user sessions
* Export outputs (PDF/Docx)
* Deployment on cloud (AWS/GCP/Azure)

---

## 👨‍💻 Author

Developed by **SAGNIK GHOSH** as a **GenAI multi-use case playground** demonstrating real-world applications using modern LLM orchestration frameworks.

---

## 📜 License

This project is for educational and demonstration purposes.
