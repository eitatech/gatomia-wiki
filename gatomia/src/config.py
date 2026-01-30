from dataclasses import dataclass
import argparse
import os
import sys
from dotenv import load_dotenv
load_dotenv()

# Constants
OUTPUT_BASE_DIR = 'output'
DEPENDENCY_GRAPHS_DIR = 'dependency_graphs'
DOCS_DIR = 'docs'
FIRST_MODULE_TREE_FILENAME = 'first_module_tree.json'
MODULE_TREE_FILENAME = 'module_tree.json'
OVERVIEW_FILENAME = 'overview.md'
MAX_DEPTH = 2
MAX_TOKEN_PER_MODULE = 36_369
MAX_TOKEN_PER_LEAF_MODULE = 16_000

# CLI context detection
_CLI_CONTEXT = False

def set_cli_context(enabled: bool = True):
    """Set whether we're running in CLI context (vs web app)."""
    global _CLI_CONTEXT
    _CLI_CONTEXT = enabled

def is_cli_context() -> bool:
    """Check if running in CLI context."""
    return _CLI_CONTEXT

@dataclass
class Config:
    """
    Configuration class for GatoWiki.
    
    Note: LLM configuration removed - all LLM interactions happen through
    GitHub Copilot Chat interface, not via API calls from Python code.
    """
    repo_path: str
    output_dir: str
    dependency_graph_dir: str
    docs_dir: str
    max_depth: int
    
    @classmethod
    def from_args(cls, args: argparse.Namespace) -> 'Config':
        """Create configuration from parsed arguments."""
        repo_name = os.path.basename(os.path.normpath(args.repo_path))
        sanitized_repo_name = ''.join(c if c.isalnum() else '_' for c in repo_name)
        
        return cls(
            repo_path=args.repo_path,
            output_dir=OUTPUT_BASE_DIR,
            dependency_graph_dir=os.path.join(OUTPUT_BASE_DIR, DEPENDENCY_GRAPHS_DIR),
            docs_dir=os.path.join(OUTPUT_BASE_DIR, DOCS_DIR, f"{sanitized_repo_name}-docs"),
            max_depth=MAX_DEPTH
        )
    
    @classmethod
    def from_cli(
        cls,
        repo_path: str,
        output_dir: str
    ) -> 'Config':
        """
        Create configuration for CLI context.
        
        Args:
            repo_path: Repository path
            output_dir: Output directory for generated docs
            
        Returns:
            Config instance
        """
        repo_name = os.path.basename(os.path.normpath(repo_path))
        base_output_dir = os.path.join(output_dir, "temp")
        
        return cls(
            repo_path=repo_path,
            output_dir=base_output_dir,
            dependency_graph_dir=os.path.join(base_output_dir, DEPENDENCY_GRAPHS_DIR),
            docs_dir=output_dir,
            max_depth=MAX_DEPTH
        )