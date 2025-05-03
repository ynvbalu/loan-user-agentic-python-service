from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config.settings import setup_logging
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app with enhanced documentation
app = FastAPI(
    title="Loan User Agentic Service",
    description="""
    A FastAPI-based service that uses LangChain and OpenAI to provide natural language processing capabilities 
    for loan transfer operations and user information queries.
    
    ## Features
    
    - Natural language processing for loan transfers
    - User count information
    - RESTful API endpoints
    - OpenAI GPT-3.5 integration
    
    ## Authentication
    
    This API requires an OpenAI API key to be set in the environment variables.
    
    ## Rate Limiting
    
    Please be mindful of API usage as it involves OpenAI API calls.
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    openapi_tags=[
        {
            "name": "process",
            "description": "Process natural language requests for loan transfers and user information"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["process"])

@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: A simple status message
    """
    return {"status": "healthy", "message": "Service is running"}

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Loan User Agentic Service...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 