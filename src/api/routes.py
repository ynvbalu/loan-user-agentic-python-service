from fastapi import APIRouter, HTTPException
import logging
import traceback
from src.core.models import UserInput, LoanTransferResponse
from src.core.agent import create_agent

logger = logging.getLogger(__name__)
router = APIRouter()

# Create agent instance
agent_executor = create_agent()

@router.post("/process", response_model=LoanTransferResponse)
async def process_input(user_input: UserInput):
    """Process user input using the LangChain agent."""
    try:
        logger.info(f"Received request to process: {user_input.text}")
        logger.debug(f"Input type: {type(user_input.text)}")
        
        logger.info("Invoking agent executor...")
        result = await agent_executor.ainvoke(
            {"input": user_input.text},
            return_only_outputs=True
        )
        logger.debug(f"Raw agent execution result: {result}")
        
        # Handle the result
        if isinstance(result, dict) and "output" in result:
            output = result["output"]
            # If output is a coroutine, await it
            if hasattr(output, "__await__"):
                response = await output
            else:
                response = output
        else:
            response = result
            
        # Ensure response is in the correct format
        if isinstance(response, str):
            # If response is a string, wrap it in a dictionary
            response = {
                "status": "success",
                "message": response
            }
            
        logger.info(f"Agent execution completed successfully")
        return {"response": response}
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e)) 