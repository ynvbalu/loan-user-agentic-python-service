# Loan Management System - Demo Script (2 Minutes)

## Introduction (15 seconds)
"Today, I'll demonstrate our AI-powered Loan Management System that uses GPT-3.5-turbo-1106 with LangChain to provide a natural language interface for loan operations. The system can handle loan transfers, user information, and OOO status management through simple conversation."

## Technology Overview (30 seconds)
"The system combines:
- GPT-3.5-turbo-1106 for natural language understanding
- LangChain's OpenAIFunctionsAgent for structured tool execution
- Five custom tools for specific operations:
  1. Loan transfers
  2. User count
  3. OOO status checks
  4. Loan verification
  5. OOO status updates"

## Demo Flow (45 seconds)

### 1. User Information Check (15 seconds)
"Let's start by checking how many users we have in the system."
```
User: "How many users are there?"
System: "There are 150 users in the system."
```

### 2. OOO Status Check (15 seconds)
"Now, let's check if a user is out of office."
```
User: "Is ALEX out of office?"
System: "User ALEX is Out of Office."
```

### 3. Loan Transfer (15 seconds)
"Let's transfer ALEX's loans to BRIAN."
```
User: "Transfer loans from ALEX to BRIAN"
System: "Successfully transferred 2 loans from ALEX to BRIAN."
```

## Key Points to Remember
1. Natural language understanding
2. Business rule enforcement
3. Error handling
4. User-friendly responses

## Technical Details
- Agent: OpenAIFunctionsAgent with GPT-3.5-turbo-1106
- Tools: Custom API tools for loan management
- Validation: OOO status and loan ownership checks
- Security: Input validation and error handling

## Demo Tips
1. Speak clearly and at a moderate pace
2. Highlight the natural language understanding
3. Emphasize the business rule enforcement
4. Show error handling if time permits

## Conclusion (30 seconds)
"This system demonstrates how AI can be used to create a user-friendly interface for complex loan management operations. The combination of GPT-3.5-turbo-1106 and LangChain provides a powerful yet safe way to handle sensitive financial operations through natural language."

## Demo Checklist
- [ ] Introduction
- [ ] Technology overview
- [ ] User count check
- [ ] OOO status check
- [ ] Loan transfer
- [ ] Conclusion

## Time Management
- 0:00 - 0:15: Introduction
- 0:15 - 0:45: Technology Overview
- 0:45 - 1:30: Demo Flow
- 1:30 - 2:00: Conclusion

## Backup Scenarios
If time permits, demonstrate:
1. Error handling (user not OOO)
2. No loans to transfer
3. User doesn't exist 