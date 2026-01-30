# Installation Guide

## 📦 Package Contents

This package contains:

```
codewiki-agent-claude-code/
├── codewiki_agent.md              # SubAgent definition for Claude Code
├── codewiki_agent_executor.py     # Python executor script
├── codewiki_analyzer.py           # Code analyzer
├── orchestrator.py                # Documentation orchestrator
├── .codewiki.example.yaml         # Example configuration
├── README.md                      # Complete usage guide
├── INDEX.md                       # Quick reference
└── INSTALL.md                     # This file
```

## 📍 Where Files Should Be

### Option A: Per-Repository Installation (Recommended)

For documenting a specific repository:

```
your-repository/
├── .claude/
│   ├── agents/
│   │   └── codewiki_agent.md          # ← Agent definition goes here
│   └── scripts/
│       ├── codewiki_agent_executor.py # ← Executor goes here
│       ├── codewiki_analyzer.py       # ← Analyzer goes here
│       └── orchestrator.py            # ← Orchestrator goes here
│
├── .codewiki.yaml                     # ← Optional config (copy from .codewiki.example.yaml)
│
├── src/                               # Your source code
├── docs/                              # Generated documentation (created by agent)
└── .codewiki/                         # Analysis cache (created by agent)
```

**Installation commands:**

```bash
# Navigate to your repository
cd /path/to/your-repository

# Create directories
mkdir -p .claude/agents .claude/scripts

# Copy agent files
cp /path/to/package/codewiki_agent.md .claude/agents/
cp /path/to/package/codewiki_agent_executor.py .claude/scripts/
cp /path/to/package/codewiki_analyzer.py .claude/scripts/
cp /path/to/package/orchestrator.py .claude/scripts/

# Optional: Copy and customize configuration
cp /path/to/package/.codewiki.example.yaml .codewiki.yaml
```

### Option B: Global Installation

For using the agent across all repositories:

```
~/.claude/
├── agents/
│   └── codewiki_agent.md              # ← Agent definition
└── scripts/
    ├── codewiki_agent_executor.py     # ← Executor
    ├── codewiki_analyzer.py           # ← Analyzer
    └── orchestrator.py                # ← Orchestrator
```

**Installation commands:**

```bash
# Create global directories
mkdir -p ~/.claude/agents ~/.claude/scripts

# Copy agent files
cp /path/to/package/codewiki_agent.md ~/.claude/agents/
cp /path/to/package/codewiki_agent_executor.py ~/.claude/scripts/
cp /path/to/package/codewiki_analyzer.py ~/.claude/scripts/
cp /path/to/package/orchestrator.py ~/.claude/scripts/
```

**Per-repository configuration:**

Even with global installation, you can have per-repo configs:

```bash
# In each repository
cd /path/to/repository
cp /path/to/package/.codewiki.example.yaml .codewiki.yaml
# Edit .codewiki.yaml with your preferences
```

## 🎯 Configuration File (.codewiki.yaml)

### Location

The `.codewiki.yaml` file should be at the **root of your repository**:

```
your-repository/
├── .codewiki.yaml       # ← Configuration file here
├── src/
├── docs/
└── ...
```

### Creating the Configuration

1. **Copy the example file:**
   ```bash
   cp .codewiki.example.yaml .codewiki.yaml
   ```

2. **Edit as needed:**
   ```bash
   nano .codewiki.yaml
   # or
   code .codewiki.yaml
   ```

3. **Basic customization:**
   ```yaml
   output:
     directory: ./docs              # Where to generate docs
     language: auto                # or en-US, pt-BR, es-ES
   
   documentation:
     include_diagrams: true         # Include Mermaid diagrams
     detail_level: comprehensive    # brief|standard|comprehensive
   
   analysis:
     ignore_paths:                  # Paths to ignore
       - node_modules/
       - venv/
       - .git/
       - build/
   ```

### Configuration is Optional

**If `.codewiki.yaml` doesn't exist**, the agent uses defaults:
- Output: `./docs/`
- Language: Auto-detect from user
- Diagrams: Enabled
- Detail level: Comprehensive

## 🔍 Analysis Files Format

### File Naming Conventions

CodeWiki analysis can generate files in different naming formats:

**Standard format:**
```
module_tree.json
dependency_graph.json
```

**Project-prefixed format (CodeWiki default with `codewiki analyze`):**
```
temp/
├── dependency_graphs/
│   └── ProjectName_dependency_graph.json
└── ProjectName_module_tree.json
```

**Alternative formats:**
```
ProjectName_module_tree.json
ProjectName_dependency_graph.json
```

**Directory structure variations:**
```
# CodeWiki default output
temp/
├── dependency_graphs/
│   └── ProjectName_dependency_graph.json
└── ProjectName_module_tree.json

# Alternative locations
docs/
├── dependency_graph.json              # Standard location
└── dependency_graphs/                 # Alternative subdirectory
    └── ProjectName_dependency_graph.json
```

### Detection Logic

The agent automatically detects files in this order:

1. **CodeWiki default output** (most common)
   - `temp/dependency_graphs/ProjectName_dependency_graph.json`
   - `temp/ProjectName_module_tree.json`

2. **Project-prefixed in docs/dependency_graphs/** (specific)
   - `docs/dependency_graphs/ProjectName_dependency_graph.json`

3. **Project-prefixed in directory** (specific)
   - `docs/ProjectName_dependency_graph.json`

4. **Standard name** (generic)
   - `docs/dependency_graph.json`

5. **Other locations**
   - `wiki/`, `.codewiki/`, `./`

**You don't need to rename or move files!** The agent finds them automatically regardless of naming convention or location.

## ✅ Verification

### After Installation

**For per-repository installation:**

```bash
# Check agent is installed
ls .claude/agents/codewiki_agent.md

# Check scripts are installed
ls .claude/scripts/codewiki_*.py
ls .claude/scripts/orchestrator.py
```

**For global installation:**

```bash
# Check agent is installed
ls ~/.claude/agents/codewiki_agent.md

# Check scripts are installed
ls ~/.claude/scripts/codewiki_*.py
ls ~/.claude/scripts/orchestrator.py
```

### Test the Installation

In Claude Code, simply say:

```
generate documentation
```

If everything is installed correctly, the agent will:
1. ✅ Recognize the command
2. ✅ Start the documentation process
3. ✅ Generate complete documentation in `./docs/`

## 🚀 Quick Start After Installation

### 1. Basic Usage

In Claude Code:
```
generate documentation
```

### 2. With Custom Config

```bash
# Create config
cp .codewiki.example.yaml .codewiki.yaml

# Edit as needed
nano .codewiki.yaml

# Generate docs
# In Claude Code:
generate documentation
```

### 3. View Generated Docs

```bash
# Open main README
code docs/README.md

# Or browse
ls docs/
```

## 📂 Directory Structure After First Run

After running the agent for the first time:

```
your-repository/
├── .claude/
│   ├── agents/
│   │   └── codewiki_agent.md
│   └── scripts/
│       ├── codewiki_agent_executor.py
│       ├── codewiki_analyzer.py
│       └── orchestrator.py
│
├── .codewiki/                         # ← Created by agent
│   ├── module_tree.json               # Analysis results
│   └── dependency_graph.json          # Dependency mapping
│
├── docs/                              # ← Created by agent OR existing analysis
│   ├── dependency_graphs/             # CodeWiki may create this subdirectory
│   │   └── ProjectName_dependency_graph.json  # Project-prefixed file
│   ├── README.md                      # Repository overview
│   ├── INDEX.md                       # Navigation index
│   ├── architecture/                  # Architecture docs
│   │   ├── overview.md
│   │   ├── patterns.md
│   │   └── diagrams/
│   └── modules/                       # Module documentation
│       ├── src/
│       │   ├── fe/
│       │   │   └── README.md
│       │   └── be/
│       │       └── README.md
│       └── cli/
│           └── README.md
│
├── .codewiki.yaml                     # ← Optional: Your config
├── src/                               # Your source code
└── ...
```

## 🔧 Troubleshooting Installation

### Issue: "Agent not found"

**Symptoms:**
```
User: generate documentation
Claude: I don't have access to that capability
```

**Solution:**
1. Verify agent file exists:
   ```bash
   ls .claude/agents/codewiki_agent.md
   # or
   ls ~/.claude/agents/codewiki_agent.md
   ```

2. If missing, reinstall:
   ```bash
   cp /path/to/package/codewiki_agent.md .claude/agents/
   ```

### Issue: "Python scripts not found"

**Symptoms:**
```
Error: codewiki_agent_executor.py not found
```

**Solution:**
1. Verify scripts exist:
   ```bash
   ls .claude/scripts/codewiki_*.py
   ```

2. If missing, reinstall:
   ```bash
   cp /path/to/package/*.py .claude/scripts/
   ```

### Issue: "Configuration not loading"

**Symptoms:**
Documentation generates with wrong settings

**Solution:**
1. Verify config location:
   ```bash
   ls .codewiki.yaml  # Must be at repository root
   ```

2. Verify YAML syntax:
   ```bash
   python3 -c "import yaml; yaml.safe_load(open('.codewiki.yaml'))"
   ```

## 🎓 Next Steps

After installation:

1. **Generate first documentation:**
   ```
   generate documentation
   ```

2. **Review output:**
   ```bash
   code docs/README.md
   ```

3. **Customize config (optional):**
   ```bash
   nano .codewiki.yaml
   ```

4. **Regenerate with new settings:**
   ```
   clean and regenerate
   ```

5. **Commit documentation:**
   ```bash
   git add docs/ .codewiki.yaml
   git commit -m "docs: Add comprehensive documentation"
   git push
   ```

## 📚 Additional Resources

- **Complete guide:** See `README.md`
- **Quick reference:** See `INDEX.md`
- **Example config:** See `.codewiki.example.yaml`
- **Agent definition:** See `codewiki_agent.md`

## 💡 Tips

1. **Start with per-repository installation** - easier to customize per project
2. **Create .codewiki.yaml only if you need customization** - defaults work well
3. **Add .codewiki/ to .gitignore** - it's just cache
4. **Commit docs/ to git** - documentation should be versioned
5. **Use global installation** - only if you want same agent across all repos

## ✅ Installation Complete!

Your CodeWiki agent is ready to use!

In Claude Code, just say:
```
generate documentation
```

Happy documenting! 📚✨
