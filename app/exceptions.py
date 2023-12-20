from typing import Optional

from fastapi import FastAPI, HTTPException

app = FastAPI()

ERROR_RESPONSE_CODES = {
    # Auth Exceptions
    "InvalidServerAuthorizationException": "000-001",
    "InvalidClientAuthorizationException": "000-002",
    "ServerAuthorizationMissingException": "000-003",
    # Assets Exceptions
    "AssetsRecordsQueryException": "001-001",
    "AssetsRecordInsertException": "001-001",
}


class AuthenticationException(HTTPException):
    """Generic authentication base exception, 403 status code"""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 403
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class InvalidServerAuthorizationException(AuthenticationException):
    """000-001 Server authentication exception, 403 status code."""


class InvalidClientAuthorizationException(AuthenticationException):
    """000-002 Client authentication exception, 403 status code."""


class UnauthorizedException(HTTPException):
    """Generic Unauthorized base exception. Signifies that although we know who the requester is
    we do not believe they have the authority to perform the requested action. 401 status code"""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 401
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class UnauthorizedException(HTTPException):
    """Generic Unauthorized base exception. 401 status code to signify that although we know who the requester is
    we do not believe they have the authority to perform the requested action."""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 401
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class DatabaseUpdateException(HTTPException):
    """Generic base exception for if any database update cannot be performed. 500 internal error"""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 500
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class DataNotFoundException(HTTPException):
    """Generic invalid Data not found exception. 404 status code, requested resource not found"""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 404
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class DatabaseQueryException(HTTPException):
    """Generic base exception for if any database query cannot be performed. This does not mean the resource cannot
    be found - this would be a 404 error. 500 internal error"""

    def __init__(self, desc: Optional[str] = ""):
        self.code = 500
        name = self.__class__.__name__
        assert name in ERROR_RESPONSE_CODES
        self.detail = {
            "Code": ERROR_RESPONSE_CODES[name],
            "CodeName": name,
            "Description": name if desc == "" else desc,
        }
        super().__init__(status_code=self.code, detail=self.detail)


class AssetsRecordsQueryException(DatabaseQueryException):
    """001-001 A postgres query to find assets records matching the criteria failed. 500 status code"""
