from pydantic import BaseModel
from typing import Optional

class FileUploadResponse(BaseModel):
    file_name: str
    message: str

class UserPromptResponse(BaseModel):
    prompt: str

class PlotResponse(BaseModel):
    plot_url: Optional[str] = None
    message: Optional[str] = None