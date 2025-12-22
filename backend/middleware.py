from fastapi import FastAPI

# Mock limiter object to handle decorators without functionality
class MockLimiter:
    def limit(self, rate):
        # Return a decorator that does nothing (passes through the function)
        def decorator(func):
            return func
        return decorator

limiter = MockLimiter()

def add_rate_limiting(app: FastAPI):
    """
    Add rate limiting to the FastAPI application
    """
    # Rate limiting functionality has been removed
    pass