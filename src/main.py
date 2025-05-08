import logging
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.config.settings import setup_logging
from pydantic import BaseModel
from typing import Dict, Any
from .core.agent import create_agent

# Configure root logger
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('loan_service_debug.log')
    ]
)

# Configure specific loggers
loggers = [
    'src.core.agent',
    'src.core.tools',
    'src.api.routes',
    'uvicorn',
    'fastapi'
]

# Set up loggers
for logger_name in loggers:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    logger.propagate = True

# Filter out httpcore trace logs
logging.getLogger('httpcore').setLevel(logging.WARNING)
logging.getLogger('httpx').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Setup logging
setup_logging()

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
    logger.debug("Health check endpoint called")
    return {"status": "healthy", "message": "Service is running"}

if __name__ == "__main__":
    import uvicorn
    try:
        logger.info("Starting Loan User Agentic Service...")
        uvicorn.run(
            "src.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False,  # Disable reload to prevent hanging
            log_level="debug"  # Changed to debug level
        )
    except Exception as e:
        logger.error(f"Failed to start service: {str(e)}", exc_info=True)
        raise 