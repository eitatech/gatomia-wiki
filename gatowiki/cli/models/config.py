"""
Configuration data models for GatoWiki CLI.

This module contains the Configuration class which represents persistent
user settings stored in ~/.gatowiki/config.json. These settings are converted
to the backend Config class when running documentation generation.
"""

from dataclasses import dataclass, asdict
from typing import Optional
from pathlib import Path


@dataclass
class Configuration:
    """
    GatoWiki configuration data model.
    
    Note: LLM configuration removed - all LLM interactions happen through
    GitHub Copilot Chat interface, not via API calls from Python code.
    
    Attributes:
        default_output: Default output directory
    """
    default_output: str = "docs"
    
    def validate(self):
        """
        Validate all configuration fields.
        
        Raises:
            ConfigurationError: If validation fails
        """
        # Only validate that default_output is a valid path string
        if not isinstance(self.default_output, str) or not self.default_output:
            from gatowiki.cli.utils.errors import ConfigurationError
            raise ConfigurationError("default_output must be a non-empty string")
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Configuration':
        """
        Create Configuration from dictionary.
        
        Args:
            data: Configuration dictionary
            
        Returns:
            Configuration instance
        """
        return cls(
            default_output=data.get('default_output', 'docs'),
        )
    
    def is_complete(self) -> bool:
        """Check if all required fields are set."""
        return bool(self.default_output)
    
    def to_backend_config(self, repo_path: str, output_dir: str):
        """
        Convert CLI Configuration to Backend Config.
        
        This method bridges the gap between persistent user settings (CLI Configuration)
        and runtime job configuration (Backend Config).
        
        Args:
            repo_path: Path to the repository to document
            output_dir: Output directory for generated documentation
            
        Returns:
            Backend Config instance ready for code analysis
        """
        from gatowiki.src.config import Config
        
        return Config.from_cli(
            repo_path=repo_path,
            output_dir=output_dir
        )

