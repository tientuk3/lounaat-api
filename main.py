from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from parse import *

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
    "https://api.tuk3diagnostics.com",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/lounaat")
async def root():
    return get_restaurants()
