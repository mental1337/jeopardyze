"""
Run with:
uvicorn app.main:app --host 127.0.0.1 --port 3002 --reload
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, games

app = FastAPI(title="Jeopardyze API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(games.router)

@app.get("/")
def root():
    return {"message": "Welcome to Jeopardyze"}

def main():
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=3002)

if __name__ == "__main__":
    main()
