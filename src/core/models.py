from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Union

class UserInput(BaseModel):
    """Input model for processing natural language requests."""
    text: str = Field(
        ...,
        description="The natural language text to process",
        example="Transfer loans from user1 to user2"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "text": "Transfer loans from user1 to user2"
            }
        }
    }

class LoanTransferRequest(BaseModel):
    """Request model for loan transfer operations."""
    fromUsername: str = Field(
        ...,
        description="Username of the source account",
        example="user1"
    )
    toUsername: str = Field(
        ...,
        description="Username of the destination account",
        example="user2"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "fromUsername": "user1",
                "toUsername": "user2"
            }
        }
    }

class LoanTransferResponse(BaseModel):
    """Response model for loan transfer operations."""
    status: str = Field(
        ...,
        description="Status of the operation (success/error)",
        example="success"
    )
    message: str = Field(
        ...,
        description="Detailed message about the operation result",
        example="Successfully transferred loans from user1 to user2"
    )
    details: Optional[Dict[str, Any]] = Field(
        None,
        description="Additional details about the operation if available"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "Successfully transferred loans from user1 to user2",
                "details": {
                    "fromUsername": "user1",
                    "toUsername": "user2",
                    "timestamp": "2024-03-14T12:00:00Z"
                }
            }
        }
    }

class UserCountResponse(BaseModel):
    """Response model for user count operations."""
    status: str = Field(
        ...,
        description="Status of the operation (success/error)",
        example="success"
    )
    message: str = Field(
        ...,
        description="Detailed message about the operation result",
        example="There are 5 users in the system"
    )
    count: Optional[int] = Field(
        None,
        description="Total number of users in the system",
        example=5
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "status": "success",
                "message": "There are 5 users in the system",
                "count": 5
            }
        }
    } 