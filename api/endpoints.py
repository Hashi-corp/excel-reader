from fastapi import APIRouter, UploadFile, File, HTTPException
from models.schemas import (
    FileUploadResponse,
    UserPromptResponse,
    PlotResponse
)

router = APIRouter()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(file: UploadFile =  File(...)):
    #input the file from user and validate file type
    return FileUploadResponse(file_name=file.filename, message="File uploaded successfully")

@router.post("/plot", response_model=UserPromptResponse)
async def user_prompt(prompt: str):
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    # Process the the prompt via LLM and generate appropriate plots
    return UserPromptResponse(prompt=prompt)