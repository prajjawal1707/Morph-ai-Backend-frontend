# run.py - CORRECT VERSION
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # This correctly points to the 'app' variable in the 'app/main.py' file
        host="127.0.0.1",
        port=8000,
        reload=True
    )