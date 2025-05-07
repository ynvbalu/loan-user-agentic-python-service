from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts import (MessagesPlaceholder, HumanMessagePromptTemplate,
                               ChatPromptTemplate, SystemMessagePromptTemplate)
import logging
from .tools import transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo, llm

logger = logging.getLogger(__name__)

def create_agent():
    """Create and configure the LangChain agent."""
    logger.info("Setting up agent prompt...")
    system_message = SystemMessagePromptTemplate.from_template(
        """You are a helpful assistant that helps with loan transfers and user information. 
        You can understand natural language requests for:
        1. Transferring loans between users
        2. Getting information about users
        3. Checking if users are Out of Office (OOO)
        4. Checking if users have loans
        5. Setting users' OOO status
        
        For loan transfers, you MUST follow these rules:
        1. ALWAYS check if the source user (user1) is OOO before proceeding with any transfer
        2. Only proceed with the transfer if the source user is confirmed to be OOO
        3. If the source user is not OOO, explain why the transfer cannot proceed
        4. Consider the following scenarios:
           - If user1 is OOO: Proceed with transfer to user2
           - If user1 is not OOO: Reject the transfer and explain why
           - If OOO status is unclear: Ask for clarification
        
        You can understand various ways of expressing transfer requests, such as:
        - "Transfer loans from user1 to user2"
        - "Move user1's loans to user2"
        - "Send funds from user1 to user2"
        - "Give user1's loans to user2"
        
        For user information, you can handle questions like:
        - "How many users are there?"
        - "What's the total number of users?"
        - "Get me the user count"
        - "Count of users"
        
        For OOO status checks, you can handle questions like:
        - "Is user1 OOO?"
        - "Check if user1 is out of office"
        - "Is user1 available?"
        - "Get OOO status for user1"

        For setting OOO status, you can handle requests like:
        - "Set user1 as OOO"
        - "Mark user1 as out of office"
        - "Update user1's OOO status to true"
        - "Change user1's availability to out of office"

        For loan checks, you can handle questions like:
        - "Does user1 have any loans?"
        - "Check if user1 has loans"
        - "How many loans does user1 have?"
        - "Get loan count for user1"
        
        When processing transfer requests:
        1. First check the OOO status of the source user
        2. Only proceed with the transfer if OOO status is confirmed
        3. Provide clear explanations for your decisions
        4. Handle edge cases gracefully
        
        DO NOT try to format or modify the input text. Pass it directly to the appropriate tool.
        The tools will handle understanding the request and providing the information."""
    )
    logger.info(f"system_message: {system_message}")

    human_message = HumanMessagePromptTemplate.from_template("{input}")
    logger.info(f"human_message: {human_message}")

    agent_scratchpad = MessagesPlaceholder(variable_name="agent_scratchpad")
    logger.info(f"agent_scratchpad: {agent_scratchpad}")

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message,
        human_message,
        agent_scratchpad
    ])
    logger.info("Agent prompt setup completed")
    logger.info(f"chat_prompt: {chat_prompt}")

    tools_list = [transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo]
    logger.info(f"Tools being used: {[tool.name for tool in tools_list]}")

    logger.info("Initializing OpenAIFunctionsAgent...")
    agent = OpenAIFunctionsAgent(
        llm=llm,
        tools=tools_list,
        prompt=chat_prompt
    )
    logger.info("OpenAIFunctionsAgent initialized successfully")
    logger.info(f"agent: {agent}")

    logger.info("Creating AgentExecutor...")
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_list,
        handle_parsing_errors=True,
        max_iterations=3,
        verbose=True,
        return_direct=True
    )
    logger.info("AgentExecutor created successfully")
    logger.info(f"agent_executor: {agent_executor}")

    return agent_executor 