from pydantic import BaseModel
from typing import Dict, Any, Union

class UserInput(BaseModel):
    text: str

class LoanTransferRequest(BaseModel):
    fromUsername: str
    toUsername: str

class LoanTransferResponse(BaseModel):
    response: Union[Dict[str, Any], str] 