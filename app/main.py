from fastapi import FastAPI

app = FastAPI()


@app.get("/", tags=["Health Check"])
def health_check():
    return {"status": "ok", "project": "AI Quote Generator API", "version": "0.1.0"}
