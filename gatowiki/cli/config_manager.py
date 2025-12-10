"""
Configuration manager for GatoWiki settings.

Note: API key storage removed - all LLM interactions happen through
GitHub Copilot Chat interface, not via API calls from Python code.
"""

import json
from pathlib import Path
from typing import Optional

from gatowiki.cli.models.config import Configuration
from gatowiki.cli.utils.errors import ConfigurationError, FileSystemError
from gatowiki.cli.utils.fs import ensure_directory, safe_write, safe_read


# Configuration file location
CONFIG_DIR = Path.home() / ".gatowiki"
CONFIG_FILE = CONFIG_DIR / "config.json"
CONFIG_VERSION = "2.0"  # Bumped version for GitHub Copilot integration


class ConfigManager:
    """
    Manages GatoWiki configuration.
    
    Storage:
        - Settings: ~/.gatowiki/config.json
    
    Note: No API keys stored - GitHub Copilot handles all LLM interactions.
    """
    
    def __init__(self):
        """Initialize the configuration manager."""
        self._config: Optional[Configuration] = None
    
    def load(self) -> bool:
        """
        Load configuration from file.
        
        Returns:
            True if configuration exists, False otherwise
        """
        # Load from JSON file
        if not CONFIG_FILE.exists():
            return False
        
        try:
            content = safe_read(CONFIG_FILE)
            data = json.loads(content)
            
            # Validate version (allow migration from v1.0)
            version = data.get('version', '1.0')
            if version not in ['1.0', '2.0']:
                # Unknown version, but try to load anyway
                pass
            
            self._config = Configuration.from_dict(data)
            
            return True
        except (json.JSONDecodeError, FileSystemError) as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")
    
    def save(
        self, 
        default_output: Optional[str] = None
    ):
        """
        Save configuration to file.
        
        Args:
            default_output: Default output directory
        """
        # Ensure config directory exists
        try:
            ensure_directory(CONFIG_DIR)
        except FileSystemError as e:
            raise ConfigurationError(f"Cannot create config directory: {e}")
        
        # Load existing config or create new
        if self._config is None:
            if CONFIG_FILE.exists():
                self.load()
            else:
                self._config = Configuration(
                    default_output="docs"
                )
        
        # Update fields if provided
        if default_output is not None:
            self._config.default_output = default_output
        
        # Validate configuration
        self._config.validate()
        
        # Save config to JSON
        config_data = {
            "version": CONFIG_VERSION,
            **self._config.to_dict()
        }
        
        try:
            safe_write(CONFIG_FILE, json.dumps(config_data, indent=2))
        except FileSystemError as e:
            raise ConfigurationError(f"Failed to save configuration: {e}")
    
    def get_config(self) -> Optional[Configuration]:
        """
        Get current configuration.
        
        Returns:
            Configuration object or None if not loaded
        """
        return self._config
    
    def is_configured(self) -> bool:
        """
        Check if configuration is complete and valid.
        
        Returns:
            True if configured, False otherwise
        """
        if self._config is None:
            return False
        
        # Check if config is complete
        return self._config.is_complete()
    
    def clear(self):
        """Clear all configuration."""
        # Delete config file
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
        
        self._config = None
    
    @property
    def config_file_path(self) -> Path:
        """Get configuration file path."""
        return CONFIG_FILE

