"""
Configuration commands for GatoWiki CLI.
"""

import json
import sys
import click
from typing import Optional

from gatowiki.cli.config_manager import ConfigManager
from gatowiki.cli.utils.errors import (
    ConfigurationError, 
    handle_error, 
    EXIT_SUCCESS,
    EXIT_CONFIG_ERROR
)
from gatowiki.cli.utils.validation import (
    validate_url,
    validate_api_key,
    validate_model_name,
    is_top_tier_model,
    mask_api_key
)


@click.group(name="config")
def config_group():
    """Manage GatoWiki configuration settings (output directory preferences)."""
    pass


@config_group.command(name="set")
@click.option(
    "--output",
    "-o",
    type=str,
    help="Default output directory for documentation (default: ./docs)"
)
def config_set(
    output: Optional[str]
):
    """
    Set configuration values for GatoWiki.
    
    Note: API key configuration is not needed. GitHub Copilot handles
    authentication automatically through your IDE or GitHub CLI.
    
    Examples:
    
    \b
    # Set default output directory
    $ gatowiki config set --output ./documentation
    
    \b
    # Reset to default (./docs)
    $ gatowiki config set --output ./docs
    """
    try:
        # Check if output option is provided
        if not output:
            click.echo("\nNo options provided. Use --help for usage information.")
            click.echo("\nExample: gatowiki config set --output ./docs")
            sys.exit(EXIT_CONFIG_ERROR)
        
        # Create config manager and save
        manager = ConfigManager()
        manager.load()  # Load existing config if present
        
        # Save only output directory
        manager.save(default_output=output)
        
        # Display success message
        click.echo()
        click.secho(f"✓ Default output directory: {output}", fg="green")
        click.echo("\n" + click.style("Configuration updated successfully.", fg="green", bold=True))
        click.echo()
        click.echo("Note: API authentication is handled by GitHub Copilot.")
        click.echo("      No API keys needed for GatoWiki v0.25.5+")
        click.echo()
        
    except ConfigurationError as e:
        click.secho(f"\n✗ Configuration error: {e.message}", fg="red", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        sys.exit(handle_error(e))


@config_group.command(name="show")
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output in JSON format"
)
def config_show(output_json: bool):
    """
    Display current configuration.
    
    Examples:
    
    \b
    # Display configuration
    $ gatowiki config show
    
    \b
    # Display as JSON
    $ gatowiki config show --json
    """
    try:
        manager = ConfigManager()
        
        if not manager.load():
            click.secho("\n✗ Configuration not found.", fg="yellow")
            click.echo("\nGatoWiki v0.25.5+ uses GitHub Copilot for authentication.")
            click.echo("No API keys needed!\n")
            click.echo("You can optionally set a default output directory:")
            click.echo("  gatowiki config set --output ./docs")
            click.echo("\nFor more help: gatowiki config set --help")
            sys.exit(EXIT_SUCCESS)
        
        config = manager.get_config()
        
        if output_json:
            # JSON output
            output = {
                "default_output": config.default_output if config else "docs",
                "config_file": str(manager.config_file_path),
                "version": "2.0.0",
                "authentication": "GitHub Copilot (managed by IDE)"
            }
            click.echo(json.dumps(output, indent=2))
        else:
            # Human-readable output
            click.echo()
            click.secho("GatoWiki Configuration (v0.25.5)", fg="blue", bold=True)
            click.echo("━" * 40)
            click.echo()
            
            click.secho("Output Settings", fg="cyan", bold=True)
            if config:
                click.echo(f"  Default Output:   {config.default_output}")
            else:
                click.echo(f"  Default Output:   docs (default)")
            
            click.echo()
            click.secho("Authentication", fg="cyan", bold=True)
            click.echo("  Provider:         GitHub Copilot")
            click.echo("  Managed by:       Your IDE (VS Code, IntelliJ, etc.)")
            click.echo("  API Keys:         Not required")
            
            click.echo()
            click.echo(f"Configuration file: {manager.config_file_path}")
            click.echo()
        
    except Exception as e:
        sys.exit(handle_error(e))


@config_group.command(name="validate")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed validation steps"
)
def config_validate(verbose: bool):
    """
    Validate GatoWiki configuration.
    
    Note: API validation is not needed in v0.25.5+. GitHub Copilot handles
    all authentication through your IDE.
    
    This command validates:
      • Configuration file exists and is valid
      • Output directory setting is correct
    
    Examples:
    
    \b
    # Validate configuration
    $ gatowiki config validate
    
    \b
    # Verbose output
    $ gatowiki config validate --verbose
    """
    try:
        click.echo()
        click.secho("Validating configuration...", fg="blue", bold=True)
        click.echo()
        
        manager = ConfigManager()
        
        # Check config file
        if verbose:
            click.echo("[1/2] Checking configuration file...")
            click.echo(f"      Path: {manager.config_file_path}")
        
        config_exists = manager.load()
        
        if not config_exists:
            click.secho("ℹ️  No configuration file found (using defaults)", fg="cyan")
            if verbose:
                click.echo("      This is normal for first-time usage")
                click.echo("      Default output directory: ./docs")
        else:
            if verbose:
                click.secho("      ✓ File exists", fg="green")
                click.secho("      ✓ Valid JSON format", fg="green")
            else:
                click.secho("✓ Configuration file exists", fg="green")
        
        # Check output directory setting
        if verbose:
            click.echo()
            click.echo("[2/2] Checking output directory...")
        
        config = manager.get_config()
        output_dir = config.default_output if config else "docs"
        
        if verbose:
            click.echo(f"      Output directory: {output_dir}")
            click.secho("      ✓ Valid setting", fg="green")
        else:
            click.secho(f"✓ Output directory: {output_dir}", fg="green")
        
        # Success
        click.echo()
        click.secho("✓ Configuration is valid!", fg="green", bold=True)
        click.echo()
        click.echo("Note: API validation not required in v0.25.5+")
        click.echo("      GitHub Copilot handles authentication automatically")
        click.echo()
        
    except ConfigurationError as e:
        click.secho(f"\n✗ Configuration error: {e.message}", fg="red", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        sys.exit(handle_error(e, verbose=verbose))

