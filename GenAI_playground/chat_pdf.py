# from langchain_community.document_loaders import PyPDFLoader
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from langgraph.graph import StateGraph, START, END
# from typing import TypedDict

# def create_vectordb(file_path):
#     # Load PDF
#     loader = PyPDFLoader(file_path)
#     documents = loader.load()

#     # Split
#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=50
#     )
#     chunks = splitter.split_documents(documents)

#     # Embeddings
#     embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

#     vectordb = FAISS.from_documents(chunks, embedding)

#     return vectordb, chunks

# def generate_summary(chunks, model):
#     text = "\n".join([c.page_content for c in chunks[:5]])

#     prompt = f"""
#         Summarize this document in 5 concise sentences:
        
#         {text}

#         Summary:
#         """
#     return model.invoke(prompt).content

# class QnAState(TypedDict):
#     question: str
#     context: str
#     answer: str

# def retrieve_docs(state: QnAState, vectordb):
#     docs = vectordb.similarity_search(state["question"], k=3)

#     context = "\n".join([doc.page_content for doc in docs])
#     state["context"] = context

#     return state

# def generate_answer(state: QnAState, model):
#     prompt = f"""
#     Answer ONLY from context. Answer in 1-2 sentences.

#     Context:
#     {state["context"]}

#     Question:
#     {state["question"]}

#     Answer:
#     """

#     state["answer"] = model.invoke(prompt).content
#     return state

# def get_workflow(model, vectordb):
#     graph = StateGraph(QnAState)

#     graph.add_node("retrieve", lambda s: retrieve_docs(s, vectordb))
#     graph.add_node("answer", lambda s: generate_answer(s, model))

#     graph.add_edge(START, "retrieve")
#     graph.add_edge("retrieve", "answer")
#     graph.add_edge("answer", END)

#     return graph.compile()

# def run_qna(question, model, vectordb):
#     workflow = get_workflow(model, vectordb)

#     return workflow.invoke({
#         "question": question,
#         "context": "",
#         "answer": ""
#     })