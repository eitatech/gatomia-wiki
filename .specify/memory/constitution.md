<!--
SYNC IMPACT REPORT
==================
Version: 0.0.0 → 1.0.0
Change Type: MAJOR (Initial constitution establishment)

Principles Defined:
  - I. Modular Architecture (NEW)
  - II. CLI-First Design (NEW)
  - III. Multi-Language Support (NEW)
  - IV. AI-Powered Intelligence (NEW)
  - V. Hierarchical Documentation (NEW)
  - VI. Open Source & Research-Driven (NEW)

Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section verified
  ✅ spec-template.md - Requirements alignment verified
  ✅ tasks-template.md - Task categorization verified
  ✅ agent-file-template.md - Generic guidance verified
  ✅ checklist-template.md - Generic checklist verified

Follow-up TODOs: None

Rationale for MAJOR version:
  - First formal constitution establishing core governance
  - Defines foundational principles for all future development
  - Establishes architectural boundaries and quality standards
-->

# GatoWiki Constitution

## Core Principles

### I. Modular Architecture

The GatoWiki system MUST maintain clear separation between analysis, generation, and presentation layers.

**Non-Negotiable Rules:**
- Backend components (`src/core/`) handle all code analysis, dependency graph construction, and agent orchestration
- CLI components (`cli/`) provide user-facing interfaces with clean command structure
- Frontend components (`src/web/`) focus solely on web application and visualization
- Each module MUST be independently testable with minimal cross-dependencies
- Shared utilities go in designated utility packages, never duplicated across modules

**Rationale:** Modular architecture enables parallel development, easier maintenance, and independent testing of core functionality. This separation allows researchers to extend analysis capabilities without touching CLI or web interfaces.

### II. CLI-First Design

All core functionality MUST be accessible through a clean, intuitive command-line interface.

**Non-Negotiable Rules:**
- Primary commands: `config` (configuration management) and `generate` (documentation generation)
- Configuration stored securely: API keys in system keychain, settings in `~/.gatowiki/config.json`
- Output to stdout for success messages, stderr for errors
- Support both JSON and human-readable formats for all outputs
- Progress tracking MUST provide clear feedback for long-running operations
- All CLI commands MUST have comprehensive help text and examples

**Rationale:** CLI-first design ensures GatoWiki can be integrated into CI/CD pipelines, automated workflows, and developer toolchains. Research users can script experiments; production users can automate documentation updates.

### III. Multi-Language Support

The system MUST support comprehensive code analysis across seven programming languages with extensibility for future additions.

**Non-Negotiable Rules:**
- Supported languages: Python, Java, JavaScript, TypeScript, C, C++, C#
- Each language MUST have a dedicated analyzer in `src/core/dependency_analyzer/analyzers/`
- All analyzers MUST inherit from `BaseAnalyzer` and implement standard interfaces
- Tree-sitter parsers MUST be used for AST parsing to ensure consistency
- Adding a new language requires: analyzer implementation, file extension registration, and validation tests
- Language-specific analysis MUST NOT leak into generic components

**Rationale:** Multi-language support is a core differentiator for GatoWiki. Standardized analyzer interfaces enable consistent quality across languages and simplify addition of new language support.

### IV. AI-Powered Intelligence

All documentation generation MUST leverage LLM capabilities while maintaining provider independence and quality control.

**Non-Negotiable Rules:**
- LLM interactions centralized in `src/core/llm_services.py`
- Support multiple providers through standardized interfaces (Anthropic, OpenAI, etc.)
- Agent system (`agent_orchestrator.py`) handles recursive documentation generation with dynamic delegation
- Agent tools provide reusable primitives: code reading, dependency traversal, documentation editing
- All prompts MUST be clear, context-aware, and include error handling
- Generated content MUST be validated (mermaid diagrams validated via Node.js tooling)

**Rationale:** Provider independence protects against vendor lock-in and API changes. Centralized LLM services enable consistent error handling, retry logic, and cost optimization. Validation ensures generated artifacts are usable.

### V. Hierarchical Documentation

Documentation generation MUST follow a hierarchical decomposition strategy that preserves architectural context.

**Non-Negotiable Rules:**
- Codebase partitioned into coherent modules via `cluster_modules.py`
- Module clustering preserves feature boundaries and architectural relationships
- Documentation generated at multiple granularities: repository, module, component
- Cross-module references MUST be tracked and resolved
- Output structure: `overview.md` (repository-level), module-specific files, `module_tree.json` (hierarchy)
- Visual artifacts (architecture diagrams, data flows, sequence diagrams) MUST accompany textual documentation

**Rationale:** Hierarchical approach enables GatoWiki to handle repositories of arbitrary size (tested up to 1.4M LOC). Preserving context across levels ensures comprehensive understanding rather than isolated component documentation.

### VI. Open Source & Research-Driven

GatoWiki exists as both a production tool and research artifact, with transparency and reproducibility as core values.

**Non-Negotiable Rules:**
- All code licensed under MIT License
- Research methodology documented in published papers (arXiv 2510.24428)
- Benchmark data and evaluation framework (GatoWikiBench) publicly available
- Breaking changes MUST be documented with migration guides
- Contributions welcome via GitHub with clear contributing guidelines
- Version numbers follow semantic versioning: MAJOR.MINOR.PATCH

**Rationale:** Open source development enables community contributions and academic validation. Research grounding ensures methodological rigor. Transparency builds trust with both researchers and practitioners.

## Technology Standards

### Required Stack

- **Language**: Python 3.12+ (type hints encouraged, PEP 8 compliance required)
- **CLI Framework**: Click (declarative command definitions, comprehensive help system)
- **Web Framework**: FastAPI (async support, automatic API documentation)
- **Code Analysis**: Tree-sitter (consistent AST parsing across languages)
- **LLM Integration**: LiteLLM + OpenAI SDK (provider abstraction)
- **Dependency Management**: pip with `pyproject.toml` (setuptools build backend)
- **Diagram Validation**: Node.js + mermaid-cli (quality assurance for generated diagrams)

### Code Quality

- **Formatting**: Black (line length: 100 characters, Python 3.12 target)
- **Type Checking**: MyPy (enabled but not enforced for all functions to balance velocity)
- **Linting**: Ruff (Python 3.12 target, 100 character line length)
- **Testing**: pytest with coverage reporting (when tests exist; test-first encouraged but not mandated)
- **Logging**: Rich library for enhanced terminal output; structured logging for web application

### Performance & Scale

- **Target Scale**: Repositories from 86K to 1.4M lines of code
- **Memory Management**: Streaming where possible; chunk large files for LLM processing
- **Concurrency**: Parallel module processing supported; agent delegation for complex modules
- **Caching**: Results cached to avoid redundant processing (implementation in progress)

## Development Workflow

### Feature Development

1. **Specification First**: Create feature spec in `.specify/specs/[###-feature]/spec.md`
2. **Planning**: Generate implementation plan via `.specify/templates/plan-template.md`
3. **Task Breakdown**: Create task list following `.specify/templates/tasks-template.md`
4. **Implementation**: Follow task order; commit frequently; test continuously
5. **Documentation**: Update README.md, DEVELOPMENT.md if architecture affected
6. **Validation**: Run linters, verify CLI commands, test on sample repositories

### Code Review Standards

- All changes require review (even from primary maintainers)
- Verify constitution compliance: modularity, CLI-first, language support, provider independence
- Check for performance implications on large repositories
- Ensure backward compatibility or document breaking changes
- Validate documentation updates match code changes

### Release Process

- Version increments follow semantic versioning (MAJOR.MINOR.PATCH)
- MAJOR: Breaking API changes, removed language support, architectural rewrites
- MINOR: New language support, new CLI commands, new analysis capabilities
- PATCH: Bug fixes, documentation improvements, performance optimizations
- Tag releases in Git with version number and changelog
- Update version in `pyproject.toml` and `gatowiki/__init__.py`

## Governance

### Constitution Authority

This constitution supersedes all conflicting practices, documentation, or conventions. When in doubt, constitution principles take precedence.

### Amendment Process

1. Propose amendment with clear rationale and impact analysis
2. Document affected templates and code areas
3. Obtain approval from project maintainers
4. Update constitution with version bump (MAJOR/MINOR/PATCH based on impact)
5. Propagate changes to dependent templates in `.specify/templates/`
6. Update DEVELOPMENT.md and README.md if user-facing changes
7. Commit with message: `docs: amend constitution to vX.Y.Z (summary)`

### Complexity Justification

Complexity beyond these principles MUST be justified in feature specs. Unjustified complexity will be rejected.

**Examples requiring justification:**
- Additional architectural layers beyond modular separation
- New configuration storage mechanisms beyond keychain + JSON
- Alternative AST parsing approaches beyond Tree-sitter
- LLM provider-specific code paths outside abstraction layer

### Compliance Review

- Feature plans MUST include "Constitution Check" section
- Pull requests MUST verify no principle violations
- Template updates MUST maintain alignment with constitution
- Runtime guidance in `.specify/templates/agent-file-template.md` for development sessions

**Version**: 1.0.0 | **Ratified**: 2025-09-05 | **Last Amended**: 2025-12-09
