from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from src.api.commons.dependency_container import DependencyContainer
from src.api.workflow import faqs_router

DependencyContainer.initilize()

app = FastAPI(
    title='Chatbot FAQs Becat'
)


# # CHECK HEALTHY
# @app.get('/')

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# add routers 
app.include_router(faqs_router.router)
