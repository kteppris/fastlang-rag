from .chat import router as chat_router
from .vectorstore import router as sources_router

router = chat_router
router.include_router(sources_router, prefix="/vectorstore", tags=["Vectorstore"])