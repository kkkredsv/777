"""
Custom exception classes for the application.

This module defines custom exceptions for different domains of the application:
- PaymentException: For payment-related errors
- UserException: For user management and authentication errors
- DatabaseException: For database operation errors
"""


class PaymentException(Exception):
    """
    Custom exception for payment-related errors.
    
    This exception is raised when issues occur during payment processing,
    validation, or transaction handling.
    """
    def __init__(self, message: str, error_code: str = "PAYMENT_ERROR"):
        """
        Initialize PaymentException.
        
        Args:
            message: Description of the payment error
            error_code: Optional error code for categorization
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class UserException(Exception):
    """
    Custom exception for user management and authentication errors.
    
    This exception is raised when issues occur with user authentication,
    authorization, registration, or user data management.
    """
    def __init__(self, message: str, error_code: str = "USER_ERROR"):
        """
        Initialize UserException.
        
        Args:
            message: Description of the user error
            error_code: Optional error code for categorization
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DatabaseException(Exception):
    """
    Custom exception for database operation errors.
    
    This exception is raised when errors occur during database operations
    such as connection failures, query execution, or data integrity issues.
    """
    def __init__(self, message: str, error_code: str = "DATABASE_ERROR"):
        """
        Initialize DatabaseException.
        
        Args:
            message: Description of the database error
            error_code: Optional error code for categorization
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


def handle_exception(exception: Exception, log_func=None) -> dict:
    """
    Handle exceptions uniformly across the application.
    
    This function processes exceptions and returns a standardized error response.
    It can optionally log the exception using a provided logging function.
    
    Args:
        exception: The exception to handle
        log_func: Optional logging function (e.g., logger.error)
        
    Returns:
        A dictionary containing error information with keys:
        - success: Boolean indicating operation failure
        - error_code: The error code if available
        - message: The error message
        - exception_type: The type of exception
        
    Example:
        >>> try:
        ...     # Some operation
        ...     raise PaymentException("Insufficient funds", "PAYMENT_INSUFFICIENT_FUNDS")
        ... except PaymentException as e:
        ...     error_response = handle_exception(e, logger.error)
        ...     print(error_response)
        {'success': False, 'error_code': 'PAYMENT_INSUFFICIENT_FUNDS', 
         'message': 'Insufficient funds', 'exception_type': 'PaymentException'}
    """
    # Extract error code if available
    error_code = getattr(exception, 'error_code', 'UNKNOWN_ERROR')
    
    # Create standardized error response
    error_response = {
        'success': False,
        'error_code': error_code,
        'message': str(exception),
        'exception_type': type(exception).__name__
    }
    
    # Log the exception if a logging function is provided
    if log_func:
        log_func(f"Exception occurred: {type(exception).__name__} - {str(exception)} (Code: {error_code})")
    
    return error_response
