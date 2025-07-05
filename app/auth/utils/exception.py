from fastapi import HTTPException

class ExceptionHandler:

    def unauthorized(message="Unauthorized"):
        raise HTTPException(status_code=401, detail=message)

    def not_found(message="Not Found"):
        raise HTTPException(status_code=404, detail=message)
    
    def bad_request(message="Bad Request"):
        return HTTPException(status_code=400, detail=message)