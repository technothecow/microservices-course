from fastapi import FastAPI
import uvicorn

from src.middleware import configure_middleware
from src.route_loader import load_routes

# Create the FastAPI application
app = FastAPI(
    title="Service Network Gateway",
    description="API Gateway Service",
    version="1.0"
)

configure_middleware(app)
load_routes(app, "src/views")

# Run the application
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50001)