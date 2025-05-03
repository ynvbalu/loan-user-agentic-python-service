from fastapi import FastAPI
import logging
from src.api.routes import router
from src.config.settings import API_HOST, API_PORT

logger = logging.getLogger(__name__)

app = FastAPI(title="Loan User Agentic Service")
app.include_router(router)

if __name__ == "__main__":
    logger.info("Starting FastAPI application...")
    import uvicorn
    uvicorn.run(app, host=API_HOST, port=API_PORT) 