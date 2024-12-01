import os
import streamlit as st
from dotenv import load_dotenv
from src.crew import LisaAICrew
import tempfile
import uuid
import json
from datetime import datetime

# Load environment variables
load_dotenv()

def init_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'temp_file_path' not in st.session_state:
        st.session_state.temp_file_path = None
    if 'report_data' not in st.session_state:
        st.session_state.report_data = None

def process_uploaded_file(uploaded_file):
    """Process uploaded file and return path"""
    if uploaded_file is not None:
        # Create a temporary file
        temp_dir = tempfile.mkdtemp()
        temp_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save uploaded file to temporary location
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return temp_path
    return None

def format_report_section(result):
    """Extract the natural language content from CrewOutput"""
    if hasattr(result, 'raw'):
        return result.raw
    return str(result)

def generate_report(crew, pdf_path):
    """Generate a comprehensive report using the master template"""
    try:
        # Generate Reason for Referral section
        referral_query = """Analyze the document and provide information for the Reason for Referral section, including:
        1. Referral source and type (initial/triennial)
        2. Primary concerns and reasons
        3. Parent and teacher input
        4. Current academic performance
        5. Medical diagnosis and current services
        6. Previous assessments
        7. Suspected areas of disability"""
        
        referral_result = crew.create_crew(pdf_path, query=referral_query).kickoff()
        
        # Generate Background Information section
        background_query = """Analyze the document and provide information for the Background Information section, including:
        1. Family information and structure
        2. Language proficiency and preferences
        3. After-school activities and interests
        4. Social-emotional-behavioral history
        5. Parent-reported behaviors and sensitivities"""
        
        background_result = crew.create_crew(pdf_path, query=background_query).kickoff()
        
        # Format the report in natural language
        report = f"""
        # Comprehensive Student Report
        Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        
        ## Reason for Referral
        {format_report_section(referral_result)}
        
        ## Background Information
        {format_report_section(background_result)}
        """
        
        return report
        
    except Exception as e:
        raise Exception(f"Error generating report: {str(e)}")

def main():
    # Display logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("assets/lisa-ai-logo.png", width=100)
    with col2:
        st.title("LISA AI - Student Report Assistant")
        st.markdown("*Powered by CrewAI and OpenAI*")
    
    init_session_state()
    
    # Session management
    col1, col2, col3 = st.columns([2,1,1])
    with col1:
        if st.button("Start New Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.messages = []
            st.session_state.temp_file_path = None
            st.session_state.report_data = None
            st.success(f"Session started: {st.session_state.session_id}")
    
    with col2:
        if st.session_state.session_id and st.button("Generate Report"):
            try:
                with st.spinner("Generating comprehensive report..."):
                    crew = LisaAICrew()
                    report = generate_report(crew, st.session_state.temp_file_path)
                    st.session_state.report_data = report
                    
                    # Save report to file
                    report_dir = "reports"
                    os.makedirs(report_dir, exist_ok=True)
                    report_path = os.path.join(report_dir, f"report_{st.session_state.session_id}.md")
                    with open(report_path, 'w') as f:
                        f.write(report)
                    
                    st.success(f"Report generated and saved to {report_path}")
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    
    with col3:
        if st.session_state.session_id and st.button("End Session"):
            try:
                # Cleanup temporary files if they exist
                if st.session_state.temp_file_path and os.path.exists(st.session_state.temp_file_path):
                    os.remove(st.session_state.temp_file_path)
                st.session_state.messages = []
                st.session_state.session_id = None
                st.session_state.temp_file_path = None
                st.session_state.report_data = None
                st.success("Session ended successfully.")
            except Exception as e:
                st.error(f"Error ending session: {str(e)}")
    
    if not st.session_state.session_id:
        st.info("Please start a new session")
        return
        
    st.write(f"Current Session: {st.session_state.session_id}")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload Student Documentation",
        type=['pdf']
    )
    
    # Process uploaded file
    if uploaded_file:
        try:
            with st.spinner("Processing document..."):
                file_path = process_uploaded_file(uploaded_file)
                if file_path:
                    st.session_state.temp_file_path = file_path
                    st.success("Document processed successfully")
        except Exception as e:
            st.error(f"Error processing document: {str(e)}")
            return
    
    # Show chat interface only if document is processed
    if st.session_state.temp_file_path:
        # Display chat history
        st.subheader("Chat with LISA AI")
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask about the student:"):
            st.chat_message("user").markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            with st.chat_message("assistant"):
                try:
                    # Create crew and process the query
                    crew = LisaAICrew().create_crew(
                        st.session_state.temp_file_path,
                        query=prompt
                    )
                    result = crew.kickoff()
                    
                    if result:
                        st.markdown(result)
                        st.session_state.messages.append(
                            {"role": "assistant", "content": result}
                        )
                    else:
                        st.error("Could not generate a response")
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        # Display report if generated
        if st.session_state.report_data:
            st.subheader("Generated Report")
            st.markdown(st.session_state.report_data)

if __name__ == "__main__":
    main() 