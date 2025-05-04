from langchain.tools import tool
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import httpx
import json
import logging
from fastapi import HTTPException
from src.config.settings import LOAN_TRANSFER_API_URL, OPENAI_MODEL, OPENAI_TEMPERATURE, OPENAI_API_KEY
import traceback

logger = logging.getLogger(__name__)

# Initialize OpenAI model
llm = ChatOpenAI(
    model=OPENAI_MODEL,
    temperature=OPENAI_TEMPERATURE,
    api_key=OPENAI_API_KEY
)

@tool("get_user_count")
async def get_user_count(input_str: str = "") -> Dict[str, Any]:
    """Get the total number of users in the system.
    This tool can be used when someone asks about:
    - How many users are there?
    - What's the total number of users?
    - Get me the user count
    - Count of users
    The tool will return the total number of users in the system."""
    try:
        logger.debug("Getting user count...")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    "http://localhost:8080/api/users/count",
                    headers={"Content-Type": "application/json"}
                )
                logger.debug(f"API Response status: {response.status_code}")
                logger.debug(f"API Response headers: {response.headers}")
                logger.debug(f"API Response content: {response.text}")
                
                response.raise_for_status()
                
                try:
                    result = response.json()
                    # Handle both integer and dictionary responses
                    if isinstance(result, int):
                        count = result
                    else:
                        count = result.get('count', 0)
                        
                    logger.info(f"Successfully retrieved user count: {count}")
                    return {
                        "status": "success",
                        "message": f"There are {count} users in the system.",
                        "count": count
                    }
                except json.JSONDecodeError as json_err:
                    # Try to parse as integer if JSON parsing fails
                    try:
                        count = int(response.text)
                        logger.info(f"Successfully retrieved user count: {count}")
                        return {
                            "status": "success",
                            "message": f"There are {count} users in the system.",
                            "count": count
                        }
                    except ValueError:
                        logger.warning(f"Could not parse API response as JSON or integer: {json_err}")
                        return {
                            "status": "success",
                            "message": f"Successfully retrieved user count: {response.text}",
                            "raw_response": response.text
                        }
                    
            except httpx.HTTPError as http_error:
                logger.error(f"HTTP error occurred: {str(http_error)}")
                logger.error(f"Response content: {http_error.response.text if hasattr(http_error, 'response') else 'No response content'}")
                raise ValueError(f"Failed to get user count: {str(http_error)}")
    except Exception as e:
        logger.error(f"Error in get_user_count: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise ValueError(f"Failed to get user count: {str(e)}")

@tool("transfer_loan")
async def transfer_loan(input_str: str) -> Dict[str, Any]:
    """Transfer loans between users. The input can be in natural language.
    Examples:
    - "Transfer loans from user1 to user2"
    - "Move user1's loans to user2"
    - "Send funds from user1 to user2"
    - "Give user1's loans to user2"
    - "Transfer loan IDs 1,2,3 from user1 to user2"
    The tool will understand the request and make the transfer."""
    try:
        logger.debug(f"transfer_loan called with input type: {type(input_str)}")
        logger.debug(f"transfer_loan raw input: {input_str}")
        
        # Use LLM to extract usernames and optional loan IDs from natural language input
        extraction_prompt = f"""Extract the source and destination usernames and optional loan IDs from this loan transfer request.
        Input: {input_str}
        Return a JSON object with 'fromUsername', 'toUsername', and optional 'loanIds' fields.
        Example 1: {{"fromUsername": "user1", "toUsername": "user2"}}
        Example 2: {{"fromUsername": "user1", "toUsername": "user2", "loanIds": [1, 2, 3]}}
        """
        
        extraction_result = await llm.ainvoke(extraction_prompt)
        logger.debug(f"LLM extraction result: {extraction_result}")
        
        try:
            input_dict = json.loads(extraction_result.content)
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            raise ValueError("Could not understand the loan transfer request. Please try rephrasing.")
            
        from_username = input_dict.get("fromUsername")
        to_username = input_dict.get("toUsername")
        loan_ids = input_dict.get("loanIds")
        
        logger.debug(f"Extracted usernames - from: {from_username}, to: {to_username}")
        logger.debug(f"Extracted loan IDs: {loan_ids}")
        
        if not from_username or not to_username:
            logger.error("Missing required username fields")
            raise ValueError("Could not identify both source and destination users. Please try rephrasing.")
        
        # Prepare the request payload
        payload = {
            "fromUsername": from_username,
            "toUsername": to_username
        }
        if loan_ids:
            payload["loanIds"] = loan_ids
        
        async with httpx.AsyncClient() as client:
            logger.info(f"Making API call to transfer loans from {from_username} to {to_username}")
            try:
                response = await client.post(
                    LOAN_TRANSFER_API_URL,
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                logger.debug(f"API Response status: {response.status_code}")
                logger.debug(f"API Response headers: {response.headers}")
                logger.debug(f"API Response content: {response.text}")
                
                response.raise_for_status()
                
                # Handle empty response
                if not response.text:
                    logger.info("Received empty response from API, assuming success")
                    return {
                        "status": "success",
                        "message": f"Successfully transferred loans from {from_username} to {to_username}",
                        "fromUsername": from_username,
                        "toUsername": to_username,
                        "loanIds": loan_ids
                    }
                
                try:
                    result = response.json()
                    logger.info(f"Transfer successful: {result}")
                    return result
                except json.JSONDecodeError as json_err:
                    logger.warning(f"Could not parse API response as JSON: {json_err}")
                    # Return a success message even if response is not JSON
                    return {
                        "status": "success",
                        "message": f"Successfully transferred loans from {from_username} to {to_username}",
                        "fromUsername": from_username,
                        "toUsername": to_username,
                        "loanIds": loan_ids,
                        "raw_response": response.text
                    }
                    
            except httpx.HTTPError as http_error:
                logger.error(f"HTTP error occurred: {str(http_error)}")
                logger.error(f"Response content: {http_error.response.text if hasattr(http_error, 'response') else 'No response content'}")
                raise ValueError(f"Failed to transfer loans: {str(http_error)}")
    except Exception as e:
        logger.error(f"Error in transfer_loan: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise ValueError(f"Failed to process loan transfer: {str(e)}")

@tool("check_user_ooo")
async def check_user_ooo(input_str: str) -> Dict[str, Any]:
    """Check if a user is Out of Office (OOO).
    This tool can be used when someone asks about:
    - Is user1 OOO?
    - Check if user1 is out of office
    - Is user1 available?
    - Get OOO status for user1
    The tool will return whether the specified user is OOO or not."""
    try:
        logger.debug(f"check_user_ooo called with input: {input_str}")
        
        # Use LLM to extract username from natural language input
        extraction_prompt = f"""Extract the username from this OOO status check request.
        Input: {input_str}
        Return a JSON object with 'username' field.
        Example: {{"username": "user1"}}
        """
        
        extraction_result = await llm.ainvoke(extraction_prompt)
        logger.debug(f"LLM extraction result: {extraction_result}")
        
        try:
            input_dict = json.loads(extraction_result.content)
        except json.JSONDecodeError:
            logger.error("Failed to parse LLM response as JSON")
            raise ValueError("Could not understand the OOO status check request. Please try rephrasing.")
            
        username = input_dict.get("username")
        
        if not username:
            logger.error("Missing username field")
            raise ValueError("Could not identify the user. Please try rephrasing.")
        
        async with httpx.AsyncClient() as client:
            logger.info(f"Checking OOO status for user: {username}")
            try:
                response = await client.get(
                    f"http://localhost:8080/api/users/username/{username}/ooo",
                    headers={"Content-Type": "application/json"}
                )
                logger.debug(f"API Response status: {response.status_code}")
                logger.debug(f"API Response headers: {response.headers}")
                logger.debug(f"API Response content: {response.text}")
                
                # Handle 404 Not Found specifically
                if response.status_code == 404:
                    return {
                        "status": "error",
                        "message": f"User '{username}' does not exist in the system.",
                        "username": username,
                        "error_type": "user_not_found"
                    }
                
                response.raise_for_status()
                
                try:
                    result = response.json()
                    is_ooo = bool(result)
                    status_message = "is" if is_ooo else "is not"
                    return {
                        "status": "success",
                        "message": f"User {username} {status_message} Out of Office",
                        "username": username,
                        "is_ooo": is_ooo
                    }
                except json.JSONDecodeError as json_err:
                    # Try to parse as boolean if JSON parsing fails
                    try:
                        is_ooo = response.text.lower() == "true"
                        status_message = "is" if is_ooo else "is not"
                        return {
                            "status": "success",
                            "message": f"User {username} {status_message} Out of Office",
                            "username": username,
                            "is_ooo": is_ooo
                        }
                    except ValueError:
                        logger.warning(f"Could not parse API response as JSON or boolean: {json_err}")
                        return {
                            "status": "success",
                            "message": f"OOO status for user {username}: {response.text}",
                            "username": username,
                            "raw_response": response.text
                        }
                    
            except httpx.HTTPError as http_error:
                logger.error(f"HTTP error occurred: {str(http_error)}")
                logger.error(f"Response content: {http_error.response.text if hasattr(http_error, 'response') else 'No response content'}")
                # Handle 404 Not Found specifically
                if hasattr(http_error, 'response') and http_error.response.status_code == 404:
                    return {
                        "status": "error",
                        "message": f"User '{username}' does not exist in the system.",
                        "username": username,
                        "error_type": "user_not_found"
                    }
                raise ValueError(f"Failed to check OOO status: {str(http_error)}")
    except Exception as e:
        logger.error(f"Error in check_user_ooo: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise ValueError(f"Failed to check OOO status: {str(e)}") 