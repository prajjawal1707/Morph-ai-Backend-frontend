import os
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.file_handler import save_file

router = APIRouter()
UPLOAD_DIR = "uploads_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a CSV/Excel file and load into DataFrame.
    """
    if not file:
        return JSONResponse(
            {"status": "error", "message": "No file received"},
            status_code=400,
        )

    result = await save_file(file)

    if not result["success"]:
        return JSONResponse(
            {"status": "error", "message": "Unsupported or invalid file format"},
            status_code=400,
        )

    return {
        "status": "success",
        "filename": result["filename"],
        "size": result["size"],
        "message": "File uploaded and dataframe loaded ✅"
    }
