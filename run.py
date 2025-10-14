# File: backend/run.py
from flask.cli import load_dotenv
import uvicorn
load_dotenv()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",  # Correct path: looks in 'app' folder for 'main.py'
        host="127.0.0.1",
        port=8000,
        reload=True
    )