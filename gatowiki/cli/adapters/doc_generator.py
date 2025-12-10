"""
CLI adapter for documentation generator backend.

This adapter wraps the existing backend documentation_generator.py
and provides CLI-specific functionality like progress reporting.
"""

from pathlib import Path
from typing import Dict, Any
import time
import asyncio
import os
import logging
import sys


from gatowiki.cli.utils.progress import ProgressTracker
from gatowiki.cli.models.job import DocumentationJob, LLMConfig
from gatowiki.cli.utils.errors import APIError

# Import backend modules
from gatowiki.src.be.documentation_generator import DocumentationGenerator
from gatowiki.src.config import Config as BackendConfig, set_cli_context


class CLIDocumentationGenerator:
    """
    CLI adapter for documentation generation with progress reporting.
    
    This class wraps the backend documentation generator and adds
    CLI-specific features like progress tracking and error handling.
    """
    
    def __init__(
        self,
        repo_path: Path,
        output_dir: Path,
        config: Dict[str, Any],
        verbose: bool = False,
        generate_html: bool = False
    ):
        """
        Initialize the CLI code analysis generator.
        
        Note: This now only performs code analysis. Documentation generation
        is handled by GitHub Copilot agents via chat interface.
        
        Args:
            repo_path: Repository path
            output_dir: Output directory
            config: Configuration (LLM config removed - not needed)
            verbose: Enable verbose output
            generate_html: Whether to generate HTML viewer
        """
        self.repo_path = repo_path
        self.output_dir = output_dir
        self.config = config
        self.verbose = verbose
        self.generate_html = generate_html
        # Reduced to 3 stages: analysis, clustering, finalization (+ optional HTML)
        self.progress_tracker = ProgressTracker(total_stages=3 + (1 if generate_html else 0), verbose=verbose)
        self.job = DocumentationJob()
        
        # Setup job metadata
        self.job.repository_path = str(repo_path)
        self.job.repository_name = repo_path.name
        self.job.output_directory = str(output_dir)
        # LLM config removed - no longer needed
        self.job.llm_config = LLMConfig(
            main_model="GitHub Copilot (via chat interface)",
            cluster_model="",
            base_url=""
        )
        
        # Configure backend logging
        self._configure_backend_logging()
    
    def _configure_backend_logging(self):
        """Configure backend logger for CLI use with colored output."""
        from gatowiki.src.be.dependency_analyzer.utils.logging_config import ColoredFormatter
        
        # Get backend logger (parent of all backend modules)
        backend_logger = logging.getLogger('gatowiki.src.be')
        
        # Remove existing handlers to avoid duplicates
        backend_logger.handlers.clear()
        
        if self.verbose:
            # In verbose mode, show INFO and above
            backend_logger.setLevel(logging.INFO)
            
            # Create console handler with formatting
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            
            # Use colored formatter for better readability
            colored_formatter = ColoredFormatter()
            console_handler.setFormatter(colored_formatter)
            
            # Add handler to logger
            backend_logger.addHandler(console_handler)
        else:
            # In non-verbose mode, suppress backend logs (use WARNING level to hide INFO/DEBUG)
            backend_logger.setLevel(logging.WARNING)
            
            # Create console handler for warnings and errors only
            console_handler = logging.StreamHandler(sys.stderr)
            console_handler.setLevel(logging.WARNING)
            
            # Use colored formatter even for warnings/errors
            colored_formatter = ColoredFormatter()
            console_handler.setFormatter(colored_formatter)
            
            backend_logger.addHandler(console_handler)
        
        # Prevent propagation to root logger to avoid duplicate messages
        backend_logger.propagate = False
    
    def generate(self) -> DocumentationJob:
        """
        Run code analysis ONLY with progress tracking.
        
        Note: Documentation generation is handled by GitHub Copilot agents.
        This method only performs dependency analysis and module clustering.
        
        Returns:
            Completed DocumentationJob
            
        Raises:
            APIError: If analysis fails
        """
        self.job.start()
        start_time = time.time()
        
        try:
            # Set CLI context for backend
            set_cli_context(True)
            
            # Create backend config with CLI settings
            backend_config = BackendConfig.from_cli(
                repo_path=str(self.repo_path),
                output_dir=str(self.output_dir)
            )
            
            # Run backend code analysis (not documentation generation)
            self._run_backend_analysis(backend_config)
            
            # Optional HTML Generation
            if self.generate_html:
                self._run_html_generation()
            
            # Finalization
            self._finalize_job()
            
            # Complete job
            generation_time = time.time() - start_time
            self.job.complete()
            
            return self.job
            
        except APIError as e:
            self.job.fail(str(e))
            raise
        except Exception as e:
            self.job.fail(str(e))
            raise
    
    def _run_backend_analysis(self, backend_config: BackendConfig):
        """Run the backend code analysis with progress tracking.
        
        Note: This now only performs analysis, not documentation generation.
        Documentation generation is handled by GitHub Copilot agents.
        """
        
        # Stage 1: Dependency Analysis
        self.progress_tracker.start_stage(1, "Dependency Analysis")
        if self.verbose:
            self.progress_tracker.update_stage(0.2, "Initializing dependency analyzer...")
        
        # Create analysis generator
        doc_generator = DocumentationGenerator(backend_config)
        
        if self.verbose:
            self.progress_tracker.update_stage(0.5, "Parsing source files...")
        
        # Build dependency graph
        try:
            components, leaf_nodes = doc_generator.graph_builder.build_dependency_graph()
            self.job.statistics.total_files_analyzed = len(components)
            self.job.statistics.leaf_nodes = len(leaf_nodes)
            
            if self.verbose:
                self.progress_tracker.update_stage(1.0, f"Found {len(leaf_nodes)} leaf nodes")
        except Exception as e:
            raise APIError(f"Dependency analysis failed: {e}")
        
        self.progress_tracker.complete_stage()
        
        # Stage 2: Module Clustering
        self.progress_tracker.start_stage(2, "Module Clustering")
        if self.verbose:
            self.progress_tracker.update_stage(0.5, "Clustering modules...")
        
        # Import clustering function
        from gatowiki.src.be.cluster_modules import cluster_modules
        from gatowiki.src.utils import file_manager
        from gatowiki.src.config import FIRST_MODULE_TREE_FILENAME, MODULE_TREE_FILENAME
        
        working_dir = str(self.output_dir.absolute())
        file_manager.ensure_directory(working_dir)
        first_module_tree_path = os.path.join(working_dir, FIRST_MODULE_TREE_FILENAME)
        module_tree_path = os.path.join(working_dir, MODULE_TREE_FILENAME)
        
        try:
            if os.path.exists(first_module_tree_path):
                module_tree = file_manager.load_json(first_module_tree_path)
            else:
                module_tree = cluster_modules(leaf_nodes, components, backend_config)
                file_manager.save_json(module_tree, first_module_tree_path)
            
            file_manager.save_json(module_tree, module_tree_path)
            self.job.module_count = len(module_tree)
            
            if self.verbose:
                self.progress_tracker.update_stage(1.0, f"Created {len(module_tree)} modules")
        except Exception as e:
            raise APIError(f"Module clustering failed: {e}")
        
        self.progress_tracker.complete_stage()
        
        # Stage 3: Analysis Completion
        self.progress_tracker.start_stage(3, "Finalizing Analysis")
        if self.verbose:
            self.progress_tracker.update_stage(0.5, "Creating analysis metadata...")
        
        try:
            # Create analysis metadata
            doc_generator.create_analysis_metadata(working_dir, components, len(leaf_nodes))
            
            # Collect generated analysis files
            for file_path in os.listdir(working_dir):
                if file_path.endswith('.json'):
                    self.job.files_generated.append(file_path)
            
            if self.verbose:
                self.progress_tracker.update_stage(1.0, "Analysis complete")
            
        except Exception as e:
            raise APIError(f"Analysis finalization failed: {e}")
        
        self.progress_tracker.complete_stage()
    
    def _run_html_generation(self):
        """Run HTML generation stage."""
        stage_num = 4 if self.generate_html else 3
        self.progress_tracker.start_stage(stage_num, "HTML Generation")
        
        from gatowiki.cli.html_generator import HTMLGenerator
        
        # Generate HTML
        html_generator = HTMLGenerator()
        
        if self.verbose:
            self.progress_tracker.update_stage(0.3, "Loading module tree and metadata...")
        
        repo_info = html_generator.detect_repository_info(self.repo_path)
        
        # Generate HTML with auto-loading of module_tree and metadata from docs_dir
        output_path = self.output_dir / "index.html"
        html_generator.generate(
            output_path=output_path,
            title=repo_info['name'],
            repository_url=repo_info['url'],
            github_pages_url=repo_info['github_pages_url'],
            docs_dir=self.output_dir  # Auto-load module_tree and metadata from here
        )
        
        self.job.files_generated.append("index.html")
        
        if self.verbose:
            self.progress_tracker.update_stage(1.0, "Generated index.html")
        
        self.progress_tracker.complete_stage()
    
    def _finalize_job(self):
        """Finalize the job."""
        # Check for analysis metadata (not documentation metadata)
        metadata_path = self.output_dir / "analysis_metadata.json"
        if not metadata_path.exists():
            # Create job metadata if it doesn't exist
            job_metadata_path = self.output_dir / "job_metadata.json"
            with open(job_metadata_path, 'w') as f:
                f.write(self.job.to_json())

