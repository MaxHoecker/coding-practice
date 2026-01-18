from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://coding-practice.com",
        "http://localhost",
        "http://localhost:8000",
        'http://localhost:3000',
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)