import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# API Settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
BASE_API_URL="http://localhost:8080"
LOAN_TRANSFER_API_URL = f"{BASE_API_URL}/api/loans/transfer"

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo-1106"
OPENAI_TEMPERATURE = 0
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Set specific log levels for different modules
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    # Log that environment variables are loaded
    logger = logging.getLogger(__name__)
    logger.info("Environment variables loaded") 