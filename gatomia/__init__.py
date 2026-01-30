"""
GatoWiki: Transform codebases into comprehensive documentation using AI-powered analysis.

This package provides a CLI tool for generating documentation from code repositories.
"""

__version__ = "0.25.5"
__author__ = "EITA Technologies"
__license__ = "MIT"

from gatowiki.cli.main import cli

__all__ = ["cli", "__version__"]

