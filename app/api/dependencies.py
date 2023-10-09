# dependencies.py
from fastapi import Request

def get_vectorstore(request: Request):
    return request.app.state.vectorstore

def get_chain(request: Request):
    return request.app.state.qa_chain
