import logging
from pathlib import Path
from typing import Dict, Any, Optional
from docx import Document
from langchain.tools import BaseTool
from pydantic import Field, BaseModel
from langchain_openai import OpenAI, OpenAIEmbeddings
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DOCXSearchTool(BaseTool):
    """Tool for processing and extracting data from DOCX files using RAG."""
    
    name: str = "docx_tool"
    description: str = "Process and extract data from DOCX documents"
    llm: Any = Field(default=None)
    embedder: Any = Field(default=None)
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__()
        self.llm = OpenAI(
            temperature=0.7,
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.embedder = OpenAIEmbeddings(
            api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def _run(self, docx_path: str, query: str) -> Dict[str, Any]:
        """Run the DOCX processing tool."""
        try:
            # Extract text from DOCX
            doc = Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            # Process query using RAG
            from langchain.text_splitter import RecursiveCharacterTextSplitter
            from langchain.vectorstores import FAISS
            from langchain.chains import RetrievalQA
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            chunks = text_splitter.split_text(text)
            
            # Create vector store
            vectorstore = FAISS.from_texts(
                chunks,
                self.embedder
            )
            
            # Create retrieval chain
            qa_chain = RetrievalQA.from_chain_type(
                llm=self.llm,
                chain_type="stuff",
                retriever=vectorstore.as_retriever()
            )
            
            # Execute query
            result = qa_chain.run(query)
            return {"response": result}
            
        except Exception as e:
            raise ValueError(f"Error processing DOCX: {str(e)}")
    
    async def _arun(self, *args, **kwargs) -> Dict[str, Any]:
        """Run the tool asynchronously."""
        raise NotImplementedError("Async version not implemented")