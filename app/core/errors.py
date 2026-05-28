from fastapi import HTTPException


class BusinessRuleError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.status_code = status_code


def business_error_to_http(error: BusinessRuleError) -> HTTPException:
    return HTTPException(status_code=error.status_code, detail=str(error))
