<h1 align="center">GatomIA Code Wiki: Evaluating AI's Ability to Generate Holistic Documentation for Large-Scale Codebases</h1>

<p align="center">
  <strong>AI-Powered Repository Documentation Generation</strong> • <strong>Multi-Language Support</strong> • <strong>Architecture-Aware Analysis</strong>
</p>

<p align="center">
  Generate holistic, structured documentation for large-scale codebases • Cross-module interactions • Visual artifacts and diagrams
</p>

<p align="center">
  <a href="https://python.org/"><img alt="Python version" src="https://img.shields.io/badge/python-3.12+-blue?style=flat-square" /></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" /></a>
  <a href="https://github.com/eitatech/gatomia-wiki/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/eitatech/gatomia-wiki?style=flat-square" /></a>
  <a href="https://arxiv.org/abs/2510.24428"><img alt="arXiv" src="https://img.shields.io/badge/arXiv-2510.24428-b31b1b?style=flat-square" /></a>
</p>

<p align="center">
  <a href="#quick-start"><strong>Quick Start</strong></a> •
  <a href="#cli-commands"><strong>CLI Commands</strong></a> •
  <a href="#documentation-output"><strong>Output Structure</strong></a> •
  <a href="https://arxiv.org/abs/2510.24428"><strong>Paper</strong></a>
</p>

---

> **⚠️ IMPORTANT: GatoWiki v0.25.5 requires GitHub Copilot**  
> This version uses GitHub Copilot agents instead of direct API calls.  
> [Integration Guide](./docs/github-copilot-integration.md)

## Quick Start

### 1. Install GatoWiki

```bash
# Install from source
pip install git+https://github.com/eitatech/gatomia-wiki.git

# Verify installation
gatowiki --version  # Should show 2.0.0+
```

### 2. Verify GitHub Copilot Access

**Prerequisites:**
- GitHub Copilot subscription (Individual, Business, or Enterprise)
- IDE with Copilot support (VS Code, IntelliJ, etc.)

```bash
# No API key configuration needed!
# GitHub Copilot handles authentication
```

### 3. Generate Documentation

Open **GitHub Copilot Chat** in your IDE and simply say:

```
Generate documentation
```

That's it! The agent will automatically:
1. Run `gatowiki analyze` if needed
2. Detect all modules in your repository
3. Generate comprehensive documentation
4. Create architecture diagrams

**Other commands:**
```
Update documentation           # Skip existing
Document the cli module        # Single module
```

### 4. Publish to GitHub Pages (Optional)

```bash
gatowiki publish --github-pages --create-branch
```

### Workflow (v0.25.5)

```
┌────────────────────────────────────────────────────┐
│     "Generate documentation"                       │
│              │                                     │
│              ▼                                     │
│  ┌────────────────┐   ┌───────────────────────┐    │
│  │ Auto-analyze   │──▶│ Generate docs for     │    │
│  │ (if needed)    │   │ each module           │    │
│  └────────────────┘   └───────────────────────┘    │
│                              │                     │
│                              ▼                     │
│                     ┌───────────────────────┐      │
│                     │ Write files to        │      │
│                     │ docs/*.md             │      │
│                     └───────────────────────┘      │
└────────────────────────────────────────────────────┘
              GitHub Copilot Agent
```

---

## What is GatomIA Code Wiki?

GatoWiki is an open-source framework for **automated repository-level documentation** across seven programming languages. It generates holistic, architecture-aware documentation that captures not only individual functions but also their cross-file, cross-module, and system-level interactions.

### Key Innovations

| Innovation | Description | Impact |
|------------|-------------|--------|
| **Hierarchical Decomposition** | Dynamic programming-inspired strategy that preserves architectural context | Handles codebases of arbitrary size (86K-1.4M LOC tested) |
| **Recursive Agentic System** | Adaptive multi-agent processing with dynamic delegation capabilities | Maintains quality while scaling to repository-level scope |
| **Multi-Modal Synthesis** | Generates textual documentation, architecture diagrams, data flows, and sequence diagrams | Comprehensive understanding from multiple perspectives |

### Supported Languages

**Python** • **Java** • **JavaScript** • **TypeScript** • **C** • **🔧 C++** • **C#**

---

## CLI Commands

### Code Analysis

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

**What it does:**
- Parses source code with Tree-sitter
- Builds dependency graphs
- Clusters modules hierarchically
- Generates `module_tree.json` and `first_module_tree.json`
- **Does NOT call any LLM APIs**

### Documentation Generation (via GitHub Copilot)

Open GitHub Copilot Chat and use simple commands:

```
Generate documentation              # Full repository
Update documentation                # Skip existing docs
Document the cli module             # Single module
Regenerate all documentation        # Overwrite all
```

The agent automatically:
- Runs `gatowiki analyze` if module_tree.json is missing
- Detects all modules in your codebase
- Generates comprehensive docs with diagrams
- Skips already-documented modules (unless regenerating)

### Publishing

```bash
# Generate HTML viewer
gatowiki publish --github-pages

# Create gh-pages branch
gatowiki publish --github-pages --create-branch

# Custom output
gatowiki publish --output ./documentation --github-pages
```

### Configuration (Optional)

```bash
# Set default output directory
gatowiki config set --output ./docs

# Show current configuration
gatowiki config show
```

**Note:** API key configuration removed in v0.25.5. GitHub Copilot handles authentication.

---

## Documentation Output

Generated documentation includes both **textual descriptions** and **visual artifacts** for comprehensive understanding.

### Textual Documentation
- Repository overview with architecture guide
- Module-level documentation with API references
- Usage examples and implementation patterns
- Cross-module interaction analysis

### Visual Artifacts
- System architecture diagrams (Mermaid)
- Data flow visualizations
- Dependency graphs and module relationships
- Sequence diagrams for complex interactions

### Output Structure

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

**Analysis Phase** (`gatowiki analyze`):
- Generates: `module_tree.json`, `first_module_tree.json`, `analysis_metadata.json`

**Documentation Phase** (GitHub Copilot):
- Generates: `overview.md`, `module1.md`, `module2.md`, etc.

**Publishing Phase** (`gatowiki publish`):
- Generates: `index.html` for GitHub Pages

---

## Experimental Results

GatoWiki has been evaluated on **CodeWikiBench**, the first benchmark specifically designed for repository-level documentation quality assessment.

### Performance by Language Category

| Language Category | GatoWiki (Sonnet-4) | DeepWiki | Improvement |
|-------------------|---------------------|----------|-------------|
| High-Level (Python, JS, TS) | **79.14%** | 68.67% | **+10.47%** |
| Managed (C#, Java) | **68.84%** | 64.80% | **+4.04%** |
| Systems (C, C++) | 53.24% | 56.39% | -3.15% |
| **Overall Average** | **68.79%** | **64.06%** | **+4.73%** |

### Results on Representative Repositories

| Repository | Language | LOC | GatoWiki-Sonnet-4 | DeepWiki | Improvement |
|------------|----------|-----|-------------------|----------|-------------|
| All-Hands-AI--OpenHands | Python | 229K | **82.45%** | 73.04% | **+9.41%** |
| puppeteer--puppeteer | TypeScript | 136K | **83.00%** | 64.46% | **+18.54%** |
| sveltejs--svelte | JavaScript | 125K | **71.96%** | 68.51% | **+3.45%** |
| Unity-Technologies--ml-agents | C# | 86K | **79.78%** | 74.80% | **+4.98%** |
| elastic--logstash | Java | 117K | **57.90%** | 54.80% | **+3.10%** |

**View comprehensive results:** See [paper](https://arxiv.org/abs/2510.24428) for complete evaluation on 21 repositories spanning all supported languages.

---

## How It Works

### Architecture Overview

GatoWiki employs a three-stage process for comprehensive documentation generation:

1. **Hierarchical Decomposition**: Uses dynamic programming-inspired algorithms to partition repositories into coherent modules while preserving architectural context across multiple granularity levels.

2. **Recursive Multi-Agent Processing**: Implements adaptive multi-agent processing with dynamic task delegation, allowing the system to handle complex modules at scale while maintaining quality.

3. **Multi-Modal Synthesis**: Integrates textual descriptions with visual artifacts including architecture diagrams, data-flow representations, and sequence diagrams for comprehensive understanding.

### Data Flow

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Codebase      │───▶│  Hierarchical    │───▶│  Multi-Agent    │
│   Analysis      │    │  Decomposition   │    │  Processing     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Visual        │◀───│  Multi-Modal     │◀───│  Structured     │
│   Artifacts     │    │  Synthesis       │    │  Content        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

---

## Requirements

- **Python 3.12+**
- **GitHub Copilot** (Individual, Business, or Enterprise subscription)
- **IDE with Copilot support** (VS Code, IntelliJ IDEA, Visual Studio, etc.)
- **Node.js** (optional, for Mermaid diagram validation)
- **Git** (optional, for branch creation features)

---

## Additional Resources

### Documentation & Guides

**GitHub Copilot Integration (v0.25.5+)**:
- 📖 **[GitHub Copilot Integration Guide](./docs/github-copilot-integration.md)** - Complete workflow, setup, and usage guide
- 🔄 **[Migration Guide](./docs/migration-to-github-copilot.md)** - Migrating from API version to v0.25.5
- 🎨 **[Agent Customization Guide](./docs/customizing-agents.md)** - Customize agents for your team

**General Resources**:
- 🐳 **[Docker Deployment](docker/DOCKER_README.md)** - Containerized deployment instructions
- 🛠️ **[Development Guide](DEVELOPMENT.md)** - Project structure, architecture, and contributing guidelines
- 📊 **[GatoWikiBench](https://github.com/eitatech/gatomia-wiki-bench)** - Repository-level documentation benchmark
- 🎬 **[Live Demo](https://demo.gatomia.xyz)** - Interactive demo and examples

### Academic Resources
- **[Paper](https://arxiv.org/abs/2510.24428)** - Full research paper with detailed methodology and results from the original research that GatoWiki was created.
---

## License

This project is licensed under the MIT License.
