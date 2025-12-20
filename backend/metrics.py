from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
import time
from typing import Callable, Awaitable
from fastapi import Request, Response

# Define metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total number of requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Duration of HTTP requests in seconds',
    ['method', 'endpoint']
)

# Add a custom metrics endpoint
async def metrics_endpoint():
    return Response(generate_latest(REGISTRY), media_type="text/plain")

def add_metrics_middleware(app):
    """
    Add metrics collection middleware to the FastAPI application
    """
    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next: Callable[[Request], Awaitable[Response]]):
        start_time = time.time()

        response = await call_next(request)

        # Record metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code
        ).inc()

        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(time.time() - start_time)

        return response