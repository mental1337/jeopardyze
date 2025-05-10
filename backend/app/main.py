from fastapi import FastAPI
from app.routers import quiz_boards


app = FastAPI(title="Jeopardyze")
app.include_router(quiz_boards.router)

@app.get("/")
async def root():
    return {"message": "Jeopardyze"}