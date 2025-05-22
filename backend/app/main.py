from fastapi import FastAPI
from app.routers import quiz_boards, game_sessions
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Jeopardyze")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quiz_boards.router)
app.include_router(game_sessions.router)

@app.get("/")
async def root():
    return {"message": "Jeopardyze"}