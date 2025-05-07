# End-to-End Flow: Loan Transfer Scenario

## Scenario: Transferring Loans from User ALEX to User BRIAN

### 1. User Interface (Frontend)
```
User types: "Transfer loans from ALEX to BRIAN"
```

### 2. Frontend to AI Service Flow
1. Frontend sends request to AI service endpoint
2. Request includes:
   - Natural language query
   - Session information
   - Authentication token

### 3. AI Service Processing

#### A. Agent Initialization
```python
# 1. Agent receives the request
agent_executor = AgentExecutor(
    agent=agent,
    tools=[transfer_loan, get_user_count, check_user_ooo, check_user_loans, set_user_ooo],
    verbose=True
)

# 2. GPT-3.5-turbo-1106 processes the request
# System message guides the model to:
# - Understand this is a loan transfer request
# - Identify source (ALEX) and destination (BRIAN) users
# - Follow the transfer rules
```

#### B. Tool Selection and Execution
```python
# 1. Agent selects TransferLoanTool
class TransferLoanTool(BaseTool):
    name = "transfer_loan"
    description = """Transfer loans between users..."""

# 2. Tool extracts usernames using LLM
extraction_prompt = f"""Extract the source and destination usernames..."""
extraction_result = llm.invoke(extraction_prompt)
# Result: {"fromUsername": "alex", "toUsername": "brian"}
```

#### C. Validation Steps
```python
# 1. Check if ALEX has loans
loans_check = check_user_loans._run("Check if alex has loans")
# API Call: GET /api/loans/username/alex/has-loans
# Response: {"hasLoans": true, "loanCount": 2}

# 2. Check if ALEX is OOO
ooo_check = check_user_ooo._run("Check if alex is OOO")
# API Call: GET /api/users/username/alex
# Response: {"oooStatus": true}
```

#### D. Loan Transfer Execution
```python
# 1. Prepare transfer request
payload = {
    "fromUsername": "alex",
    "toUsername": "brian"
}

# 2. Execute transfer
response = requests.post(
    LOAN_TRANSFER_API_URL,
    json=payload,
    headers={"Content-Type": "application/json"}
)
# API Call: POST /api/loans/transfer
```

### 4. Backend Processing

#### A. Loan Transfer API
1. Receives transfer request
2. Validates:
   - User existence
   - OOO status
   - Loan ownership
3. Executes transfer in database
4. Updates loan ownership records

#### B. Database Operations
1. Begin transaction
2. Update loan records
3. Update user statistics
4. Commit transaction

### 5. Response Flow

#### A. Backend to AI Service
```python
# 1. Backend returns success response
response = {
    "success": true,
    "message": "Loans transferred successfully",
    "transferDetails": {
        "fromUsername": "alex",
        "toUsername": "brian",
        "loanCount": 2
    }
}

# 2. AI Service formats response
return f"Successfully transferred 2 loans from ALEX to BRIAN"
```

#### B. AI Service to Frontend
1. Sends formatted response
2. Includes:
   - Success message
   - Transfer details
   - Any relevant warnings

#### C. Frontend to User
1. Displays success message
2. Updates UI to reflect changes
3. Shows transfer confirmation

### 6. Error Handling Scenarios

#### A. User Not OOO
```python
# If ALEX is not OOO
if "is not Out of Office" in ooo_check:
    return f"I'm sorry, but I cannot proceed with the loan transfer from ALEX to BRIAN because ALEX is not Out of Office."
```

#### B. No Loans to Transfer
```python
# If ALEX has no loans
if "has no loans" in loans_check:
    return f"Cannot transfer loans: User 'ALEX' has no loans to transfer."
```

#### C. User Doesn't Exist
```python
# If user doesn't exist
if response.status_code == 404:
    return f"User 'ALEX' does not exist in the system."
```

### 7. Logging and Monitoring

#### A. AI Service Logs
```python
logger.info("Processing loan transfer request")
logger.debug(f"Extracted usernames: {from_username} -> {to_username}")
logger.info(f"Transfer result: {response.text}")
```

#### B. Backend Logs
1. API request logs
2. Database operation logs
3. Performance metrics

### 8. Security Measures

#### A. Input Validation
1. Username sanitization
2. Request validation
3. Authentication checks

#### B. Data Protection
1. Secure API communication
2. Sensitive data handling
3. Error message sanitization 