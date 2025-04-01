from fastapi import FastAPI

app = FastAPI(title="Jeopardyze")

@app.get("/")
async def root():
    return {"message": "Jeopardyze"}