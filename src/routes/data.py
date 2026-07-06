from fastapi import FastAPI,APIRouter,Depends, UploadFile, status
from fastapi.responses import JSONResponse
import os
import aiofiles
from helpers.config import get_settings,Settings
from controllers import DataController,ProjectController,ProcessController
from models import ResponseSignals
import logging
from .schemas.data import ProcessRequest

logger = logging.getLogger("uvicorn.error")

data_router = APIRouter(
    prefix = "/api/v1/data",
    tags = ['api_v1','data']
)

# upload
@data_router.post("/upload/{project_id}")

async def upload_data(project_id: str,file:UploadFile,
                      app_settings : Settings = Depends(get_settings)):
    
    data_controller = DataController()

    #validate the file properties 
    is_valid , result_signal = data_controller.validate_uploaded_file(file=file)
    
    if not is_valid:
        return JSONResponse (
            status_code= status.HTTP_400_BAD_REQUEST.value,
            content={"signal" : result_signal}
                             )
        
    project_file_path = ProjectController().get_project_path(project_id)    
    
    file_path,file_id =data_controller.generate_unique_filepath(
        origin_filename=file.filename,
        project_id=project_id
        )
    
    try:
        async with aiofiles.open(file_path, "wb") as f:
            while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                await f.write(chunk)
    except Exception as e:

        logger.error(f"Error while uploading file: {e}")

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignals.FILE_UPLOAD_FAILED.value
            }
        )
        
    return JSONResponse (
            content={
                "signal" : ResponseSignals.FILE_UPLOADED_SUCCESS.value,
                "file_id" : file_id
                })


@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, Process_request: ProcessRequest):
    file_id = Process_request.file_id
    chunk_size = Process_request.chunk_size
    chunk_overlap = Process_request.overlap_size
   
    process_controller = ProcessController(project_id=project_id)
    file_content = process_controller.get_file_content(file_id=file_id)
    file_chunks = process_controller.process_file_content( file_content=file_content,file_id=file_id, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    
    if file_chunks is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "signal": ResponseSignals.FILE_PROCESSING_FAILED.value
            }
        )
        
    return file_chunks