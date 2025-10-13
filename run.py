# File: backend/run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",  # This now correctly points to the 'app' in 'main.py'
        host="127.0.0.1",
        port=8000,
        reload=True
    )