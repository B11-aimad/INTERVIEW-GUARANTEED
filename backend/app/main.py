from fastapi import FastAPI

app = FastAPI(title="Entretien Garanti API")

@app.get("/health")
def health():
    return {"status": "ok"}