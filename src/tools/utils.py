import logging
import yaml
from pathlib import Path
from typing import Dict, Any
import os

class ConfigManager:
    """Manages configuration loading and validation for Lisa-AI."""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.agents_config = None
        self.tasks_config = None
        
    def load_config(self) -> None:
        """Load all configuration files."""
        try:
            with open(self.config_dir / "agents.yaml", "r") as f:
                self.agents_config = yaml.safe_load(f)
            with open(self.config_dir / "tasks.yaml", "r") as f:
                self.tasks_config = yaml.safe_load(f)
        except FileNotFoundError as e:
            logging.error(f"Configuration file not found: {e}")
            raise
        except yaml.YAMLError as e:
            logging.error(f"Error parsing YAML configuration: {e}")
            raise

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """Retrieve configuration for a specific agent."""
        if not self.agents_config:
            self.load_config()
        return self.agents_config.get(agent_name, {})

    def get_task_config(self, task_name: str) -> Dict[str, Any]:
        """Retrieve configuration for a specific task."""
        if not self.tasks_config:
            self.load_config()
        return self.tasks_config.get(task_name, {})

def setup_logging(
    level: int = logging.INFO,
    log_file: str = "lisa-ai.log"
) -> None:
    """Configure logging with both file and console handlers."""
    log_format = "%(asctime)s [%(levelname)s] %(message)s"
    
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(level=level, format=log_format)
    
    # Add file handler
    file_handler = logging.FileHandler(log_dir / log_file)
    file_handler.setFormatter(logging.Formatter(log_format))
    logging.getLogger().addHandler(file_handler)

def clear_session() -> None:
    """Clear temporary session data and reset state."""
    logging.info("Clearing session data...")
    try:
        # Clear temporary files
        temp_dir = Path("tmp")
        if temp_dir.exists():
            for file in temp_dir.glob("*"):
                try:
                    file.unlink()
                except Exception as e:
                    logging.warning(f"Failed to delete {file}: {e}")
        
        # Reset session state
        logging.info("Session data cleared successfully")
    except Exception as e:
        logging.error(f"Error clearing session: {e}")
        raise

def validate_file_path(file_path: str) -> bool:
    """Validate if a file path exists and is accessible."""
    path = Path(file_path)
    return path.exists() and path.is_file()

def get_llm_config(provider="ollama"):
    """
    Return LLM configuration based on the selected provider.
    """
    if provider == "ollama":
        return {
            "llm": {
                "provider": "ollama",
                "config": {
                    "model": "phi3.5",  # Updated to use phi3.5
                    "temperature": 0.3,  # Lower temperature for more focused analysis
                    "top_p": 0.9,       # Slightly constrained sampling for professional output
                    "num_ctx": 4096     # Context window for handling longer documents
                }
            },
            "embedder": {
                "provider": "ollama",
                "config": {
                    "model": "phi3.5"   # Using same model for consistency
                }
            }
        }
    elif provider == "openai":
        return {
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4",
                    "temperature": 0.7
                }
            },
            "embedder": {
                "provider": "openai",
                "config": {
                    "model": "text-embedding-ada-002"
                }
            }
        }
    else:
        raise ValueError("Unsupported LLM provider. Choose 'ollama' or 'openai'.")

# Initialize logging when module is imported
setup_logging() 