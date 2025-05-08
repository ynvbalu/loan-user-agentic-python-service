# Loan Management System - 2-Minute Demo Script

## Introduction (15 seconds)
"Today, I'll demonstrate our AI-powered loan management system that automatically handles loan transfers when officers go Out of Office. The system uses natural language processing to make this process seamless and efficient."

## Technology Overview (30 seconds)
"Our system is built with:
- Frontend: React and TypeScript for a modern UI
- Backend: Spring Boot for robust API handling
- AI Service: Python with LangChain and GPT-3.5-turbo-1106
- Database: H2 for data persistence for POC"

## Demo Flow (45 seconds)

### 1. Show Chatbot Interface
"Let's look at our AI chatbot interface. Here, users can interact naturally with the system."

### 2. Demonstrate Loan Transfer
"Let's transfer loans from ALEX to BRIAN:
1. Type: 'Transfer loans from ALEX to BRIAN'
2. Watch the AI:
   - Check ALEX's OOO status
   - Verify loan ownership
   - Execute the transfer
3. See the confirmation message"

### 3. Show Key Components
"Behind this simple interaction, our system uses:
- AI Agent for decision making
- Tools for:
  - OOO status verification
  - Loan transfer validation
  - User information retrieval"

## Conclusion (30 seconds)
"This system demonstrates how AI can streamline complex business processes. The natural language interface makes it user-friendly, while the robust backend ensures data integrity and security."

## Demo Checklist
- [ ] Open the application
- [ ] Show the chatbot interface
- [ ] Demonstrate a loan transfer
- [ ] Show the confirmation
- [ ] Highlight the technologies used

## Key Points to Remember
1. Keep the demo focused on the main flow
2. Emphasize the natural language interaction
3. Highlight the AI capabilities
4. Show the real-time response
5. Mention the security aspects

## Technical Details (For Reference)

### AI Agent Code
```python
def create_agent():
    system_message = """You are a helpful assistant that helps with loan transfers.
    You can understand natural language requests for:
    1. Transferring loans between users
    2. Checking OOO status
    3. Validating transfers"""
    
    agent = OpenAIFunctionsAgent(
        llm=llm,
        tools=[transfer_loan, check_user_ooo, check_user_loans],
        prompt=chat_prompt
    )
```

### Key Tools
```python
@api_tool("Transfer loans between users")
def transfer_loan(self, from_username: str, to_username: str):
    # Check OOO status
    source_user = self.check_user_ooo(from_username)
    if not source_user.ooo_status:
        return "Cannot transfer: User is not OOO"
    
    # Execute transfer
    return "Transfer successful"
```

## Demo Tips
1. Have the application ready before starting
2. Use a pre-configured test case
3. Keep the explanation concise
4. Focus on the user experience
5. Be ready to answer questions about the technology stack 