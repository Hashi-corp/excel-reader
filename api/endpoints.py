from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import (
    FileUploadResponse,
    UserPromptResponse,
    PlotResponse
)
from services.file_service import save_and_parse_file

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile =  File(...)):
    try:
        file_location, df = save_and_parse_file(file)
        # Optionally, you can store df in a cache or session for later use
        return FileUploadResponse(file_name=file.filename, message="File uploaded and parsed successfully")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/plot", response_model=UserPromptResponse)
async def user_prompt(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    # Process the the prompt via LLM and generate appropriate plots
    return UserPromptResponse(prompt=prompt)