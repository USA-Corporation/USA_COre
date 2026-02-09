from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Absolute Intelligence System"}

@app.get("/health")
def health():
    return {"status": "healthy"}
