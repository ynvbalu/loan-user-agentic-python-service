from setuptools import setup, find_packages

setup(
    name="loan-user-agentic-python-service",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "langchain",
        "langchain-openai",
        "python-dotenv",
        "httpx",
        "pydantic"
    ],
    python_requires=">=3.8",
) 