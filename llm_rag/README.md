# RAG

## Langchain POC


## LLamaindex POC


## Basic app
```shell
pip install uvicorn fastapi python-multipart streamlit PyMuPDF
```

```shell
cd app

# Start FastAPI backend
uvicorn server:app --reload --port 8000

# Start Streamlit frontend
streamlit run app.py --server.port 8501
```
