#!/usr/bin/env python
import logging
from pathlib import Path
from crew import LisaAICrew

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('src/logs/lisa-ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_directories():
    """Create necessary directories if they don't exist."""
    logger.debug("Creating output directory...")
    Path("output").mkdir(exist_ok=True)
    Path("src/logs").mkdir(exist_ok=True, parents=True)

def run():
    """Run the LisaAI crew to analyze PDF document."""
    try:
        logger.debug("Starting LisaAI analysis...")
        
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        
        # Create necessary directories
        setup_directories()
        
        # Define PDF path
        pdf_path = str(project_root / "data/sample.pdf")
        logger.debug(f"PDF path: {pdf_path}")
        
        # Create and run crew
        logger.debug("Creating crew...")
        crew = LisaAICrew().create_crew(pdf_path)
        
        logger.debug("Running crew analysis...")
        results = crew.kickoff()
        
        # Print results
        print("\nAnalysis Results:")
        print(results)
        
    except Exception as e:
        logger.error(f"Error running analysis: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    run()
