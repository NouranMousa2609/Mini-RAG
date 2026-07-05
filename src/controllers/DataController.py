import os

from .BaseController import BaseController
from .ProjectController import ProjectController

from models import ResponseSignals
from fastapi import UploadFile
import random
import string
import re



class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.size_scale = 1048576
    
    def validate_uploaded_file(self,file:UploadFile):
        print(f">>> content_type: '{file.content_type}'")  # add this temporarily
        print(f">>> allowed: {self.app_settings.FILE_ALLOWED_TYPES}")
        content_type = file.content_type.split(";")[0].strip()
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignals.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignals.FILE_SIZE_EXCEEDED.value
        return True, ResponseSignals.FILE_VALIDATED_SUCCESS.value
    
    def generate_unique_filepath(self, origin_filename:str, project_id:str):
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id)
        
        cleaned_filename = self.get_clean_file_name(origin_filename)
        
        new_file_path = os.path.join(project_path, 
                                     random_key + "_" +
                                     cleaned_filename)
        
        while os.path.exists(new_file_path):
            random_key = self.generate_random_string()
            new_file_path = os.path.join(project_path, 
                                     random_key + "_" + cleaned_filename)
        return new_file_path , random_key + "_" + cleaned_filename   
        
        
    def get_clean_file_name(self, origin_filename:str):  
        cleaned_filename = re.sub(r'[^\w.]', '', origin_filename.strip())
        cleaned_filename = cleaned_filename.replace(" ", "_")
        return cleaned_filename