"""
DocWal SDK Exceptions
"""


class DocWalError(Exception):
    """Base exception for all DocWal SDK errors"""

    def __init__(self, message, status_code=None, response=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(DocWalError):
    """Raised when API key authentication fails"""
    pass


class ValidationError(DocWalError):
    """Raised when request validation fails"""
    pass


class RateLimitError(DocWalError):
    """Raised when rate limit is exceeded"""
    pass


class NotFoundError(DocWalError):
    """Raised when resource is not found"""
    pass


class PermissionError(DocWalError):
    """Raised when permission is denied"""
    pass
