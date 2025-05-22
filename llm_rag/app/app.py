import uuid
import requests
import streamlit as st

BACKEND_URL = "http://localhost:8000"

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.title("📁 Chat with Your File")

# File Upload
uploaded_file = st.file_uploader("Upload a file", type=["txt", "pdf", "csv", "docx"])

if uploaded_file:
    st.session_state["uploaded"] = True
    response = requests.post(
        f"{BACKEND_URL}/upload",
        files={"file": (uploaded_file.name, uploaded_file)},
        data={"session_id": st.session_state.session_id}
    )
    st.success(response.json()["message"])

# Chat
if st.session_state.get("uploaded", False):
    user_input = st.text_input("Ask a question about the file:")
    if user_input:
        res = requests.post(
            f"{BACKEND_URL}/chat",
            data={"session_id": st.session_state.session_id, "user_input": user_input}
        )
        if res.status_code == 200:
            for turn in res.json()["history"]:
                st.markdown(f"**You**: {turn['user']}")
                st.markdown(f"**Bot**: {turn['bot']}")
        else:
            st.error(res.json()["error"])
