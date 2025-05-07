# Loan Management System - High Level Overview

## System Purpose
An intelligent loan management system that automatically handles loan transfers when officers go Out of Office (OOO), powered by AI and natural language processing.

## Key Components
1. **AI Chatbot Interface**
   - Natural language interaction
   - Real-time loan transfer requests
   - Smart status updates

2. **Loan Management Backend**
   - Secure loan transfers
   - User status tracking
   - Data persistence

3. **AI Service**
   - GPT-3.5-turbo-1106 powered
   - Natural language understanding
   - Automated decision making

## Core Features
- Automated loan transfers for OOO officers
- Natural language chatbot interface
- Real-time status updates
- Secure data handling
- Smart validation rules

## Example Flow
```
User: "Transfer loans from ALEX to BRIAN"
System: Checks OOO status → Validates loans → Executes transfer → Confirms completion
```

## Technology Stack
- Frontend: React + TypeScript
- Backend: Spring Boot
- AI: Python + LangChain + GPT-3.5
- Database: H2

# Loan User AI Service Documentation

## Use Case
When a loan officer (ALEX) goes Out of Office (OOO), their loans need to be transferred to another officer (BRIAN). Our AI service automates this through natural language processing using the GPT-3.5-turbo-1106 model.

## Technologies Used

### Frontend
- React 18
  - Modern UI components
  - Hooks for state management
  - Functional components
- TypeScript
  - Type safety
  - Better IDE support
  - Enhanced maintainability
- Material-UI
  - Pre-built components
  - Responsive design
  - Theme customization
- Redux Toolkit
  - State management
  - API integration
  - Action creators
- React Router
  - Navigation
  - Route protection
  - Dynamic routing
- Vite


### AI Service
- Python 3.8+
- LangChain
- OpenAI GPT-3.5-turbo-1106
  - Natural language understanding
  - Context awareness
  - Response generation
- FastAPI
  - REST API endpoints
  - Async support
  - OpenAPI documentation
- Poetry
  - Dependency management
  - Virtual environment
  - Build system
- Pydantic
  - Data validation
  - Type checking
  - Schema generation

### Backend
- Spring Boot 3.2.3
  - RESTful APIs
  - Dependency injection
  - Auto-configuration
- Java 21
  - Modern Java features
  - Pattern matching
  - Record classes
- H2 Database
  - In-memory database
  - SQL support
  - Data persistence
- Spring Data JPA
  - Repository pattern
  - Query methods
  - Transaction management
- OpenAPI/Swagger
  - API documentation
  - Interactive testing
  - Schema validation
- Maven
  - Build automation
  - Dependency management
  - Project structure

## System Architecture

### Frontend Chatbot Interface
- Modern React/TypeScript implementation
- Material-UI components for clean design
- Real-time chat interface
- Example UI Flow:
```
┌─────────────────────────────────┐
│ Chat Interface                  │
├─────────────────────────────────┤
│ User: Transfer loans from ALEX  │
│      to BRIAN                   │
│                                 │
│ Bot: Let me check if ALEX is    │
│      OOO first...               │
│                                 │
│ Bot: ALEX is Out of Office.     │
│      Transferring loans...      │
│                                 │
│ Bot: Successfully transferred   │
│      loans to BRIAN             │
└─────────────────────────────────┘
```

### Backend Service Integration
- Spring Boot REST APIs
- Key Endpoints:
  - `/api/users/username/{username}/ooo` - OOO status
  - `/api/loans/transfer` - Loan transfer
  - `/api/users/count` - User count
- H2 Database for data persistence
- Swagger documentation

## AI Service Overview

### 1. Core Components (`agent.py`)
```python
OPENAI_MODEL = "gpt-3.5-turbo-1106"

def create_agent():
    system_message = """You are a helpful assistant that helps with loan transfers and user information.
    You can understand natural language requests for:
    1. Transferring loans between users
    2. Getting information about users
    3. Checking if users are Out of Office (OOO)
    4. Checking if users have loans
    5. Setting users' OOO status"""

    agent = OpenAIFunctionsAgent(
        llm=llm,  # Configured with GPT-3.5-turbo-1106
        tools=[transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo],
        prompt=chat_prompt
    )
```

### 2. Key Tools (`tools.py`)
```python
# OOO Status Check
@api_tool("Check if a user is Out of Office (OOO)")
def check_user_ooo(self, username: str) -> UserInfo:
    response = requests.get(
        f"{self.base_url}/api/users/username/{username}/ooo"
    )
    return UserInfo(
        username=username,
        ooo_status=bool(response.json())
    )

# Loan Transfer
@api_tool("Transfer loans between users")
def transfer_loan(self, from_username: str, to_username: str) -> LoanTransfer:
    # First check OOO status
    source_user = self.check_user_ooo(from_username)
    if not source_user.ooo_status:
        return LoanTransfer(
            from_username=from_username,
            to_username=to_username,
            success=False,
            message=f"Cannot transfer loans: {from_username} is not Out of Office"
        )
```

### 3. Data Models (`tools.py`)
```python
@dataclass
class UserInfo:
    username: str
    ooo_status: bool

@dataclass
class LoanTransfer:
    from_username: str
    to_username: str
    success: bool
    message: str
```

## Complete Flow Example
```
Frontend: User types "Transfer loans from ALEX to BRIAN"
AI Service: Processes request using GPT-3.5-turbo-1106
Backend: Verifies OOO status through API
AI Service: Initiates transfer if OOO status confirmed
Backend: Processes loan transfer in database
Frontend: Updates UI with success message
```

## GPT-3.5-turbo-1106 Benefits
- Better natural language understanding
- More accurate intent recognition
- Improved response generation
- Enhanced context awareness

## Integration Points
- Frontend to AI Service: REST API
- AI Service to Backend: REST API
- OpenAI API integration
- Logging system
- Error tracking

## Error Handling
- Comprehensive error handling for API calls
- User-friendly error messages
- Detailed logging for debugging
- Graceful fallback mechanisms

## Security
- API key management
- Input validation
- Error message sanitization
- Secure API communication

# Loan Management System Use Case

## Core Problem
When a loan officer (e.g., ALEX) goes Out of Office (OOO), their active loans need to be transferred to another officer (e.g., BRIAN) to ensure continuous loan management and customer service. The system uses an AI-powered chatbot to handle these requests through natural language processing.

## System Components

### 1. Frontend (React + TypeScript)
- Modern UI with Material-UI components
- AI-Powered Chatbot Interface:
  - Real-time chat window
  - Natural language input
  - Context-aware responses
  - Status updates and notifications
  - Example chat flow:
  ```
  User: "Transfer loans from ALEX to BRIAN"
  Bot: "Let me check if ALEX is OOO first..."
  Bot: "ALEX is Out of Office. Transferring loans..."
  Bot: "Successfully transferred loans to BRIAN"
  ```
- Loan management dashboard
- User management interface
- OOO status tracking and updates

### 2. Backend (Spring Boot)
- RESTful APIs for loan and user management
- Key Features:
  - User CRUD operations
  - Loan management
  - OOO status management
  - Loan transfer functionality
- H2 Database for data persistence
- Swagger documentation for API endpoints

### 3. AI Service (Python + LangChain)
- Natural language processing for loan transfer requests
- Key Features:
  - OOO status verification
  - Loan transfer validation
  - User information retrieval
  - Smart decision-making for transfers
  - Natural language understanding
  - Context-aware responses
  - Multi-turn conversations

## Business Rules

1. **OOO Status Verification**
   - Must verify source user's OOO status before transfer
   - Transfers only allowed if source user is confirmed OOO
   - Clear error messages for non-OOO users

2. **Loan Transfer Process**
   - Can transfer specific loans or all loans
   - Validates loan ownership
   - Ensures target user exists
   - Maintains transaction integrity

3. **User Management**
   - Tracks user OOO status
   - Manages user profiles
   - Handles user availability

4. **Chatbot Interaction**
   - Understands various request formats:
     - "Transfer loans from user1 to user2"
     - "Move user1's loans to user2"
     - "Send funds from user1 to user2"
     - "Give user1's loans to user2"
   - Handles user queries:
     - "Is user1 OOO?"
     - "How many users are there?"
     - "Does user1 have any loans?"
   - Provides clear explanations for actions
   - Maintains conversation context

## Example Flow

1. **User Request via Chatbot**
   ```
   User: "Transfer loans from ALEX to BRIAN"
   ```

2. **AI Service Processing**
   - Checks ALEX's OOO status
   - Verifies ALEX has loans
   - Validates BRIAN's existence
   - Provides real-time status updates

3. **Transfer Execution**
   - If ALEX is OOO: Proceeds with transfer
   - If ALEX is not OOO: Rejects with explanation
   - Updates loan ownership in database

4. **User Notification**
   - Success: Confirms transfer completion
   - Failure: Explains reason for rejection
   - Provides next steps or alternatives

## Security & Validation

1. **Input Validation**
   - Username verification
   - Loan ownership checks
   - OOO status validation
   - Natural language input sanitization

2. **Error Handling**
   - Comprehensive error messages
   - Transaction rollback
   - Logging for debugging
   - User-friendly error explanations

3. **API Security**
   - Secure endpoints
   - Data validation
   - Error message sanitization
   - Chat session management

This system provides an automated, intelligent solution for managing loan transfers when officers are out of office, ensuring business continuity while maintaining data integrity and security. The AI-powered chatbot makes the system more accessible and user-friendly, allowing users to interact with the system using natural language. 