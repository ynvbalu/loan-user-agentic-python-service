from fastapi import APIRouter, HTTPException
import logging
import traceback
from src.core.models import UserInput, LoanTransferResponse, UserCountResponse
from src.core.agent import create_agent

logger = logging.getLogger(__name__)
router = APIRouter()

# Create agent instance
agent_executor = create_agent()

@router.post(
    "/process",
    response_model=LoanTransferResponse,
    summary="Process Natural Language Request",
    description="""
    Process natural language requests for loan transfers and user information.
    
    This endpoint accepts natural language text and uses an AI agent to:
    - Transfer loans between users
    - Get user count information
    
    Examples of supported requests:
    - "Transfer loans from user1 to user2"
    - "Move user1's loans to user2"
    - "How many users are there?"
    - "Get me the total number of users"
    """,
    responses={
        200: {
            "description": "Successful operation",
            "content": {
                "application/json": {
                    "example": {
                        "status": "success",
                        "message": "Successfully transferred loans from user1 to user2",
                        "details": {
                            "fromUsername": "user1",
                            "toUsername": "user2"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid input or request format",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Invalid request format",
                        "details": {"error": "Could not understand the request"}
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {
                        "status": "error",
                        "message": "Internal server error",
                        "details": {"error": "An unexpected error occurred"}
                    }
                }
            }
        }
    }
)
async def process_input(user_input: UserInput) -> LoanTransferResponse:
    """
    Process natural language input and perform the requested operation.
    
    Args:
        user_input (UserInput): The natural language input to process
        
    Returns:
        LoanTransferResponse: The result of the operation
        
    Raises:
        HTTPException: If there's an error processing the request
    """
    try:
        logger.info(f"Processing input: {user_input.text}")
        result = await agent_executor.ainvoke({"input": user_input.text})
        logger.info(f"Agent result: {result}")
        
        # Ensure consistent response format
        if isinstance(result, str):
            return LoanTransferResponse(
                status="success",
                message=result,
                details={"raw_response": result}
            )
        elif isinstance(result, dict):
            return LoanTransferResponse(
                status="success",
                message=result.get("message", "Operation completed successfully"),
                details=result
            )
        else:
            return LoanTransferResponse(
                status="success",
                message=str(result),
                details={"raw_response": str(result)}
            )
            
    except Exception as e:
        logger.error(f"Error processing input: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail={
                "status": "error",
                "message": "Failed to process request",
                "details": {"error": str(e)}
            }
        ) 