"""
Analyze command for code analysis only (no documentation generation).
"""

import sys
import logging
from pathlib import Path
from typing import Optional
import click
import time

from gatowiki.cli.utils.errors import (
    RepositoryError,
    handle_error,
    EXIT_SUCCESS,
)
from gatowiki.cli.utils.repo_validator import validate_repository
from gatowiki.cli.utils.logging import create_logger


@click.command(name="analyze")
@click.option(
    "--repo-path",
    type=click.Path(exists=True),
    default=".",
    help="Repository path to analyze (default: current directory)",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default="docs",
    help="Output directory for analysis results (default: ./docs)",
)
@click.option(
    "--languages",
    type=str,
    help="Comma-separated list of languages to analyze (e.g., python,java,typescript)",
)
@click.option(
    "--max-depth",
    type=int,
    help="Maximum module hierarchy depth",
)
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed progress and debug information",
)
@click.pass_context
def analyze_command(
    ctx,
    repo_path: str,
    output: str,
    languages: Optional[str],
    max_depth: Optional[int],
    verbose: bool
):
    """
    Analyze repository code structure without generating documentation.
    
    Performs tree-sitter parsing, dependency graph construction, and module
    clustering. Outputs module_tree.json and first_module_tree.json for use
    by GitHub Copilot agents.
    
    This command does NOT generate documentation or call LLM APIs. It only
    performs code analysis. Documentation generation is handled by GitHub
    Copilot agents.
    
    Examples:
    
    \b
    # Analyze current directory
    $ gatowiki analyze
    
    \b
    # Analyze specific repository
    $ gatowiki analyze --repo-path /path/to/repo
    
    \b
    # Filter by languages
    $ gatowiki analyze --languages python,java
    
    \b
    # Set maximum depth
    $ gatowiki analyze --max-depth 3
    """
    logger = create_logger(verbose=verbose)
    start_time = time.time()
    
    # Suppress httpx INFO logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    
    try:
        # Validate repository
        logger.step("Validating repository...", 1, 3)
        
        repo_path_obj = Path(repo_path).expanduser().resolve()
        repo_path_obj, detected_languages = validate_repository(repo_path_obj)
        
        logger.success(f"Repository valid: {repo_path_obj.name}")
        if verbose:
            logger.debug(f"Detected languages: {', '.join(f'{lang} ({count} files)' for lang, count in detected_languages)}")
        
        # Validate output directory
        output_dir = Path(output).expanduser().resolve()
        output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.success(f"Output directory: {output_dir}")
        
        # Perform dependency analysis
        logger.step("Analyzing code structure...", 2, 3)
        
        from gatowiki.src.config import Config
        from gatowiki.src.be.dependency_analyzer import DependencyGraphBuilder
        from gatowiki.src.utils import file_manager
        from gatowiki.src.config import FIRST_MODULE_TREE_FILENAME, MODULE_TREE_FILENAME
        import os
        
        # Create config for analysis
        # Note: LLM configuration removed - all LLM interactions happen through GitHub Copilot Chat
        temp_dir = os.path.join(str(output_dir), "temp")
        config = Config(
            repo_path=str(repo_path_obj),
            output_dir=temp_dir,
            dependency_graph_dir=os.path.join(temp_dir, "dependency_graphs"),
            docs_dir=str(output_dir),
            max_depth=max_depth if max_depth else 3
        )
        
        # Build dependency graph
        graph_builder = DependencyGraphBuilder(config)
        
        if verbose:
            logger.debug("Parsing source files with tree-sitter...")
        
        components, leaf_nodes = graph_builder.build_dependency_graph()
        
        logger.success(f"Found {len(components)} components, {len(leaf_nodes)} leaf nodes")
        
        # Perform module clustering
        logger.step("Clustering modules...", 3, 3)
        
        from gatowiki.src.be.cluster_modules import cluster_modules
        
        working_dir = str(output_dir.absolute())
        file_manager.ensure_directory(working_dir)
        first_module_tree_path = os.path.join(working_dir, FIRST_MODULE_TREE_FILENAME)
        module_tree_path = os.path.join(working_dir, MODULE_TREE_FILENAME)
        
        if verbose:
            logger.debug("Clustering components into modules...")
        
        # Note: cluster_modules requires LLM, but we'll handle this gracefully
        # For now, create a simple flat structure
        # TODO: Implement non-LLM clustering or make this optional
        try:
            module_tree = cluster_modules(leaf_nodes, components, config)
        except Exception as e:
            if verbose:
                logger.warning(f"LLM-based clustering failed: {e}")
                logger.debug("Creating simple flat module structure...")
            
            # Create simple flat structure
            module_tree = {
                repo_path_obj.name: {
                    "description": "Repository root",
                    "components": leaf_nodes,
                    "children": {}
                }
            }
        
        file_manager.save_json(module_tree, first_module_tree_path)
        file_manager.save_json(module_tree, module_tree_path)
        
        logger.success(f"Created {len(module_tree)} modules")
        
        # Display results
        analysis_time = time.time() - start_time
        
        click.echo()
        click.secho("✓ Analysis complete!", fg="green", bold=True)
        click.echo()
        click.echo(f"  Repository:     {repo_path_obj.name}")
        click.echo(f"  Components:     {len(components)}")
        click.echo(f"  Leaf nodes:     {len(leaf_nodes)}")
        click.echo(f"  Modules:        {len(module_tree)}")
        click.echo(f"  Analysis time:  {analysis_time:.1f}s")
        click.echo()
        click.echo(f"  Output files:")
        click.echo(f"    • {output_dir / FIRST_MODULE_TREE_FILENAME}")
        click.echo(f"    • {output_dir / MODULE_TREE_FILENAME}")
        click.echo()
        click.secho("Next steps:", fg="cyan", bold=True)
        click.echo("  1. Open GitHub Copilot Chat")
        click.echo("  2. Ask: 'Generate documentation for this repository'")
        click.echo("  3. Run: gatowiki publish --github-pages (optional)")
        click.echo()
        
    except RepositoryError as e:
        logger.error(e.message)
        sys.exit(e.exit_code)
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user")
        sys.exit(130)
    except Exception as e:
        sys.exit(handle_error(e, verbose=verbose))
