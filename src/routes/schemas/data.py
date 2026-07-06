from pydantic import BaseModel
from typing import Optional
class ProcessRequest(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100  # Default chunk size is 
    overlap_size: Optional[int] = 20  # Default overlap size is 10
    do_reset: Optional[int] = 0  # Default is not to reset
    