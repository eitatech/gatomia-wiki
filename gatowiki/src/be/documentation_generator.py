import logging
import os
from typing import Dict, List, Any
import traceback

# Configure logging and monitoring
logger = logging.getLogger(__name__)

# Local imports
from gatowiki.src.be.dependency_analyzer import DependencyGraphBuilder
from gatowiki.src.be.cluster_modules import cluster_modules
from gatowiki.src.config import (
    Config,
    FIRST_MODULE_TREE_FILENAME,
    MODULE_TREE_FILENAME
)
from gatowiki.src.utils import file_manager

# NOTE: This module now ONLY performs code analysis.
# Documentation generation is handled by GitHub Copilot agents through chat interface.
# Output: module_tree.json and first_module_tree.json for agents to consume.


class DocumentationGenerator:
    """Code analysis orchestrator - generates module trees for GitHub Copilot agents.
    
    This class performs dependency analysis and module clustering ONLY.
    Documentation generation is handled by GitHub Copilot agents via chat interface.
    """
    
    def __init__(self, config: Config, commit_id: str = None):
        self.config = config
        self.commit_id = commit_id
        self.graph_builder = DependencyGraphBuilder(config)
    
    def create_analysis_metadata(self, working_dir: str, components: Dict[str, Any], num_leaf_nodes: int):
        """Create a metadata file with code analysis information.
        
        Note: This only captures analysis metadata. Documentation generation
        metadata is handled by GitHub Copilot agents.
        """
        from datetime import datetime
        
        metadata = {
            "analysis_info": {
                "timestamp": datetime.now().isoformat(),
                "generator_version": "2.0.0-copilot",
                "repo_path": self.config.repo_path,
                "commit_id": self.commit_id
            },
            "statistics": {
                "total_components": len(components),
                "leaf_nodes": num_leaf_nodes,
                "max_depth": self.config.max_depth
            },
            "analysis_files": [
                "module_tree.json",
                "first_module_tree.json"
            ],
            "note": "Documentation generation is handled by GitHub Copilot agents via chat interface"
        }
        
        metadata_path = os.path.join(working_dir, "analysis_metadata.json")
        file_manager.save_json(metadata, metadata_path)

    
    
    def run(self) -> str:
        """Run code analysis ONLY - generates module trees for GitHub Copilot agents.
        
        Returns:
            working_dir: Path to output directory with analysis files
        """
        try:
            # Build dependency graph
            logger.info("🔍 Building dependency graph...")
            components, leaf_nodes = self.graph_builder.build_dependency_graph()

            logger.info(f"✓ Found {len(components)} components with {len(leaf_nodes)} leaf nodes")
            
            # Cluster modules
            working_dir = os.path.abspath(self.config.docs_dir)
            file_manager.ensure_directory(working_dir)
            first_module_tree_path = os.path.join(working_dir, FIRST_MODULE_TREE_FILENAME)
            module_tree_path = os.path.join(working_dir, MODULE_TREE_FILENAME)
            
            # Check if module tree exists
            if os.path.exists(first_module_tree_path):
                logger.info(f"✓ Module tree found at {first_module_tree_path}")
                module_tree = file_manager.load_json(first_module_tree_path)
            else:
                logger.info("📊 Clustering modules...")
                module_tree = cluster_modules(leaf_nodes, components, self.config)
                file_manager.save_json(module_tree, first_module_tree_path)
            
            # Save module tree
            file_manager.save_json(module_tree, module_tree_path)
            logger.info(f"✓ Grouped components into {len(module_tree)} modules")
            
            # Create analysis metadata
            self.create_analysis_metadata(working_dir, components, len(leaf_nodes))
            
            logger.info("")
            logger.info("✅ Code analysis completed successfully!")
            logger.info(f"📁 Analysis files saved to: {working_dir}")
            logger.info(f"   - {FIRST_MODULE_TREE_FILENAME}")
            logger.info(f"   - {MODULE_TREE_FILENAME}")
            logger.info(f"   - analysis_metadata.json")
            logger.info("")
            logger.info("📝 Next steps:")
            logger.info("   1. Use GitHub Copilot Chat to generate documentation")
            logger.info("   2. Refer to .github/agents/gatowiki-orchestrator.agent.md")
            logger.info("   3. Run 'gatowiki publish' to generate GitHub Pages")
            
            return working_dir
            
        except Exception as e:
            logger.error(f"Code analysis failed: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise
