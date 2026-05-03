from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import streamlit as st
from GenAI_playground.blog_creator import generate_blog
from GenAI_playground.support_assistant import handle_review
from GenAI_playground.chat_csv import run_csv_chatbot
from GenAI_playground.sentiment_multiagent import run_customer_service
from GenAI_playground.cover_letter_builder import *
# from GenAI_playground.chat_pdf import create_vectordb, generate_summary, run_qna
import pandas as pd
import tempfile

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
# print("Api_key:",api_key)
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.5
)

st.set_page_config(page_title="AI App", layout="wide")

st.title("🚀 GenAI Playground")

option = st.selectbox(
    "Choose Application",
    ["Blog Generator", "Support Assistant","Chat with CSV","Sentiment Analyzer using Multiagent","Cover Letter Generator"]
)

#######------Blog Generator-----##########
if option == "Blog Generator":
    st.header("📝 Blog Generator")

    title = st.text_input("Enter Blog Topic")

    if st.button("Generate Blog"):
        if title:
            with st.spinner("Generating blog..."):
                result = generate_blog(title, model)

            st.subheader("📌 Outline")
            st.write(result["outline"])

            st.subheader("📝 Blog Content")
            st.write(result["content"])
        else:
            st.warning("Please enter a topic")

#######------Support Assistant-----##########
elif option == "Support Assistant":
    st.header("💬 Automated Support Assistant")

    review = st.text_area("Enter Customer Review")

    if st.button("Analyze & Respond"):
        if review:
            with st.spinner("Analyzing review..."):
                result = handle_review(review, model)

            st.subheader("📊 Sentiment")
            st.write(result["sentiment"])

            if result["sentiment"] == "negative":
                st.subheader("🧠 Diagnosis")
                col1, col2, col3 = st.columns(3)

                col1.metric("Issue Type", result["diagnosis"]["issue_type"])
                col2.metric("Tone", result["diagnosis"]["tone"])
                urgency = result["diagnosis"]["urgency"]
                if urgency == "high":
                    st.error("🔴 High Priority Issue")
                elif urgency == "medium":
                    st.warning("🟡 Medium Priority Issue")
                else:
                    st.success("🟢 Low Priority Issue")

            st.subheader("💬 Response")
            st.write(result["response"])
        else:
            st.warning("Please enter a review")

#######------Chat with CSV-----##########
elif option =="Chat with CSV":
    st.header("📊 CSV Chatbot")
    uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        with st.expander("📄 Preview Data"):
            st.dataframe(df.head())
            st.dataframe(df.describe())

        user_query = st.text_input("💬 Ask a question about your data")

        if st.button("Run Query") and user_query:
            # st.write("WIP")
            with st.spinner("⏳ Processing..."):
                response = run_csv_chatbot(user_query, df, model)
                st.subheader("💬 Answer")
                st.success(response.get("final_answer", "No answer generated"))
                
                if response.get("error"):
                    st.error(f"⚠️ Error: {response['error']}")


#######------Sentiment Analyzer using Multiagent-----##########
elif option =="Sentiment Analyzer using Multiagent":
    st.header("📞 Customer Sentiment Analyzer using Multiagent")
    query = st.text_area("Enter your query:")
    if st.button("Submit"):
        if not query.strip():
            st.warning("Please enter a query.")
        else:
            result = run_customer_service(query, model)
            st.subheader("🔍 Analysis")
            col1, col2 = st.columns(2)

            with col1:
                st.write( result["category"])

            with col2:
                st.write("**Sentiment:**", result["sentiment"])
            
            st.subheader("💬 Response")
            st.write(result["response"])

#######------Cover Letter Generator-----##########
elif option == "Cover Letter Generator":
    st.header("💼 Cover Letter Generator")
    job_title = st.text_input("Enter Job Title")
    job_description = st.text_area("Enter Job Description", height=100)

    if st.button("Generate Cover Letter"):
        if job_title and job_description:
            with st.spinner("Generating..."):
                result = handle_cover_letter(
                job_title= job_title,
                job_description= job_description,
                model=model
            )
             
            if result.get("status") == "success":
                st.subheader("📌 Resume Bullet Points")
                bullets = result.get("resume_bullets", "")
                if bullets:
                    st.markdown(bullets)
                else:
                    st.info("No bullet points generated.")

                st.subheader("📄 Cover Letter")
                cover_letter = result.get("cover_letter", "")
                if cover_letter:
                    st.markdown(cover_letter)
                else:
                    st.info("No cover letter generated.")

        else:
            st.warning("Please enter both fields")


#######------Chat with PDF-----##########
# elif option == "Chat with PDF":
#     st.header("📄 PDF Chatbot (RAG + LangGraph)")
#     uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

#     if uploaded_file:
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#             tmp.write(uploaded_file.read())
#             file_path = tmp.name
#         st.success("✅ PDF uploaded!")

        # if "vectordb" not in st.session_state:
        #     with st.spinner("🔄 Processing PDF..."):
        #         vectordb, chunks = create_vectordb(file_path)
        #         st.session_state.vectordb = vectordb
        #         st.session_state.chunks = chunks

        # if "summary" not in st.session_state:
        #     st.session_state.summary = generate_summary(st.session_state.chunks,model)
        
        # st.subheader("📌 Summary")
        # st.info(st.session_state.summary)

        # query = st.text_input("💬 Ask a question")

        # if st.button("Ask") and query:
        #     with st.spinner("Thinking..."):
        #         response = run_qna(
        #         query,
        #         model,
        #         st.session_state.vectordb
        #     )
        #     st.subheader("📌 Answer")
        #     st.success(response["answer"])