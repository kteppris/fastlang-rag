# api/endpoints/sources.py
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Body
from langchain.vectorstores.base import VectorStore

from api.dependencies import get_vectorstore

router = APIRouter()

@router.get("/sources/", response_model=List[dict])
async def get_sources(vectorstore: VectorStore = Depends(get_vectorstore)):
    # Fetch the metadata
    metadatas = vectorstore.get(include=["metadatas"])["metadatas"]

    if not metadatas:
        raise HTTPException(status_code=404, detail="No sources found")

    sources_dict = {}

    for data in metadatas:
        # If the source is not in our dictionary, add it
        if data["source"] not in sources_dict:
            sources_dict[data["source"]] = {
                "fetch_time": data["fetch_time"],
                "file_path": data["file_path"],
                "encoder_model": data["encoder_model"],
                "pages": []
            }

        # If page attribute exists, append to our pages list
        if "page" in data:
            sources_dict[data["source"]]["pages"].append(data["page"])

    # Convert the pages list to a count of unique pages for each source
    for source, details in sources_dict.items():
        if details["pages"]:
            details["page_count"] = max(details["pages"])
            details["docs_count"] = len(details["pages"])
            del details["pages"]
        else:
            del details["pages"]

    sources_list = list(sources_dict.values())
    return sources_list

@router.post("/query/")
async def search_documents(query: str = Body(...), vectorstore: VectorStore = Depends(get_vectorstore)):
    try:
        # Search the vectorstore with the provided query
        documents = vectorstore.similarity_search_with_score(
            query=query,
            k=5
        )

        # Extracting page_content and metadata from each Document
        results = [{"page_content": doc.page_content, "metadata": doc.metadata, "score": score} for doc, score in documents]

        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing query: {e}")