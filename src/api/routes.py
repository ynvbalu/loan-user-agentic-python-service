from fastapi import APIRouter, HTTPException
import logging
import traceback
from src.core.models import UserInput, LoanTransferResponse, UserCountResponse
from src.core.agent import create_agent
from fastapi.responses import PlainTextResponse

logger = logging.getLogger(__name__)
router = APIRouter()

# Create agent instance
agent_executor = create_agent()

@router.post(
    "/process",
    response_class=PlainTextResponse,
    summary="Process Natural Language Request",
    description="""
    Process natural language requests for loan transfers and user information.
    
    This endpoint accepts natural language text and uses an AI agent to:
    - Transfer loans between users
    - Get user count information
    - Check user OOO status
    
    Examples of supported requests:
    - "Transfer loans from user1 to user2"
    - "Move user1's loans to user2"
    - "How many users are there?"
    - "Get me the total number of users"
    - "Is user1 OOO?"
    - "Check if user1 is out of office"
    """,
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "text/plain": {
                    "example": "Successfully transferred loans from user1 to user2"
                }
            }
        },
        400: {
            "description": "Invalid input or request format",
            "content": {
                "text/plain": {
                    "example": "Could not understand the request"
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "text/plain": {
                    "example": "An unexpected error occurred"
                }
            }
        }
    }
)
async def process_input(user_input: UserInput) -> str:
    """
    Process natural language input and perform the requested operation.
    
    Args:
        user_input (UserInput): The natural language input to process
        
    Returns:
        str: The result message of the operation
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Processing input: {user_input.text}")
        result = await agent_executor.ainvoke({"input": user_input.text})
        logger.info(f"Agent result: {result}")
        
        # Extract just the output message from the result
        if isinstance(result, dict) and "output" in result:
            return result["output"]
        elif isinstance(result, dict) and "message" in result:
            return result["message"]
        elif isinstance(result, str):
            return result
        else:
            return str(result)
            
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        ) 