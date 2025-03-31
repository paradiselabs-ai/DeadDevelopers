"""
Middleware package for the DeadDevelopers application.

This package contains custom middleware for the FastHTML application.
"""

from .session import CustomSessionMiddleware

__all__ = ['CustomSessionMiddleware']