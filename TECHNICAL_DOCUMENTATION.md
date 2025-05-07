# Loan Management System - Technical Documentation

## Overview
This document explains the core components of the Loan Management System's AI service, focusing on the agent.py and tools.py files that work together to provide a natural language interface for loan management operations.

## Core Components

### 1. Language Model Configuration
```python
llm = ChatOpenAI(
    model=OPENAI_MODEL,  # GPT-3.5-turbo-1106
    temperature=OPENAI_TEMPERATURE,
    api_key=OPENAI_API_KEY
)
```
- Uses GPT-3.5-turbo-1106 for natural language understanding
- Configurable temperature for response variability
- Secure API key management

## Agent Implementation (agent.py)

### 1. Agent Structure
The agent is built using LangChain's OpenAIFunctionsAgent, which combines:
- GPT-3.5-turbo-1106 for natural language understanding
- Custom tools for specific operations
- Structured prompt templates
- Error handling and logging

### 2. System Message
The system message defines the agent's capabilities and rules:
```python
system_message = SystemMessagePromptTemplate.from_template(
    """You are a helpful assistant that helps with loan transfers and user information.
    You can understand natural language requests for:
    1. Transferring loans between users
    2. Getting information about users
    3. Checking if users are Out of Office (OOO)
    4. Checking if users have loans
    5. Setting users' OOO status
    ...
    """
)
```

### 3. Prompt Template
The agent uses a three-part chat prompt:
1. System Message: Instructions and capabilities
2. Human Message: User input
3. Agent Scratchpad: Agent's thought process

### 4. Agent Configuration
```python
agent = OpenAIFunctionsAgent(
    llm=llm,
    tools=[transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo],
    prompt=chat_prompt
)
```

### 5. Agent Executor
```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=[transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo],
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=3,
    return_direct=True
)
```

## Tools Implementation (tools.py)

### 1. Base Tool Structure
All tools inherit from LangChain's BaseTool and implement:
- Name and description
- _run method for execution
- Error handling and logging
- Natural language processing

### 2. TransferLoanTool
```python
class TransferLoanTool(BaseTool):
    name = "transfer_loan"
    description = """Transfer loans between users..."""
```
Key Features:
- Extracts usernames from natural language
- Validates OOO status
- Checks for existing loans
- Executes the transfer
- Returns formatted response

### 3. GetUserCountTool
```python
class GetUserCountTool(BaseTool):
    name = "get_user_count"
    description = """Get the total number of users..."""
```
Key Features:
- Simple API call to get user count
- JSON response parsing
- Formatted output

### 4. CheckUserOOOTool
```python
class CheckUserOOOTool(BaseTool):
    name = "check_user_ooo"
    description = """Check if a user is Out of Office..."""
```
Key Features:
- Username extraction from natural language
- User existence verification
- OOO status check
- Formatted response

### 5. CheckUserLoansTool
```python
class CheckUserLoansTool(BaseTool):
    name = "check_user_loans"
    description = """Check if a user has any loans..."""
```
Key Features:
- Username extraction from natural language
- User existence verification
- Loan count and status check
- Formatted response

## Tool Interaction Flow

### 1. Natural Language Processing
1. User input is received by the agent
2. GPT-3.5-turbo-1106 understands the intent
3. Appropriate tool is selected
4. Tool extracts necessary information

### 2. Validation Steps
1. User existence check
2. OOO status verification
3. Loan availability check
4. Business rule validation

### 3. API Communication
1. Tool makes API call to backend
2. Response is processed
3. Error handling if needed
4. Formatted response returned

## Error Handling

### 1. Tool Level
- Input validation
- API error handling
- JSON parsing errors
- User existence checks

### 2. Agent Level
- Parsing errors
- Maximum iterations
- Tool selection errors
- Response formatting

## Logging

### 1. Tool Logging
- Input parameters
- API calls
- Error details
- Response data

### 2. Agent Logging
- Tool selection
- Execution flow
- Error handling
- Performance metrics

## Security Features

### 1. Input Validation
- Username sanitization
- JSON parsing safety
- API response validation

### 2. Error Message Sanitization
- No sensitive data in errors
- User-friendly messages
- Secure logging

## Best Practices

### 1. Code Organization
- Clear class structure
- Consistent error handling
- Comprehensive logging
- Type hints and documentation

### 2. API Integration
- Proper error handling
- Response validation
- Secure communication
- Rate limiting consideration

### 3. Natural Language Processing
- Clear tool descriptions
- Consistent response formats
- User-friendly messages
- Context maintenance 