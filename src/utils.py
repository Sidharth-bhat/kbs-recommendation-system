"""
Utility functions for the Knowledge Base Recommendation System.
"""

from typing import Any, Dict


def format_response(success: bool, data: Any = None, message: str = "") -> Dict[str, Any]:
    """
    Format a standard API response.
    
    Args:
        success: Whether the operation was successful
        data: Response data
        message: Optional message
        
    Returns:
        Formatted response dictionary
    """
    response = {"success": success}
    
    if data is not None:
        response["data"] = data
    
    if message:
        response["message"] = message
    
    return response
