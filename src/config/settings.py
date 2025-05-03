import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.info("Environment variables loaded")

# API Settings
API_HOST = "0.0.0.0"
API_PORT = 8000
LOAN_TRANSFER_API_URL = "http://localhost:8080/api/loans/transfer"

# OpenAI Settings
OPENAI_MODEL = "gpt-3.5-turbo-1106"
OPENAI_TEMPERATURE = 0
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set") 