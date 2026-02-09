from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Absolute Intelligence", "status": "live"}

@app.get("/health")
def health():
    return {"status": "healthy"}
