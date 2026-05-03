import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="GenAI App", layout="wide")
st.title("🚀 GenAI Playground")

# ---------------- SESSION STATE ----------------
if "file_id" not in st.session_state:
    st.session_state.file_id = None

# ---------------- MENU ----------------
option = st.selectbox(
    "Choose Application",
    ["Blog Generator", "Support Assistant", "Cover Letter Generator", "Chat with CSV", "Sentiment Analyzer using Multiagent"]
)

# =========================================================
# 📝 BLOG GENERATOR
# =========================================================
if option == "Blog Generator":
    st.header("📝 Blog Generator")

    user_input = st.text_input("Enter Blog Topic")

    if st.button("Generate Blog"):
        if user_input:
            with st.spinner("Generating..."):
                res = requests.post(
                    f"{API_URL}/generate",
                    json={"text": user_input, "task_type": "blog"},
                    timeout=60
                )
                result = res.json()

            if result["status"] == "success":
                st.subheader("📝 Blog Content")
                st.write(result["output"])
            else:
                st.error(result["message"])
        else:
            st.warning("Enter a topic")


# =========================================================
# 💬 SUPPORT ASSISTANT
# =========================================================
elif option == "Support Assistant":
    st.header("💬 Support Assistant")

    user_input = st.text_area("Enter Customer Review")

    if st.button("Analyze & Respond"):
        if user_input:
            with st.spinner("Analyzing..."):
                res = requests.post(
                    f"{API_URL}/generate",
                    json={"text": user_input, "task_type": "support"},
                    timeout=60
                )
                result = res.json()

            if result["status"] == "success":
                st.subheader("💬 Response")
                st.write(result["output"])
            else:
                st.error(result["message"])
        else:
            st.warning("Enter a review")


# =========================================================
# 📊 COVER LETTER GENERATOR
# =========================================================

elif option == "Cover Letter Generator":
    st.header("💼 Cover Letter Generator")
    
    job_title = st.text_input("Enter Job Title")
    job_description = st.text_area("Enter Job Description", height=100)

    if st.button("Generate Cover Letter"):
        if job_title and job_description:
            with st.spinner("Generating..."):
                res = requests.post(
                    f"{API_URL}/generateCoverLetter",
                    json={
                        "job_title": job_title,
                        "job_description": job_description
                    },
                    timeout=90
                )
                result = res.json()

            if result["status"] == "success":
                st.subheader("📌 Resume Bullet Points")
                st.write(result["resume_bullets"])

                st.subheader("📄 Cover Letter")
                st.write(result["cover_letter"])
            else:
                st.error(result["message"])
        else:
            st.warning("Please enter both fields")

# =========================================================
# 📊 Sentiment Analyzer using Multiagent
# =========================================================

# =========================================================
# 📊 CSV CHATBOT
# =========================================================
elif option == "Chat with CSV":
    st.header("📊 CSV Chatbot")

    # -------- Upload --------
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file and st.session_state.file_id is None:
        with st.spinner("Uploading file..."):
            res = requests.post(
                f"{API_URL}/upload",
                files={"file": uploaded_file}
            )
            result = res.json()

        if result["status"] == "success":
            st.session_state.file_id = result["file_id"]
            
            st.success("✅ File uploaded successfully")

        else:
            st.error(result["message"])

    if "preview" not in st.session_state:
        st.session_state.preview = None
    if "describe" not in st.session_state:
        st.session_state.describe = None
    # -------- PreView --------
    if st.session_state.file_id:
        if st.button("📄 Show Preview"):
            with st.spinner("Fetching preview..."):
                res = requests.get(
                    f"{API_URL}/preview",
                    params={"file_id": st.session_state.file_id}
                )
                result = res.json()

            if result.get("status") == "success":
                st.session_state.preview = result["preview"]
                st.session_state.describe = result["describe"]
            else:
                st.error(result.get("message"))

    if st.session_state.preview:
        st.subheader("📄 Data Preview")
        st.dataframe(pd.DataFrame(st.session_state.preview))
    if st.session_state.describe:
        st.subheader("📊 Data Summary")
        st.dataframe(pd.DataFrame(st.session_state.describe))


    # -------- QnA --------
    if st.session_state.file_id:
        st.subheader("💬 Ask Questions")

        query = st.text_input("Ask about your data")

        if st.button("Run Query"):
            if query:
                with st.spinner("Processing..."):
                    res = requests.post(
                        f"{API_URL}/csv/query",
                        json={
                            "file_id": st.session_state.file_id,
                            "query": query
                        },
                        timeout=60
                    )
                    result = res.json()

                if result["status"] == "success":
                    st.success(result["answer"])

                    if result.get("error"):
                        st.error(result["error"])
                else:
                    st.error(result["message"])
            else:
                st.warning("Enter a query")

    # -------- Reset --------
    if st.button("🔄 Reset Session"):
        st.session_state.file_id = None
        st.experimental_rerun()