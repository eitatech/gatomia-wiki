# GatoWiki - AI-Powered Repository Documentation Generator

## Project Overview

**GatoWiki** (also known as GatomIA Code Wiki) is an open-source AI-powered framework for automated repository-level documentation generation. It transforms large-scale codebases (86K-1.4M lines of code) into comprehensive, architecture-aware documentation using hierarchical decomposition and multi-agent processing.

**Version**: 0.25.5 (GitHub Copilot integration)
**License**: MIT
**Python Requirement**: 3.12+
**Research Paper**: arXiv 2510.24428

### Core Capabilities

- **Multi-Language Support**: Python, Java, JavaScript, TypeScript, C, C++, C# (7 languages via Tree-sitter)
- **Hierarchical Decomposition**: Dynamic programming-inspired strategy preserving architectural context
- **Recursive Multi-Agent Processing**: Adaptive multi-agent system with dynamic delegation
- **Multi-Modal Documentation**: Textual descriptions + visual artifacts (Mermaid diagrams, architecture diagrams, data flows, sequence diagrams)
- **GitHub Copilot Integration**: v0.25.5 uses GitHub Copilot agents instead of direct LLM API calls

### Key Innovation

GatoWiki employs a three-stage process:
1. **Hierarchical Decomposition** - Partitions repositories into coherent modules while preserving architectural context
2. **Recursive Multi-Agent Processing** - Adaptive processing with dynamic task delegation for complex modules
3. **Multi-Modal Synthesis** - Integrates textual and visual artifacts for comprehensive understanding

---

## Architecture & Structure

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    CLI Layer (Click)                    │
│  Entry Point: gatowiki/cli/main.py                      │
│  Commands: analyze, publish, config                     │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Service Layer (Orchestration)              │
│  Core: gatowiki/src/core/documentation_generator.py     │
│  Orchestrates: Analysis → Clustering → Agent Processing │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│          Analysis Layer (Code Understanding)            │
│  - Dependency Analyzer: AST parsing, call graphs        │
│  - Language Analyzers: Python, Java, JS, TS, C, C++, C# │
│  - Repository Analyzer: File tree construction          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│            Data Layer (Models & Persistence)            │
│  Models: Node, CallRelationship, Repository (Pydantic)  │
│  Output: JSON artifacts, Markdown docs                  │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
gatowiki/
├── gatowiki/                           # Main Python package (69 .py files, 12,075 LOC)
│   ├── __init__.py                     # Version: 0.25.5
│   ├── __main__.py
│   ├── run_web_app.py                  # Web application entry point
│   │
│   ├── cli/                            # Command-line interface (Click framework)
│   │   ├── main.py                     # Main CLI group with version command
│   │   ├── config_manager.py           # Configuration file management
│   │   ├── html_generator.py           # HTML generation for GitHub Pages
│   │   ├── git_manager.py              # Git operations
│   │   ├── commands/                   # CLI command implementations
│   │   │   ├── analyze.py              # Code analysis command
│   │   │   ├── publish.py              # GitHub Pages publishing
│   │   │   └── config.py               # Configuration management
│   │   ├── models/                     # Data models (config, job tracking)
│   │   ├── utils/                      # CLI utilities (logging, fs, validation, etc.)
│   │   └── adapters/                   # External integrations
│   │
│   ├── src/                            # Core application logic
│   │   ├── core/                       # Core analysis engine
│   │   │   ├── main.py                 # Async orchestration entry point
│   │   │   ├── documentation_generator.py  # Analysis orchestrator
│   │   │   ├── cluster_modules.py      # Hierarchical module decomposition
│   │   │   │
│   │   │   └── dependency_analyzer/    # Multi-language AST analysis
│   │   │       ├── ast_parser.py       # AST parsing orchestrator
│   │   │       ├── dependency_graphs_builder.py  # Builds dependency graphs
│   │   │       ├── topo_sort.py        # Topological sorting
│   │   │       ├── analyzers/          # Language-specific parsers
│   │   │       │   ├── python.py       # Python AST analyzer (ast.NodeVisitor)
│   │   │       │   ├── java.py         # Java analyzer (Tree-sitter)
│   │   │       │   ├── javascript.py   # JavaScript analyzer
│   │   │       │   ├── typescript.py   # TypeScript analyzer
│   │   │       │   ├── c.py            # C analyzer
│   │   │       │   ├── cpp.py          # C++ analyzer
│   │   │       │   └── csharp.py       # C# analyzer
│   │   │       ├── analysis/           # Analysis service layer
│   │   │       │   ├── repo_analyzer.py   # File tree analysis
│   │   │       │   ├── call_graph_analyzer.py  # Dependency analysis
│   │   │       │   ├── analysis_service.py  # Orchestration service
│   │   │       │   └── cloning.py      # Repository cloning
│   │   │       ├── models/             # Data models (Node, CallRelationship, Repository)
│   │   │       └── utils/              # Utilities (logging, patterns, security)
│   │   │
│   │   └── web/                        # Web application (FastAPI)
│   │       ├── web_app.py              # FastAPI application
│   │       ├── routes.py               # HTTP route handlers
│   │       ├── models.py               # Pydantic data models
│   │       ├── github_processor.py     # GitHub repo processing
│   │       ├── background_worker.py    # Background job processing
│   │       ├── cache_manager.py        # Documentation caching
│   │       └── visualise_docs.py       # Documentation visualization
│   │
│   └── templates/                      # Jinja2 HTML templates
│       └── github_pages/               # GitHub Pages templates
│
├── docker/                             # Docker deployment
│   ├── Dockerfile                      # Python 3.12 containerization
│   ├── docker-compose.yml              # Service orchestration
│   ├── env.example                     # Environment variable template
│   └── DOCKER_README.md                # Docker deployment guide
│
├── docs/                               # User documentation
│   ├── github-copilot-integration.md   # GitHub Copilot setup guide
│   └── customizing-agents.md           # Agent customization guide
│
├── specs/                              # Feature specifications
│   ├── requirements.md                 # GitHub Copilot integration requirements
│   ├── design.md                       # Design documentation
│   ├── tasks.md                        # Implementation tasks
│   └── steering/                       # Project steering documents
│
├── .github/                            # GitHub configuration
│   ├── agents/                         # GitHub Copilot agent definitions
│   ├── instructions/                   # Agent instructions
│   └── prompts/                        # Prompt templates
│
├── .specify/                           # Feature specification management
│   ├── memory/                         # Specification memory
│   ├── scripts/                        # Automation scripts
│   └── templates/                      # Specification templates
│
├── .beads/                             # Issue tracking system (beads)
├── pyproject.toml                      # Python project metadata
├── requirements.txt                    # Python dependencies (160+ packages)
├── README.md                           # Main documentation
├── DEVELOPMENT.md                      # Development guide
├── AGENTS.md                           # Agent system constitution
└── LICENSE                             # MIT License
```

---

## Technologies & Frameworks

### Core Stack

- **Language**: Python 3.12+ (strict requirement)
- **CLI Framework**: Click 8.1.0+ (declarative command interface)
- **Web Framework**: FastAPI 0.116.1 (async HTTP server)
- **Code Analysis**: Tree-sitter 0.23.2 (AST parsing across 7 languages)
- **LLM Integration**:
  - LiteLLM 1.77.0 (provider abstraction)
  - OpenAI SDK 1.107.1
  - Pydantic-AI 1.0.6 (AI agent framework)
  - **Note**: v0.25.5 uses GitHub Copilot agents instead of direct API calls
- **Configuration**: Pydantic 2.11.7 + Pydantic-Settings 2.10.1
- **Templates**: Jinja2 3.1.6 (HTML templating)
- **Diagrams**: Mermaid-py 0.8.0 (diagram generation and validation)
- **Logging**: Rich 14.1.0 (enhanced terminal output)
- **Git Integration**: GitPython 3.1.40
- **Network Analysis**: NetworkX 3.5 (dependency graphs)
- **Web Server**: Uvicorn 0.35.0 (ASGI server)

### Tree-Sitter Language Parsers

- tree-sitter-python 0.23.6
- tree-sitter-java 0.23.5
- tree-sitter-javascript 0.21.4
- tree-sitter-typescript 0.21.2
- tree-sitter-c 0.21.4
- tree-sitter-cpp 0.23.4
- tree-sitter-c-sharp 0.23.1

### Development Tools

- **Testing**: pytest 7.4.0+, pytest-cov 4.1.0+, pytest-asyncio 0.21.0+
- **Formatting**: Black 23.0.0+ (100-char lines, Python 3.12 target)
- **Type Checking**: MyPy 1.5.0+ (non-enforced)
- **Linting**: Ruff 0.1.0+ (100-char lines, Python 3.12 target)

### External Dependencies

- **Node.js** 14.0.0+ (for Mermaid diagram validation)
- **Git** (for repository cloning and branch operations)

---

## Main Entry Points & Workflows

### CLI Entry Point

**Main Command**: `gatowiki/cli/main.py:cli()`

**Available Commands**:
1. `gatowiki analyze` - Code analysis without documentation
2. `gatowiki publish` - GitHub Pages publishing
3. `gatowiki config` - Configuration management
4. `gatowiki version` - Version display

### Web Application Entry Point

**Entry Point**: `gatowiki/run_web_app.py`
- Runs FastAPI ASGI app on port 8000 by default

### Documentation Generation Workflow (v0.25.5)

```
1. Analysis Phase (gatowiki analyze)
   ├─ Input: Repository path
   ├─ Process:
   │  ├─ RepoAnalyzer builds file tree (recursive directory scan)
   │  ├─ DependencyParser extracts components per language
   │  │  ├─ PythonASTAnalyzer (ast.NodeVisitor)
   │  │  └─ Other analyzers (Tree-sitter based)
   │  ├─ CallGraphAnalyzer tracks relationships
   │  ├─ DependencyGraphBuilder constructs full graph
   │  └─ cluster_modules() performs hierarchical decomposition
   └─ Output: module_tree.json, first_module_tree.json, analysis_metadata.json

2. Documentation Phase (GitHub Copilot Chat)
   ├─ GitHub Copilot agent reads module_tree.json
   ├─ User says: "Generate documentation"
   ├─ Process:
   │  ├─ Auto-analyze if module_tree.json missing
   │  ├─ Per-module documentation generation
   │  ├─ Cross-reference resolution
   │  ├─ Mermaid diagram generation
   │  └─ Hierarchical assembly
   └─ Output: overview.md, module_*.md files

3. Publishing Phase (gatowiki publish)
   ├─ Input: Generated documentation files
   ├─ Process:
   │  ├─ HTML generation for GitHub Pages
   │  ├─ Git branch creation (gh-pages)
   │  └─ Push to remote
   └─ Output: GitHub Pages site
```

---

## Code Patterns & Conventions

### Architectural Patterns

1. **Layered Architecture**
   - CLI layer (`cli/`) → User interface
   - Service layer (`src/core/documentation_generator.py`) → Orchestration
   - Core layer (Dependency analysis) → Code understanding
   - Data layer (Pydantic models) → Type safety

2. **Multi-Agent System**
   - GitHub Copilot agents via `.github/agents/*.md` definitions
   - Agents execute GatoWiki CLI commands
   - Dynamic delegation for complex modules

3. **Factory Pattern**
   - `DependencyParser` instantiates language-specific analyzers
   - `AnalysisService` creates and configures analyzer chain

4. **Strategy Pattern**
   - Language-specific analyzers (Python, Java, C, C++, C#, JavaScript, TypeScript)
   - Each implements standard interfaces from `BaseAnalyzer`

### Code Style

- **Formatting**: Black (100-character line length, Python 3.12 target)
- **Type Hints**: Encouraged but not enforced
- **Logging**: Rich library for colored terminal output
- **Error Handling**: Custom exception hierarchy (RepositoryError, FileSystemError, ConfigurationError, etc.)
- **Docstrings**: Expected for public functions/classes

### Module Conventions

- `__init__.py` files in all packages
- Relative imports within packages
- Async/await for long-running operations
- Context managers for resource management

---

## Configuration & Settings

### Configuration Storage

**Location**: `~/.gatowiki/config.json` (Version 2.0)

**Contains**:
- Output directory defaults
- **Note**: No API keys stored (GitHub Copilot handles auth)

### Environment Variables

- `PYTHONPATH=/app` (Docker)
- `PYTHONUNBUFFERED=1` (Docker)
- `GATOWIKI_LOG_LEVEL` (Logging control)
- `.env` files supported via python-dotenv

---

## Development Guidelines

### Adding New Language Support

To add support for a new programming language:

1. **Create language analyzer** in `gatowiki/src/core/dependency_analyzer/analyzers/new_language.py`:
   ```python
   from .base import BaseAnalyzer

   class NewLanguageAnalyzer(BaseAnalyzer):
       def __init__(self):
           super().__init__("new_language")

       def extract_dependencies(self, ast_node):
           # Implement dependency extraction
           pass

       def extract_components(self, ast_node):
           # Implement component extraction
           pass
   ```

2. **Register analyzer** in `ast_parser.py`:
   ```python
   LANGUAGE_ANALYZERS = {
       # ... existing languages ...
       "new_language": NewLanguageAnalyzer,
   }
   ```

3. **Add file extensions** in configuration
4. **Add tests** for the new language

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gatowiki tests/

# Run specific test file
pytest tests/test_dependency_analyzer.py
```

**Note**: Tests directory currently excluded from repo (.gitignore), though testing infrastructure is configured in pyproject.toml.

### Code Quality Commands

```bash
# Format code
black gatowiki/

# Type checking
mypy gatowiki/

# Linting
ruff gatowiki/

# Verbose logging
gatowiki analyze --verbose
export GATOWIKI_LOG_LEVEL=DEBUG
```

---

## Important CLI Commands

### Analysis

```bash
# Run dependency analysis and module clustering
gatowiki analyze

# Custom output directory
gatowiki analyze --output ./documentation

# Filter by languages
gatowiki analyze --languages python,typescript

# Limit module depth
gatowiki analyze --max-depth 3

# Enable verbose logging
gatowiki analyze --verbose
```

**What it does**: Parses source code, builds dependency graphs, clusters modules hierarchically, generates JSON artifacts. **Does NOT call LLM APIs**.

### Documentation Generation (GitHub Copilot)

Open GitHub Copilot Chat and use simple commands:

```
Generate documentation              # Full repository
Update documentation                # Skip existing docs
Document the cli module             # Single module
Regenerate all documentation        # Overwrite all
```

### Publishing

```bash
# Generate HTML viewer
gatowiki publish --github-pages

# Create gh-pages branch
gatowiki publish --github-pages --create-branch

# Custom output
gatowiki publish --output ./documentation --github-pages
```

### Configuration

```bash
# Set default output directory
gatowiki config set --output ./docs

# Show current configuration
gatowiki config show
```

---

## Output Structure

Generated documentation files:

```
./docs/
├── overview.md               # Repository overview (start here!)
├── module1.md                # Module documentation
├── module2.md                # Additional modules...
├── module_tree.json          # Hierarchical module structure (from analyze)
├── first_module_tree.json    # Initial clustering result (from analyze)
├── analysis_metadata.json    # Analysis statistics (from analyze)
└── index.html                # Interactive viewer (from publish)
```

**Analysis Phase**: Generates `module_tree.json`, `first_module_tree.json`, `analysis_metadata.json`
**Documentation Phase**: Generates `overview.md`, `module_*.md` files
**Publishing Phase**: Generates `index.html` for GitHub Pages

---

## Performance & Scalability

### Target Scale

- **Tested Range**: 86K - 1.4M lines of code
- **Supported Languages**: 7 languages (Python, Java, JavaScript, TypeScript, C, C++, C#)
- **Performance Results** (from research paper):
  - High-level languages (Python, JS, TS): **79.14%** quality score
  - Managed languages (C#, Java): **68.84%** quality score
  - Systems languages (C, C++): **53.24%** quality score

### Scalability Features

- Hierarchical decomposition for arbitrary codebase sizes
- Dynamic agent delegation for complex modules
- Memory-conscious processing with streaming
- Caching system for redundant operations (in progress)
- Parallel module processing supported

---

## Security & Quality

### Security Measures

- Credential storage via system keyring (not in code)
- Path validation to prevent directory traversal
- Symlink detection and rejection
- Repository path validation and cleanup
- Safe file I/O operations with error handling

### Quality Assurance

- Mermaid diagram validation via Node.js
- Type hints with MyPy (optional enforcement)
- Code formatting with Black (100-char lines)
- Linting with Ruff
- Coverage reporting with pytest-cov

---

## Git Workflow & Session Completion

### Session Close Protocol (MANDATORY)

**CRITICAL**: Before saying "done" or "complete", you MUST run this checklist:

```bash
1. git status              # Check what changed
2. git add <files>         # Stage code changes
3. bd sync                 # Commit beads changes
4. git commit -m "..."     # Commit code
5. bd sync                 # Commit any new beads changes
6. git push                # Push to remote
```

**Work is NOT complete until `git push` succeeds.**

### Git Conventions

- **Main branch**: `main` (primary development)
- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Issue Tracking**: Beads issue tracker (`.beads/`)
- **Git worktrees**: Used for feature isolation

---

## Constitution Principles (AGENTS.md)

GatoWiki follows six core principles that govern all development:

1. **Modular Architecture** - Clear separation between analysis, generation, and presentation layers
2. **CLI-First Design** - All core functionality accessible through clean CLI
3. **Multi-Language Support** - 7 languages with extensibility for future additions
4. **AI-Powered Intelligence** - LLM capabilities with provider independence
5. **Hierarchical Documentation** - Preserves architectural context across multiple granularities
6. **Open Source & Research-Driven** - Transparency, reproducibility, community contributions

**Constitution Authority**: These principles supersede all conflicting practices or documentation.

---

## Research & Academic Context

### Published Research

- **Paper**: arXiv 2510.24428
- **Benchmark**: CodeWikiBench (first repository-level documentation benchmark)
- **Evaluation**: 21 repositories across all supported languages

### Notable Tested Repositories

- All-Hands-AI--OpenHands (Python, 229K LOC) - 82.45% quality
- puppeteer--puppeteer (TypeScript, 136K LOC) - 83.00% quality
- sveltejs--svelte (JavaScript, 125K LOC) - 71.96% quality
- Unity-Technologies--ml-agents (C#, 86K LOC) - 79.78% quality
- elastic--logstash (Java, 117K LOC) - 57.90% quality

---

## Docker Deployment

### Docker Configuration

**Dockerfile**: `docker/Dockerfile` (Python 3.12)
**Compose**: `docker/docker-compose.yml` (Service orchestration)
**Environment**: `docker/env.example` (Environment variable template)

```bash
# Build and run with Docker Compose
docker-compose up -d

# Run analysis in container
docker exec gatowiki gatowiki analyze
```

---

## Important Files & Their Purposes

| File | Purpose |
|------|---------|
| `gatowiki/cli/main.py` | CLI entry point with Click framework |
| `gatowiki/src/core/documentation_generator.py` | Main orchestrator for analysis pipeline |
| `gatowiki/src/core/dependency_analyzer/ast_parser.py` | AST parsing orchestrator for all languages |
| `gatowiki/src/core/cluster_modules.py` | Hierarchical module decomposition logic |
| `pyproject.toml` | Python project metadata and dependencies |
| `requirements.txt` | Complete dependency list (160+ packages) |
| `AGENTS.md` | Constitution and governing principles |
| `README.md` | Main user documentation |
| `DEVELOPMENT.md` | Developer guide and architecture |

---

## Common Issues & Debugging

### Enable Verbose Logging

```bash
gatowiki analyze --verbose
export GATOWIKI_LOG_LEVEL=DEBUG
```

### Tree-sitter Parser Errors

- Ensure language parsers are properly installed
- Check file encoding (UTF-8 expected)

### Memory Issues with Large Repositories

- Adjust module decomposition threshold
- Increase delegation depth limit

---

## Key Considerations for AI Assistants

### When Working on This Codebase

1. **NEVER generate or modify code without reading the relevant files first**
2. **Always check constitution compliance** (AGENTS.md) before making architectural changes
3. **Use the beads issue tracker** (`bd` commands) for multi-session work
4. **Follow the CLI-first design principle** - all functionality must be accessible via CLI
5. **Maintain language analyzer independence** - language-specific code should not leak into generic components
6. **Test on multiple languages** when changing core analysis logic
7. **Validate Mermaid diagrams** using Node.js tooling
8. **Document breaking changes** with migration guides
9. **Always push to remote** before ending a session (see Session Close Protocol)

### Code Modification Guidelines

- Prefer editing existing files over creating new ones
- Follow Black formatting (100-char lines)
- Add type hints for new functions
- Update relevant documentation (README.md, DEVELOPMENT.md)
- Test changes with `pytest` if tests exist
- Run linters (`black`, `ruff`, `mypy`) before committing

### Architecture Boundaries

- **CLI Layer** (`cli/`) - User-facing commands only
- **Service Layer** (`src/core/documentation_generator.py`) - Orchestration only
- **Analysis Layer** (`src/core/dependency_analyzer/`) - Code understanding only
- **Web Layer** (`src/web/`) - Web interface only

**Do not mix concerns across these boundaries.**

---

## Version History

- **v0.25.5** (Current) - GitHub Copilot integration, removed direct LLM API calls
- **v0.25.0** - Major architectural update
- **v2.0** - Configuration version with GitHub Copilot support

---

## Additional Resources

- **GitHub Copilot Integration**: `docs/github-copilot-integration.md`
- **Agent Customization**: `docs/customizing-agents.md`
- **Docker Deployment**: `docker/DOCKER_README.md`
- **Research Paper**: https://arxiv.org/abs/2510.24428
- **Repository**: https://github.com/eitatech/gatomia-wiki

---

**Last Updated**: 2026-01-14
**Analyzed Version**: 0.25.5
