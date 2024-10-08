class IterableAPIException(Exception):
    """Base exception for Iterable API errors."""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response


class RateLimitException(IterableAPIException):
    """Exception raised when rate limit is exceeded."""


class ValidationException(IterableAPIException):
    """Exception raised when input validation fails."""


class AuthenticationException(IterableAPIException):
    """Exception raised when authentication fails."""
