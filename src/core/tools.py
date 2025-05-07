from langchain.tools import BaseTool
from langchain_openai import ChatOpenAI
import requests
import json
import logging

from src.config.settings import (LOAN_TRANSFER_API_URL, OPENAI_MODEL, OPENAI_TEMPERATURE,
                                 OPENAI_API_KEY, BASE_API_URL)
import traceback

logger = logging.getLogger(__name__)

# Initialize OpenAI model
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=OPENAI_TEMPERATURE,
    api_key=OPENAI_API_KEY
)

class TransferLoanTool(BaseTool):
    name = "transfer_loan"
    description = """Transfer loans between users. The input can be in natural language.
    Examples:
    - "Transfer loans from user1 to user2"
    - "Move user1's loans to user2"
    - "Send funds from user1 to user2"
    - "Give user1's loans to user2"
    - "Transfer loan IDs 1,2,3 from user1 to user2"
    The tool will understand the request and make the transfer.
    IMPORTANT: The transfer will only proceed if the source user (user1) is confirmed to be OOO."""

    def _run(self, input_str: str) -> str:
        try:
            # Extract usernames using LLM
            extraction_prompt = f"""Extract the source and destination usernames from this loan 
            transfer request.
            Input: {input_str}
            Return a JSON object with 'fromUsername' and 'toUsername' fields.
            Example: {{"fromUsername": "user1", "toUsername": "user2"}}
            """
            
            extraction_result = llm.invoke(extraction_prompt)
            logger.debug(f"LLM extraction result: {extraction_result}")
            
            try:
                input_dict = json.loads(extraction_result.content)
            except json.JSONDecodeError:
                return "Could not understand the loan transfer request. Please try rephrasing."
                
            from_username = input_dict.get("fromUsername", "").lower()
            to_username = input_dict.get("toUsername", "").lower()
            
            if not from_username or not to_username:
                return "Could not identify both source and destination users. Please try rephrasing."
            
            # Check if source user has loans using CheckUserLoansTool
            loans_check = check_user_loans._run(f"Check if {from_username} has loans")
            if "has no loans" in loans_check:
                return f"Cannot transfer loans: User '{from_username}' has no loans to transfer."
            
            # Check OOO status using CheckUserOOOTool
            ooo_check = check_user_ooo._run(f"Check if {from_username} is OOO")
            if "is not Out of Office" in ooo_check:
                return f"I'm sorry, but I cannot proceed with the loan transfer from {from_username} to {to_username} because {from_username} is not Out of Office. Please confirm if {from_username} is currently Out of Office to proceed with the transfer."
            
            # Execute transfer
            payload = {
                "fromUsername": from_username,
                "toUsername": to_username
            }
            
            response = requests.post(
                LOAN_TRANSFER_API_URL,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            
            if not response.text:
                return f"Successfully transferred loans from {from_username} to {to_username}"
            
            try:
                result = response.json()
                return f"Successfully transferred loans from {from_username} to {to_username}"
            except json.JSONDecodeError:
                return f"Successfully transferred loans from {from_username} to {to_username}"
                
        except Exception as e:
            logger.error(f"Error in transfer_loan: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            return f"Failed to transfer loans: {str(e)}"

class GetUserCountTool(BaseTool):
    name = "get_user_count"
    description = """Get the total number of users in the system.
    This tool can be used when someone asks about:
    - How many users are there?
    - What's the total number of users?
    - Get me the user count
    - Count of users
    The tool will return the total number of users in the system."""

    def _run(self, input_str: str = "") -> str:
        try:
            logger.debug("Getting user count...")
            response = requests.get(
                f"{BASE_API_URL}/api/users/count",
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            try:
                result = response.json()
                if isinstance(result, int):
                    count = result
                else:
                    count = result.get('count', 0)
                
                return f"There are {count} users in the system."
            except json.JSONDecodeError:
                try:
                    count = int(response.text)
                    return f"There are {count} users in the system."
                except ValueError:
                    return f"Successfully retrieved user count: {response.text}"
        except Exception as e:
            logger.error(f"Error in get_user_count: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to get user count: {str(e)}")

class CheckUserOOOTool(BaseTool):
    name = "check_user_ooo"
    description = """Check if a user is Out of Office (OOO).
    This tool can be used when someone asks about:
    - Is user1 OOO?
    - Check if user1 is out of office
    - Is user1 available?
    - Get OOO status for user1
    The tool will return whether the specified user is OOO or not."""

    def _run(self, input_str: str) -> str:
        try:
            logger.debug(f"check_user_ooo called with input: {input_str}")
            
            extraction_prompt = f"""Extract the username from this OOO status check request.
            Input: {input_str}
            Return a JSON object with 'username' field.
            Example: {{"username": "user1"}}
            """
            
            extraction_result = llm.invoke(extraction_prompt)
            logger.debug(f"LLM extraction result: {extraction_result}")
            
            try:
                input_dict = json.loads(extraction_result.content)
            except json.JSONDecodeError:
                raise ValueError("Could not understand the OOO status check request. Please try rephrasing.")
                
            username = input_dict.get("username", "").lower()
            
            if not username:
                raise ValueError("Could not identify the user. Please try rephrasing.")
            
            logger.info(f"Checking OOO status for user: {username}")
            response = requests.get(
                f"{BASE_API_URL}/api/users/username/{username}",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 404:
                return f"User '{username}' does not exist in the system."
            
            response.raise_for_status()
            
            try:
                result = response.json()
                is_ooo = result.get("oooStatus", False)
            except json.JSONDecodeError:
                raise ValueError("Failed to parse user data")
            
            if "available" in input_str.lower():
                return f"User {username} is {'not available (OOO)' if is_ooo else 'available'}"
            else:
                return f"User {username} is {'Out of Office' if is_ooo else 'in office'}"
                
        except Exception as e:
            logger.error(f"Error in check_user_ooo: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to check OOO status: {str(e)}")

class CheckUserLoansTool(BaseTool):
    name = "check_user_loans"
    description = """Check if a user has any loans.
    This tool can be used when someone asks about:
    - Does user1 have any loans?
    - Check if user1 has loans
    - How many loans does user1 have?
    - Get loan count for user1
    The tool will return whether the specified user has loans and the total count."""

    def _run(self, input_str: str) -> str:
        try:
            logger.debug(f"check_user_loans called with input: {input_str}")
            
            extraction_prompt = f"""Extract the username from this loan check request.
            Input: {input_str}
            Return a JSON object with 'username' field.
            Example: {{"username": "user1"}}
            """
            
            extraction_result = llm.invoke(extraction_prompt)
            logger.debug(f"LLM extraction result: {extraction_result}")
            
            try:
                input_dict = json.loads(extraction_result.content)
            except json.JSONDecodeError:
                raise ValueError("Could not understand the loan check request. Please try rephrasing.")
                
            username = input_dict.get("username", "").lower()
            
            if not username:
                raise ValueError("Could not identify the user. Please try rephrasing.")
            
            logger.info(f"Checking loans for user: {username}")
            response = requests.get(
                f"{BASE_API_URL}/api/loans/username/{username}/has-loans",
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 404:
                return f"User '{username}' does not exist in the system."
            
            response.raise_for_status()
            result = response.json()
            
            has_loans = result.get("hasLoans", False)
            loan_count = result.get("loanCount", 0)
            
            if has_loans:
                return f"User {username} has {loan_count} loan(s)"
            else:
                return f"User {username} has no loans"
                
        except Exception as e:
            logger.error(f"Error in check_user_loans: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to check loans: {str(e)}")

class SetUserOOOTool(BaseTool):
    name = "set_user_ooo"
    description = """Set a user's Out of Office (OOO) status.
    This tool can be used when someone wants to:
    - Set user1 as OOO
    - Mark user1 as out of office
    - Update user1's OOO status
    - Change user1's availability
    The tool will update the user's OOO status to either true or false.
    Examples:
    - "Set user1 as OOO"
    - "Mark user1 as not OOO"
    - "Update user1's OOO status to true"
    - "Change user1's availability to out of office"
    - "Set user1 as available"
    - "Mark user1 as in office"
    """

    def _run(self, input_str: str) -> str:
        try:
            logger.debug(f"set_user_ooo called with input: {input_str}")
            
            extraction_prompt = f"""Extract the username and desired OOO status from this request.
            Input: {input_str}
            Return a JSON object with 'username' and 'oooStatus' fields.
            
            Rules for determining oooStatus:
            1. Set oooStatus to true if the request indicates:
               - Setting as OOO
               - Marking as out of office
               - Setting as unavailable
               - Any phrase indicating the user is not available
            
            2. Set oooStatus to false if the request indicates:
               - Setting as available
               - Marking as in office
               - Setting as not OOO
               - Any phrase indicating the user is available
            
            Example: {{"username": "user1", "oooStatus": true}}
            """
            
            extraction_result = llm.invoke(extraction_prompt)
            logger.debug(f"LLM extraction result: {extraction_result}")
            
            try:
                input_dict = json.loads(extraction_result.content)
            except json.JSONDecodeError:
                raise ValueError("Could not understand the OOO status update request. Please try rephrasing.")
                
            username = input_dict.get("username", "").lower()
            ooo_status = input_dict.get("oooStatus", False)
            
            if not username:
                raise ValueError("Could not identify the user. Please try rephrasing.")
            
            logger.info(f"Setting OOO status for user: {username} to {ooo_status}")
            response = requests.put(
                f"{BASE_API_URL}/api/users/username/{username}/ooo",
                json={"oooStatus": ooo_status},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 404:
                return f"User '{username}' does not exist in the system."
            
            response.raise_for_status()
            
            try:
                result = response.json()
                actual_status = result.get("oooStatus", ooo_status)
                status_word = "Out of Office" if actual_status else "available"
                return f"Successfully set user {username} as {status_word}"
            except json.JSONDecodeError:
                status_word = "Out of Office" if ooo_status else "available"
                return f"Successfully set user {username} as {status_word}"
                
        except Exception as e:
            logger.error(f"Error in set_user_ooo: {str(e)}")
            logger.error(f"Full traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to set OOO status: {str(e)}")

# Initialize tools
transfer_loan = TransferLoanTool()
get_user_count = GetUserCountTool()
check_user_ooo = CheckUserOOOTool()
check_user_loans = CheckUserLoansTool()
set_user_ooo = SetUserOOOTool() 