---
inclusion: always
---

# Project Structure

## Top-Level Organization

```
gatowiki/                    # Main package directory
├── cli/                     # Command-line interface
├── src/                     # Core application (backend + frontend)
├── templates/               # HTML templates for web viewer
├── run_web_app.py          # Web application entry point
├── __main__.py             # Package entry point
└── py.typed                # PEP 561 type marker

docker/                      # Docker deployment files
docs/                        # Generated documentation output
img/                         # Project images and assets
.specify/                    # Specification and planning tools
pyproject.toml              # Package metadata and configuration
requirements.txt            # Pinned dependencies
```

## CLI Module (`gatowiki/cli/`)

Command-line interface implementation using Click framework.

```
cli/
├── main.py                 # CLI entry point and command registration
├── commands/               # Command implementations
│   ├── config.py          # Configuration management (set, show, validate)
│   └── generate.py        # Documentation generation command
├── models/                 # Data models
│   ├── config.py          # Configuration data structures
│   └── job.py             # Job tracking models
├── utils/                  # CLI utilities
│   ├── api_errors.py      # API error handling
│   ├── errors.py          # General error handling
│   ├── fs.py              # File system operations
│   ├── instructions.py    # User instructions and help text
│   ├── logging.py         # Logging configuration
│   ├── progress.py        # Progress tracking and display
│   ├── repo_validator.py  # Repository validation
│   └── validation.py      # Input validation
├── adapters/               # External service integrations
│   └── doc_generator.py   # Documentation generation adapter
├── config_manager.py       # Configuration persistence
├── git_manager.py          # Git operations
└── html_generator.py       # HTML viewer generation
```

## Backend Module (`gatowiki/src/core/`)

Core documentation generation engine with AI agents and dependency analysis.

```
src/core/
├── main.py                        # Backend entry point
├── agent_orchestrator.py          # Multi-agent coordination
├── documentation_generator.py     # Documentation generation orchestration
├── cluster_modules.py             # Hierarchical module decomposition
├── llm_services.py               # LLM API integration and fallback handling
├── prompt_template.py            # Agent system prompts and templates
├── utils.py                      # Backend utilities
├── agent_tools/                  # Tools available to AI agents
│   ├── deps.py                   # Dependency context for agents
│   ├── read_code_components.py   # Code reading tool
│   ├── str_replace_editor.py     # Documentation editing tool
│   └── generate_sub_module_documentations.py  # Recursive delegation tool
└── dependency_analyzer/          # Multi-language code analysis
    ├── ast_parser.py             # AST parsing coordinator
    ├── dependency_graphs_builder.py  # Dependency graph construction
    ├── topo_sort.py              # Topological sorting
    ├── analysis/                 # Analysis services
    │   ├── analysis_service.py   # Main analysis orchestration
    │   ├── call_graph_analyzer.py  # Call graph construction
    │   ├── cloning.py            # Repository cloning
    │   └── repo_analyzer.py      # Repository-level analysis
    ├── analyzers/                # Language-specific analyzers
    │   ├── python.py
    │   ├── java.py
    │   ├── javascript.py
    │   ├── typescript.py
    │   ├── c.py
    │   ├── cpp.py
    │   └── csharp.py
    ├── models/                   # Data models
    │   ├── core.py               # Core data structures (Node, Edge, etc.)
    │   └── analysis.py           # Analysis result models
    └── utils/                    # Analyzer utilities
        ├── logging_config.py     # Logging setup
        ├── patterns.py           # Pattern matching utilities
        └── security.py           # Security validation
```

## Frontend Module (`gatowiki/src/web/`)

Web application for GitHub URL-based documentation generation.

```
src/web/
├── web_app.py              # FastAPI application setup
├── routes.py               # API endpoints
├── github_processor.py     # GitHub repository processing
├── visualise_docs.py       # Documentation visualization
├── background_worker.py    # Async job processing
├── cache_manager.py        # Caching layer
├── models.py               # Frontend data models
├── config.py               # Frontend configuration
├── templates.py            # Template rendering
└── template_utils.py       # Template utilities
```

## Key Architectural Patterns

### Hierarchical Decomposition
- Modules are organized in a tree structure (`module_tree.json`)
- Each module can contain sub-modules for complex codebases
- Topological sorting ensures proper dependency ordering

### Recursive Agent System
- `agent_orchestrator.py` creates agents based on module complexity
- Simple modules use leaf agents (direct documentation)
- Complex modules use recursive agents (can delegate to sub-modules)
- Agents have access to tools: read code, edit docs, generate sub-docs

### Dependency Analysis Pipeline
1. **AST Parsing**: Language-specific parsers extract code structure
2. **Graph Building**: Construct dependency and call graphs
3. **Clustering**: Group related components into modules
4. **Topological Sort**: Order modules by dependencies
5. **Agent Processing**: Generate documentation following dependency order

### Multi-Modal Output
- Textual documentation in Markdown
- Mermaid diagrams for architecture visualization
- JSON metadata for module structure
- HTML viewer for interactive browsing

## Configuration Storage

- **User config**: `~/.gatowiki/config.json` (API keys via system keychain)
- **Module tree**: `docs/module_tree.json` (hierarchical structure)
- **Metadata**: `docs/metadata.json` (generation info)
- **Docker env**: `.env` file for container configuration

## Output Structure

```
docs/
├── overview.md                 # Repository-level documentation
├── <module_name>.md           # Module-specific documentation
├── module_tree.json           # Hierarchical module structure
├── first_module_tree.json     # Initial clustering result
├── metadata.json              # Generation metadata
└── index.html                 # Interactive viewer (with --github-pages)
```

## Naming Conventions

- **Modules**: Snake_case for Python modules and packages
- **Classes**: PascalCase (e.g., `AgentOrchestrator`, `DependencyAnalyzer`)
- **Functions**: Snake_case (e.g., `create_agent`, `process_module`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `MODULE_TREE_FILENAME`)
- **Private members**: Leading underscore (e.g., `_internal_method`)

## Import Patterns

- Use absolute imports from package root: `from gatowiki.src.core import ...`
- Local imports within modules: `from .utils import ...`
- Type hints imported from `typing` module
- Pydantic models for data validation and serialization
