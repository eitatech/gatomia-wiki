---
inclusion: always
---

# Technology Stack

## Core Technologies

- **Python 3.12+**: Primary language (required minimum version)
- **Node.js**: Required for Mermaid diagram validation
- **Git**: For repository operations and branch management

## Key Frameworks & Libraries

### AI/LLM Integration
- **pydantic-ai**: Agent framework for AI orchestration
- **litellm**: Multi-provider LLM API abstraction (supports Anthropic, OpenAI, etc.)
- **openai**: OpenAI API client

### Code Analysis
- **tree-sitter**: AST-based parsing for multi-language support
- Language-specific parsers: `tree-sitter-python`, `tree-sitter-java`, `tree-sitter-javascript`, `tree-sitter-typescript`, `tree-sitter-c`, `tree-sitter-cpp`, `tree-sitter-c-sharp`

### Web Application
- **FastAPI**: Web framework for the web interface
- **Jinja2**: HTML templating
- **uvicorn**: ASGI server

### CLI
- **click**: Command-line interface framework
- **rich**: Terminal formatting and progress display
- **keyring**: Secure credential storage (uses system keychain)

### Utilities
- **GitPython**: Git operations
- **networkx**: Graph algorithms for dependency analysis
- **pydantic**: Data validation and settings management
- **PyYAML**: Configuration file handling
- **mermaid-py**: Mermaid diagram generation and validation

## Build System

- **setuptools**: Package building (defined in `pyproject.toml`)
- **pip**: Dependency management
- Package metadata in `pyproject.toml` following PEP 621

## Common Commands

### Installation
```bash
# Install from source
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"

# Install from GitHub
pip install git+https://github.com/eitatech/gatomia-wiki.git
```

### CLI Usage
```bash
# Configure API credentials
gatowiki config set --api-key <key> --base-url <url> --main-model <model> --cluster-model <model>

# Generate documentation
gatowiki generate

# Generate with GitHub Pages support
gatowiki generate --github-pages --create-branch

# Enable verbose logging
gatowiki generate --verbose
```

### Web Application
```bash
# Run web app locally
python gatowiki/run_web_app.py --host 0.0.0.0 --port 8000
```

### Docker
```bash
# Build image
docker-compose -f docker/docker-compose.yml build

# Start services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=gatowiki tests/

# Run specific test file
pytest tests/test_dependency_analyzer.py
```

### Code Quality
```bash
# Format code
black gatowiki/

# Type checking
mypy gatowiki/

# Linting
ruff check gatowiki/
```

## Configuration Files

- **pyproject.toml**: Package metadata, dependencies, tool configuration
- **requirements.txt**: Pinned dependencies for reproducible builds
- **~/.gatowiki/config.json**: User configuration (API settings)
- **.env**: Environment variables for Docker deployment
- **docker/docker-compose.yml**: Container orchestration

## Development Tools

- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-asyncio**: Async test support
- **black**: Code formatting (line length: 100)
- **mypy**: Static type checking
- **ruff**: Fast Python linter
