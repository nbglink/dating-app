from fastapi import FastAPI
app = FastAPI(title="Dating API", version="0.0.7")

@app.get("/")
def root():
    return {"ok": True}
