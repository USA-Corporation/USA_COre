from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def root():
    return {"Absolute Intelligence": "Live"}

@app.get("/health")
def health():
    return {"status": "healthy"}
