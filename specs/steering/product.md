---
inclusion: always
---

# GatoWiki Product Overview

GatoWiki is an AI-powered documentation generation framework that creates comprehensive, repository-level documentation for large-scale codebases. It uses hierarchical decomposition and recursive multi-agent processing to generate holistic documentation that captures not just individual components, but their cross-file, cross-module, and system-level interactions.

## Core Capabilities

- **Multi-language support**: Python, Java, JavaScript, TypeScript, C, C++, C#
- **Hierarchical decomposition**: Dynamic programming-inspired strategy for breaking down large codebases while preserving architectural context
- **Recursive agent system**: Adaptive multi-agent processing with dynamic delegation for complex modules
- **Multi-modal output**: Generates textual documentation, architecture diagrams (Mermaid), data flows, and sequence diagrams
- **Dual interfaces**: CLI tool for local repositories and web application for GitHub URL-based generation

## Key Features

- Handles codebases from 86K to 1.4M+ lines of code
- Generates repository overview, module documentation, and cross-module interaction analysis
- Creates visual artifacts including system architecture diagrams and dependency graphs
- Supports GitHub Pages deployment with interactive HTML viewer
- Uses tree-sitter for AST-based code analysis across all supported languages

## Target Users

Developers and teams who need to:
- Understand large, unfamiliar codebases quickly
- Generate comprehensive documentation for existing projects
- Maintain up-to-date architectural documentation
- Onboard new team members efficiently
