"""
Run with:
uvicorn app.main:app --host 0.0.0.0 --port 3002
"""

from fastapi import FastAPI

app = FastAPI(title="Jeopardyze API")

@app.get("/")
def root():
    return {"message": "Welcome to Jeopardyze API"}



def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3002)

if __name__ == "__main__":
    main()
