from enum import Enum

class ResponseSignals(Enum):
    
    FILE_VALIDATED_SUCCESS="File_validated_successsfully"
    FILE_TYPE_NOT_SUPPORTED="File_type_not_supported"
    FILE_SIZE_EXCEEDED="File_size_exceeded"
    FILE_UPLOADED_SUCCESS="File_upload_success"
    FILE_UPLOADED_FAIL="File_upload_fail"
    