from setuptools import setup, find_packages

setup(
    name="lisa-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.28.0",
        "crewai[tools]>=0.1.0",
        "python-dotenv>=1.0.0",
        "langchain-openai>=0.0.2",
        "openai>=1.3.0",
    ],
) 