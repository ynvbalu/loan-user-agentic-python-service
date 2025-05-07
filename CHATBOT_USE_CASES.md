# Chatbot Use Cases and Prompts

## 1. User Information Queries
```
1. "How many users are there?"
2. "What's the total number of users?"
3. "Get me the user count"
4. "Count of users"
```

## 2. OOO Status Checks
```
1. "Is ALEX out of office?"
2. "Check if ALEX is OOO"
3. "Is ALEX available?"
4. "Get OOO status for ALEX"
5. "What's ALEX's availability status?"
```

## 3. Loan Verification
```
1. "Does ALEX have any loans?"
2. "Check if ALEX has loans"
3. "How many loans does ALEX have?"
4. "Get loan count for ALEX"
5. "Show me ALEX's loans"
```

## 4. Loan Transfer Scenarios

### A. Basic Transfers
```
1. "Transfer loans from ALEX to BRIAN"
2. "Move ALEX's loans to BRIAN"
3. "Send funds from ALEX to BRIAN"
4. "Give ALEX's loans to BRIAN"
```

### B. Specific Loan Transfers
```
1. "Transfer loan ID 123 from ALEX to BRIAN"
2. "Move loan number 456 from ALEX to BRIAN"
3. "Transfer these loans from ALEX to BRIAN: 123, 456, 789"
```

## 5. OOO Status Management
```
1. "Set ALEX as OOO"
2. "Mark ALEX as out of office"
3. "Update ALEX's OOO status to true"
4. "Change ALEX's availability to out of office"
5. "Remove ALEX's OOO status"
6. "Set ALEX as available"
```

## 6. Error Scenarios

### A. User Not OOO
```
1. "Transfer loans from ALEX to BRIAN" (when ALEX is not OOO)
2. "Move ALEX's loans to BRIAN" (when ALEX is not OOO)
```

### B. No Loans to Transfer
```
1. "Transfer loans from ALEX to BRIAN" (when ALEX has no loans)
2. "Move ALEX's loans to BRIAN" (when ALEX has no loans)
```

### C. User Doesn't Exist
```
1. "Transfer loans from NONEXISTENT to BRIAN"
2. "Check if NONEXISTENT is OOO"
3. "Get loan count for NONEXISTENT"
```

### D. Invalid Transfers
```
1. "Transfer loans from ALEX to ALEX"
2. "Move loans from BRIAN to BRIAN"
```

## 7. Combined Queries
```
1. "Is ALEX OOO and does they have any loans?"
2. "Check if ALEX is OOO and transfer their loans to BRIAN if they are"
3. "How many users are there and who is OOO?"
```

## 8. Clarification Requests
```
1. "Which user's loans do you want to transfer?"
2. "Please specify the source and destination users"
3. "I need more information about the transfer"
```

## 9. Status Updates
```
1. "What's the status of the transfer?"
2. "Did the transfer complete successfully?"
3. "Show me the transfer details"
```

## 10. Help and Guidance
```
1. "What can you help me with?"
2. "Show me available commands"
3. "How do I transfer loans?"
4. "What are the rules for loan transfers?"
```

## Testing Sequence
1. Start with basic user information
2. Check OOO status
3. Verify loan existence
4. Attempt transfer
5. Check transfer status
6. Try error scenarios
7. Test combined queries
8. Verify help functionality

## Expected Responses
1. User Information: "There are X users in the system"
2. OOO Status: "User X is Out of Office" or "User X is in office"
3. Loan Check: "User X has Y loan(s)" or "User X has no loans"
4. Transfer Success: "Successfully transferred Y loans from X to Z"
5. Transfer Error: "Cannot proceed: [specific reason]"
6. Help: List of available commands and rules 