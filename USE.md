## Usecase:
## When given user is OOO, ask agent transfer loans to available user with chatbot.

## AI-powered system uses GPT-3.5 with LangChain framework to provide 
## a natural language interface through chatbot for loan assignment operations.

## Key AI Components:
┌─────────────────────────────────────────────────────────────────────┐
│ 1. GPT-3.5                                                          │
│    - Natural language understanding                                 │
│    - Intent recognition                                             │
│                                                                     │
│ 2. LangChain OpenAIFunctionsAgent                                   │
│    - Tool orchestration                                             │
│    - Business rule enforcement                                      │
└─────────────────────────────────────────────────────────────────────┘

# Flow Diagram
```
[User Interface(REACT]                [Agentic AI Service(Python)]      [Backend(Java) for APIs]
     |                                 |                                |
     |  "Transfer loans from           |                                |
     |   ALEX to BRIAN"                |                                |
     |----------------------------->   |                                |
     |                                 |                                |
     |                                 |  1. Agent Initialization       |
     |                                 |     - GPT-3.5 processes        |
     |                                 |     - Identifies intent        |
     |                                 |                                |
     |                                 |  2. Tool Selection             |
     |                                 |     - TransferLoanTool         |
     |                                 |     - Extracts usernames       |
     |                                 |                                |
     |                                 |  3. Validation Steps           |
     |                                 |     - Check ALEX's loans       |
     |                                 |     - Check OOO status         |
     |                                 |                                |
     |                                 |  4. Execute Transfer           |
     |                                 |----------------------------->  |
     |                                 |                                |
     |                                 |                                |  5. Backend Processing
     |                                 |                                |     - Validate users
     |                                 |                                |     - Update database
     |                                 |                                |
     |                                 |  6. Success Response           |
     |                                 |<------------------------------ |
     |                                 |                                |
     |  7. "Successfully transferred   |                                |
     |     2 loans from ALEX to BRIAN" |                                |
     |<-----------------------------   |                                |
     |                                 |                                |



Error Scenarios:
┌─────────────────────────────────────────────────────────────────────┐
│ 1. User Not OOO:                                                    │
│    "Cannot proceed: ALEX is not Out of Office"                      │
│                                                                     │
│ 2. No Loans:                                                        │
│    "Cannot transfer: ALEX has no loans"                             │
│                                                                     │
│ 3. User Not Found:                                                  │
│    "User 'ALEX' does not exist"                                     │
└─────────────────────────────────────────────────────────────────────┘





``` 