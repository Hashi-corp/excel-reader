from pydantic import BaseModel
from typing import Optional

class FileUploadResponse(BaseModel):
    file_name: str
    message: str
    preview: str  # DataFrame head as string

class UserPromptResponse(BaseModel):
    prompt: str

class PlotResponse(BaseModel):
    plot_url: Optional[str] = None
    message: Optional[str] = None