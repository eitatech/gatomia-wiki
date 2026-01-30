# CodeWiki Documentation Agent for Claude Code

## 🎯 What is This Agent?

An **autonomous SubAgent** for Claude Code that generates complete repository documentation automatically. You just need to say **"generate documentation"** and the agent does everything else!

## ✨ Features

✅ **Completely Autonomous**: Executes the entire process without intervention
✅ **Intelligent**: Detects existing files, installs dependencies automatically
✅ **Robust**: Complete error handling with automatic solutions
✅ **Informative**: Constant feedback on each step
✅ **Efficient**: Incremental update when documentation already exists
✅ **Multilingual**: Responds in user's language while keeping technical terms in English
✅ **Diagram-Only Updates**: Add diagrams to existing docs without rewriting content

## 🚀 How to Use in Claude Code

### Step 1: Add the Agent

1. **Copy files** to your repository:
   ```bash
   cp codewiki_agent.md your-repository/.claude/agents/
   cp codewiki_agent_executor.py your-repository/.claude/scripts/
   ```

2. **Or configure as global agent** in Claude Code:
   ```bash
   # Create global agents directory
   mkdir -p ~/.claude/agents
   
   # Copy agent
   cp codewiki_agent.md ~/.claude/agents/
   cp codewiki_agent_executor.py ~/.claude/scripts/
   ```

### Step 2: Use the Agent

**In Claude Code**, simply say:

```
generate documentation
```

Or any variation:
- "document the repository"
- "create documentation"
- "execute codewiki"
- "gerar documentação" (Portuguese)
- "generar documentación" (Spanish)

### Alternative: Update Diagrams Only

If you already have documentation and want to add/update **only diagrams** without regenerating text:

```
add diagrams to existing documentation
```

Or:
- "update documentation with diagrams only"
- "inject diagrams without regenerating"
- "adicionar apenas diagramas" (Portuguese)

**What this does:**
- ✅ Creates `docs/architecture/diagrams/` with 4 global diagrams
- ✅ Injects component diagrams into module docs
- ✅ Updates INDEX.md and README.md with architecture links
- ❌ Does NOT rewrite existing text content
- ❌ Does NOT remove manual customizations

See `ADICIONAR_APENAS_DIAGRAMAS.md` for detailed guide.

### Step 3: Follow Progress

The agent will show real-time progress:

```
🚀 Starting CodeWiki documentation generation...

1️⃣ Verifying analysis files...
   ✗ module_tree.json not found
   ✗ dependency_graph.json not found

2️⃣ Analyzing source code...
   📦 Installing CodeWiki...
   ✓ CodeWiki installed
   🔍 Executing analysis...
   ✓ Analysis completed (3.2s)

3️⃣ Generating documentation...
   [1/4] ✓ src/fe (18 components)
   [2/4] ✓ src/be (45 components)
   [3/4] ✓ cli (12 components)
   [4/4] ✓ src (3 components)

4️⃣ Creating indexes and navigation...
   ✓ README.md generated
   ✓ INDEX.md generated
   ✓ Diagrams created

✅ Documentation complete!

📁 ./docs/ (23 files, 3.2 MB)
📖 Start with: docs/README.md
```

## 🎨 Functionality

### Intelligent Detection

The agent searches for analysis files in multiple locations with support for **project-prefixed filenames**:

**Priority order:**
1. `temp/dependency_graphs/*_dependency_graph.json` (CodeWiki default output)
2. `temp/*_module_tree.json` (CodeWiki default output)
3. `docs/dependency_graphs/*_dependency_graph.json` (project-prefixed in subdirectory)
4. `docs/*_dependency_graph.json` (project-prefixed)
5. `docs/dependency_graph.json` (standard name)
6. `wiki/`, `.codewiki/`, `./` (root)

**CodeWiki default output structure** (`codewiki analyze`):
```
./temp/
├── dependency_graphs/
│   └── ProjectName_dependency_graph.json
└── ProjectName_module_tree.json
```

**Examples of detected files:**
- `temp/dependency_graphs/MyProject_dependency_graph.json` ✅ (CodeWiki default)
- `temp/MyProject_module_tree.json` ✅ (CodeWiki default)
- `docs/dependency_graphs/MyProject_dependency_graph.json` ✅
- `docs/MyProject_dependency_graph.json` ✅
- `docs/dependency_graph.json` ✅
- `.codewiki/module_tree.json` ✅

If found, uses existing ones. If not, generates automatically.

### Automatic Installation

If CodeWiki is not installed:
1. ✅ Clones repository automatically
2. ✅ Installs dependencies
3. ✅ Configures and executes

You don't need to do anything!

### Incremental Update

If documentation already exists:

```
📄 Existing documentation detected!

Verifying changes...
   ✓ module_tree.json (updated 2 days ago)
   ✓ Code modified in: src/be/

Options:
1. Update only src/be (fast ~30s)
2. Regenerate everything (complete ~3min)

Recommendation: Option 1

Choose (1-2):
```

### Error Handling

If something fails, the agent:
1. ✅ Identifies the problem
2. ✅ Explains what happened
3. ✅ Offers solutions
4. ✅ Tries to resolve automatically

Example:

```
❌ CodeWiki not found!

Solutions:
1. Install: pip install codewiki
2. Clone: git clone https://github.com/FSoft-AI4Code/CodeWiki
3. Use local version: ./codewiki.py

Should I install it automatically? (yes/no)
```

## 📋 Available Commands

### Main Command
```
generate documentation
```
Executes complete process automatically.

### Diagnostic Commands

```
check status
```
Shows current documentation status.

```
clean and regenerate
```
Removes old files and regenerates from scratch.

```
debug
```
Debug mode with detailed output.

## ⚙️ Configuration (Optional)

### .codewiki.yaml File

Create in your repository root:

```yaml
output:
  directory: ./documentation  # Default: ./docs
  language: auto             # auto-detect or en-US, pt-BR, es-ES
  
analysis:
  ignore_paths:
    - node_modules/
    - venv/
    - .git/
    - build/
    
documentation:
  include_diagrams: true
  include_usage_examples: true
  detail_level: comprehensive  # brief|standard|comprehensive
  
formatting:
  max_line_length: 120
  include_timestamps: false
```

### Environment Variables

```bash
# Output directory
export CODEWIKI_OUTPUT_DIR="./documentation"

# Verbosity level (0-3)
export CODEWIKI_VERBOSE=2

# Include diagrams
export CODEWIKI_DIAGRAMS=true

# Language (auto for auto-detection)
export CODEWIKI_LANG="auto"
```

## 🎯 Use Cases

### Case 1: First Documentation

```
# You're in a new repository without documentation
cd my-project/

# In Claude Code
> generate documentation

# The agent:
# 1. Installs CodeWiki
# 2. Analyzes all code
# 3. Generates complete documentation
# 4. Creates indexes and navigation

# Result: docs/ fully populated
```

### Case 2: Existing CodeWiki Analysis

```
# You already have CodeWiki analysis files
my-project/
├── docs/
│   └── dependency_graphs/
│       ├── MyProject_dependency_graph.json  ← Found automatically!
│       └── MyProject_module_tree.json       ← Found automatically!

# In Claude Code
> generate documentation

# The agent:
# 1. Detects existing analysis files (even with project prefix!)
# 2. Uses them directly (no re-analysis needed)
# 3. Generates documentation
# 4. Creates indexes and navigation

# Result: Fast documentation generation using existing analysis
```

### Case 3: Update After Changes

```
# You modified some files
git status
# modified: src/be/services/new_feature.py

# In Claude Code
> generate documentation

# The agent:
# 1. Detects existing documentation
# 2. Identifies modified module (src/be)
# 3. Updates only what's necessary
# 4. Keeps the rest intact

# Result: Fast incremental update
```

### Case 3: Multiple Repositories

```
# You have several repos to document
repos/
├── frontend/
├── backend/
└── mobile/

# In Claude Code (in each repo)
cd repos/frontend && generate documentation
cd repos/backend && generate documentation
cd repos/mobile && generate documentation

# Or batch mode:
> generate documentation for all repositories in ./repos/
```

### Case 4: CI/CD Integration

```yaml
# .github/workflows/docs.yml
name: Update Documentation

on:
  push:
    branches: [ main, develop ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        
      - name: Generate Documentation
        run: |
          python3 codewiki_agent_executor.py
          
      - name: Commit Documentation
        run: |
          git config user.name "Documentation Bot"
          git add docs/
          git commit -m "docs: Update documentation [skip ci]"
          git push
```

## 📊 Generated Output

### Directory Structure

```
docs/
├── README.md                    # Repository overview
├── INDEX.md                     # Navigation index
├── architecture/
│   ├── overview.md             # General architecture
│   ├── patterns.md             # Detected patterns
│   └── diagrams/               # Diagrams
│       ├── system.mmd
│       ├── modules.mmd
│       └── dataflow.mmd
└── modules/
    ├── src/
    │   ├── fe/
    │   │   ├── README.md       # Frontend module documentation
    │   │   └── components/
    │   │       ├── BackgroundWorker.md
    │   │       ├── CacheManager.md
    │   │       └── ...
    │   └── be/
    │       ├── README.md       # Backend module documentation
    │       └── components/
    └── cli/
        └── README.md
```

### Documentation Quality

✅ **Complete**: All modules and components documented
✅ **Visual**: Mermaid diagrams at multiple levels
✅ **Navigable**: Links between documents, complete index
✅ **Contextual**: Explains purposes, dependencies, patterns
✅ **Professional**: Consistent formatting, clear language

## 🔧 Troubleshooting

### Problem: "CodeWiki not found"

**Solution**: The agent will install automatically. If it fails manually:

```bash
# Option 1: Clone repository
git clone https://github.com/FSoft-AI4Code/CodeWiki
cd CodeWiki
pip install -r requirements.txt

# Option 2: Point to existing installation
export CODEWIKI_PATH="/path/to/CodeWiki"
```

### Problem: "Analysis failed"

**Common causes**:
- Invalid syntax in some files
- Unsupported language
- Permission issues

**Solution**: The agent will show specific error and offer alternatives.

### Problem: "Incomplete documentation"

**Solution**:
```
> clean and regenerate
```

Or manually:
```bash
rm -rf .codewiki/ docs/
# Then: generate documentation
```

### Problem: "Too slow for large repo"

**Solution**: Configure batch processing:

```yaml
# .codewiki.yaml
performance:
  batch_size: 50
  parallel_processing: true
  max_workers: 4
```

### Question: "My files have project name prefix, will they work?"

**Answer**: Yes! The agent automatically detects:
- `ProjectName_dependency_graph.json` ✅
- `ProjectName_module_tree.json` ✅
- Files in `docs/dependency_graphs/` subdirectory ✅

No need to rename files. The agent finds them automatically.

### Question: "Where should I put my CodeWiki analysis files?"

**Answer**: The agent searches in this order:
1. `docs/dependency_graphs/` (with any prefix)
2. `docs/` (with or without prefix)
3. `wiki/`
4. `.codewiki/`
5. Root directory

Put them in any of these locations and the agent will find them!

## 💡 Tips and Best Practices

### 1. Regular Commits

After generating documentation:
```bash
git add docs/
git commit -m "docs: Update documentation"
git push
```

### 2. Ignore Temporary Files

Add to `.gitignore`:
```
.codewiki/
.codewiki-temp/
```

### 3. Review and Customize

After automatic generation:
1. Review docs/README.md
2. Add domain-specific context
3. Improve usage examples
4. Add custom diagrams

### 4. Incremental Update

For large projects, use incremental update:
```
> update documentation only for module src/be
```

### 5. Multilingual Documentation

Generate in multiple languages:
```yaml
# .codewiki.yaml
output:
  languages:
    - en-US: ./docs/en/
    - pt-BR: ./docs/pt/
    - es-ES: ./docs/es/
```

## 📚 Interaction Examples

### Example 1: First Generation

```
User: generate documentation

Agent: 🚀 Starting CodeWiki documentation generation...

[... complete process ...]

✅ Documentation complete!
   • 4 modules documented
   • 158 components analyzed
   • 23 files generated

User: where is the documentation?

Agent: Documentation was generated in ./docs/

Main files:
📖 docs/README.md - Repository overview
📑 docs/INDEX.md - Complete navigation index
📁 docs/modules/ - Documentation for each module

You can open with:
code docs/README.md
```

### Example 2: Update

```
User: I updated the code, need to update documentation

Agent: 📄 Existing documentation detected!

Analyzing changes...
   ✓ Detected changes in: src/be/services/

Updating only what's necessary...
   [1/1] ✓ src/be updated

✅ Update completed in 28 seconds!
```

### Example 3: Diagnostics

```
User: documentation is incomplete

Agent: 🔍 Checking status...

Problems found:
   ⚠️ src/fe/components/NewComponent.py not documented
   ⚠️ 2 broken links in README.md

Would you like me to:
1. Re-analyze and update automatically
2. Regenerate all documentation
3. Show problem details

Choose (1-3):

User: 1

Agent: ✓ Re-analysis completed
      ✓ Problems fixed
      ✓ Documentation updated
```

## 🎓 Additional Resources

### Auxiliary Scripts

**scripts/validate-docs.sh**
```bash
#!/bin/bash
# Validate generated documentation

echo "Validating documentation..."

# Check main files
[ -f docs/README.md ] || echo "❌ README.md missing"
[ -f docs/INDEX.md ] || echo "❌ INDEX.md missing"

# Check links
echo "Checking links..."
find docs -name "*.md" -exec markdown-link-check {} \;

echo "✓ Validation complete"
```

**scripts/preview-docs.sh**
```bash
#!/bin/bash
# Preview documentation locally

cd docs
python3 -m http.server 8000 &
echo "📖 Documentation available at: http://localhost:8000"
```

### Git Hooks

**.git/hooks/pre-commit**
```bash
#!/bin/bash
# Update documentation before commit

echo "Updating documentation..."
python3 codewiki_agent_executor.py --quiet

git add docs/
```

## 🚀 Quick Start

1. **Copy agent files**
   ```bash
   mkdir -p .claude/agents .claude/scripts
   cp codewiki_agent.md .claude/agents/
   cp codewiki_agent_executor.py .claude/scripts/
   ```

2. **In Claude Code, say**
   ```
   generate documentation
   ```

3. **Wait** - The agent does everything else!

4. **Review**
   ```bash
   code docs/README.md
   ```

5. **Commit**
   ```bash
   git add docs/
   git commit -m "docs: Add comprehensive documentation"
   git push
   ```

**Done!** Your repository now has complete professional documentation! 📚✨

## 📞 Support

If you encounter problems:

1. **Check status**: `check status`
2. **Debug mode**: `debug`
3. **Clean and regenerate**: `clean and regenerate`
4. **Manual**: Execute `python3 codewiki_agent_executor.py --debug`

## 📄 License

This agent is part of the CodeWiki Skills system and follows the same license.

---

**Developed to simplify code documentation with Claude Code! 🎉**
