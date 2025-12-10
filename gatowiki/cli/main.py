"""
Main CLI application for GatoWiki using Click framework.
"""

import sys
import click
from pathlib import Path

from gatowiki import __version__


@click.group()
@click.version_option(version=__version__, prog_name="GatoWiki CLI")
@click.pass_context
def cli(ctx):
    """
    GatoWiki: Transform codebases into comprehensive documentation.
    
    Analyze code structure and publish documentation with GitHub Copilot integration.
    Supports Python, Java, JavaScript, TypeScript, C, C++, and C#.
    
    Workflow:
      1. gatowiki analyze      - Analyze code structure
      2. GitHub Copilot Chat   - Generate documentation via agents
      3. gatowiki publish      - Publish to GitHub Pages (optional)
    """
    # Ensure context object exists
    ctx.ensure_object(dict)


@cli.command()
def version():
    """Display version information."""
    click.echo(f"GatoWiki CLI v{__version__}")
    click.echo("Python-based documentation generator using AI analysis")
    

# Import commands
from gatowiki.cli.commands.config import config_group
from gatowiki.cli.commands.analyze import analyze_command
from gatowiki.cli.commands.publish import publish_command

# Register command groups
cli.add_command(config_group)
cli.add_command(analyze_command, name="analyze")
cli.add_command(publish_command, name="publish")


def main():
    """Entry point for the CLI."""
    try:
        cli(obj={})
    except KeyboardInterrupt:
        click.echo("\n\nInterrupted by user", err=True)
        sys.exit(130)
    except Exception as e:
        click.secho(f"\n✗ Unexpected error: {e}", fg="red", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()

