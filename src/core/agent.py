from langchain.agents import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate
import logging
from .tools import transfer_loan, get_user_count, check_user_ooo, llm

logger = logging.getLogger(__name__)

def create_agent():
    """Create and configure the LangChain agent."""
    logger.info("Setting up agent prompt...")
    system_message = SystemMessagePromptTemplate.from_template(
        """You are a helpful assistant that helps with loan transfers and user information. You can understand natural language requests for:
        1. Transferring loans between users
        2. Getting information about users
        3. Checking if users are Out of Office (OOO)
        
        For loan transfers, you can understand various ways of expressing the same request, such as:
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
        
        DO NOT try to format or modify the input text. Pass it directly to the appropriate tool.
        The tools will handle understanding the request and providing the information."""
    )

    human_message = HumanMessagePromptTemplate.from_template("{input}")
    agent_scratchpad = MessagesPlaceholder(variable_name="agent_scratchpad")

    chat_prompt = ChatPromptTemplate.from_messages([
        system_message,
        human_message,
        agent_scratchpad
    ])
    logger.info("Agent prompt setup completed")

    logger.info("Initializing OpenAIFunctionsAgent...")
    agent = OpenAIFunctionsAgent(
        llm=llm,
        tools=[transfer_loan, get_user_count, check_user_ooo],
        prompt=chat_prompt
    )
    logger.info("OpenAIFunctionsAgent initialized successfully")

    logger.info("Creating AgentExecutor...")
    agent_executor = AgentExecutor(
        agent=agent,
        tools=[transfer_loan, get_user_count, check_user_ooo],
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=3,
        return_direct=True
    )
    logger.info("AgentExecutor created successfully")

    return agent_executor 