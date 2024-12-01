from crewai_tools import PDFSearchTool as BasePDFSearchTool
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PDFSearchTool(BasePDFSearchTool):
    """Tool for processing and extracting data from PDF files."""
    
    def __init__(self, pdf_path=None):
        """Initialize the PDF search tool with the given file path."""
        super().__init__(
            pdf=pdf_path,
            config={
                "llm": {
                    "provider": "openai",
                    "config": {
                        "model": "gpt-4",
                        "temperature": 0.7,
                        "api_key": os.getenv("OPENAI_API_KEY")
                    }
                },
                "embedder": {
                    "provider": "openai",
                    "config": {
                        "model": "text-embedding-ada-002",
                        "api_key": os.getenv("OPENAI_API_KEY")
                    }
                }
            }
        )