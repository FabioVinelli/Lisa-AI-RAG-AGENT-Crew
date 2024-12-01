from crewai import Agent, Task, Crew, Process
from langchain_openai import OpenAI
from src.tools.pdf_tool import PDFSearchTool
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LisaAICrew:
    """Crew for analyzing student documents and generating reports."""

    def __init__(self):
        self.llm = OpenAI(
            temperature=0.7,
            model="gpt-4",
            api_key=os.getenv("OPENAI_API_KEY"),
            max_tokens=4096
        )
        
        # Load report template structure
        template_path = os.path.join(os.path.dirname(__file__), '../templates/report_template.json')
        with open(template_path) as f:
            self.template = json.load(f)

    def create_crew(self, pdf_path: str, query: str = None) -> Crew:
        """Create a crew focused on document analysis and Q&A."""
        
        # Create document analysis agent with enhanced prompting
        analysis_agent = Agent(
            role="Educational Document Analyzer",
            goal="Extract and analyze student information for psychoeducational reports",
            backstory="""You are an expert in analyzing educational documents and creating 
            psychoeducational reports. You understand the importance of accurate data extraction
            and proper interpretation of student information. You are familiar with educational
            standards and report requirements. You communicate in a clear, natural way that is
            easy for parents and educators to understand.""",
            tools=[PDFSearchTool(pdf_path=pdf_path)],
            llm=self.llm,
            verbose=True,
            allow_delegation=True
        )

        # Create task with natural language output format
        task = Task(
            description=f"""Analyze the document and respond to the query: "{query if query else 'Provide a complete summary'}"

            When responding:
            1. Use natural, professional language
            2. Be concise but thorough
            3. Include relevant details and context
            4. Maintain a supportive, educational tone
            5. Format the response in clear paragraphs
            
            If no specific query is provided, structure the response to cover:
            1. Student's basic information
            2. Reason for referral
            3. Background information
            4. Assessment results
            5. Recommendations

            Additional Guidelines:
            - Focus on clarity and readability
            - Avoid technical jargon unless necessary
            - Provide context for any technical terms used
            - Include specific examples when relevant
            - Maintain a professional, supportive tone
            - Ensure complete responses without truncation
            - Use detailed examples and evidence from the document""",
            expected_output="""A comprehensive, well-structured response that fully addresses the query 
            or provides a detailed summary. The response should be complete, clear, and professional, 
            incorporating all relevant information from the document without truncation.""",
            agent=analysis_agent,
            context_length=4000
        )

        # Create and return crew
        return Crew(
            agents=[analysis_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )