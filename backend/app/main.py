from fastapi import FastAPI
from app.routers import quiz_boards, game_sessions, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Jeopardyze")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173",
                   "https://jeopardyze.xyz",
                   "https://www.jeopardyze.xyz"
                   ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(quiz_boards.router)
app.include_router(game_sessions.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Jeopardyze"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}