# Loan User Agentic Python Service

A FastAPI-based service that uses LangChain and OpenAI to provide natural language processing capabilities for loan transfer operations.

## Features

- Natural language processing for loan transfers
- User count information
- RESTful API endpoints
- OpenAI GPT-3.5 integration
- Comprehensive error handling and logging

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd loan-user-agentic-python-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file with your OpenAI API key:
```
OPENAI_API_KEY=your-api-key-here
```

## Usage

1. Start the service:
```bash
python src/main.py
```

2. The service will be available at `http://localhost:8000`

3. Available endpoints:
   - POST `/process`: Process natural language requests
     ```bash
     curl -X POST "http://localhost:8000/process" \
          -H "Content-Type: application/json" \
          -d '{"text": "Transfer loans from user1 to user2"}'
     ```

## Project Structure

```
loan-user-agentic-python-service/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── models.py
│   │   └── tools.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py
│   └── utils/
│       └── __init__.py
├── requirements.txt
├── setup.py
└── README.md
```

## Development

- The service uses FastAPI for the web framework
- LangChain for agent-based processing
- OpenAI's GPT-3.5 for natural language understanding
- Pydantic for data validation
- httpx for async HTTP requests

## License

[Your chosen license] 