from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from models.schemas import (
    FileUploadResponse,
    UserPromptResponse,
    PlotResponse
)
from services.file_service import save_and_parse_file, load_file_as_dataframe
from services.ai_service import infer_plot_types_from_prompt
from services.data_processor import generate_and_save_plots
import pandas as pd
import os

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
async def user_prompt(prompt: str = Query(...), filename: str = Query(...)):
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if not filename:
        raise HTTPException(status_code=400, detail="Filename must be provided")
    # Use Gemini to infer plot types
    plot_types_str = infer_plot_types_from_prompt(prompt)
    plot_types = [pt.strip() for pt in plot_types_str.replace('\n', ',').split(',') if pt.strip()]
    try:
        df = load_file_as_dataframe(filename)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except ValueError:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    plot_files = generate_and_save_plots(df, plot_types, 'plots')
    return UserPromptResponse(prompt=f"Plots generated: {plot_files}")