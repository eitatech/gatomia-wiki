# CodeWiki Documentation Agent - Claude Code

## 🎯 Executive Summary

**Autonomous SubAgent** for Claude Code that generates complete repository documentation automatically.

**Single Command**: `generate documentation`

**Result**: Complete professional documentation with diagrams, architecture analysis, and navigation.

---

## 📦 Package Contents

### Main Files

| File | Size | Description |
|------|------|-------------|
| `codewiki_agent.md` | ~45 KB | Complete SubAgent definition |
| `codewiki_agent_executor.py` | ~14 KB | Python executor script |
| `codewiki_analyzer.py` | ~22 KB | Code analyzer |
| `orchestrator.py` | ~20 KB | Documentation generator |
| `README.md` | ~25 KB | Complete usage guide |
| `.codewiki.example.yaml` | ~5 KB | Example configuration |

**Total**: ~130 KB of code and documentation

---

## 🚀 How to Use (3 Steps)

### 1. Install in Claude Code

```bash
# Option A: Per repository
mkdir -p .claude/agents .claude/scripts
cp codewiki_agent.md .claude/agents/
cp codewiki_agent_executor.py .claude/scripts/
cp codewiki_analyzer.py .claude/scripts/
cp orchestrator.py .claude/scripts/

# Option B: Global
mkdir -p ~/.claude/agents ~/.claude/scripts
cp codewiki_agent.md ~/.claude/agents/
cp codewiki_agent_executor.py ~/.claude/scripts/
cp codewiki_analyzer.py ~/.claude/scripts/
cp orchestrator.py ~/.claude/scripts/
```

### 2. Use in Claude Code

In Claude Code, simply say:

```
generate documentation
```

### 3. Review and Commit

```bash
# Review
code docs/README.md

# Commit
git add docs/
git commit -m "docs: Add comprehensive documentation"
git push
```

**Done!** ✅

---

## 💡 What the Agent Does

### Automatic Process

```
User: "generate documentation"
   ↓
🔍 Verify analysis files
   ├─ ✓ Found → Use existing
   └─ ✗ Not found → Generate automatically
   ↓
📦 Install CodeWiki (if necessary)
   ├─ Clone repository
   ├─ Install dependencies
   └─ Configure
   ↓
🔍 Analyze source code
   ├─ Extract components
   ├─ Map dependencies
   └─ Generate module_tree.json + dependency_graph.json
   ↓
📝 Generate documentation
   ├─ Document modules (bottom-up)
   ├─ Create Mermaid diagrams
   ├─ Synthesize overview
   └─ Generate navigation
   ↓
✅ Validate and report
   ├─ Verify completeness
   ├─ Validate links
   └─ Generate report
```

### Generated Output

```
docs/
├── README.md              # Repository overview
├── INDEX.md               # Navigation index
├── architecture/
│   ├── overview.md        # System architecture
│   ├── patterns.md        # Detected patterns
│   └── diagrams/          # Visual diagrams
│       ├── system.mmd
│       └── modules.mmd
└── modules/
    ├── src/fe/
    │   ├── README.md      # Frontend module doc
    │   └── components/    # Component docs
    ├── src/be/
    │   ├── README.md      # Backend module doc
    │   └── components/
    └── cli/
        └── README.md
```

---

## 🎨 Key Features

### ✅ Completely Autonomous
- Doesn't ask permission to execute
- Installs dependencies automatically
- Resolves problems on its own
- Constant feedback

### ✅ Intelligent
- Detects existing files (even with project name prefix)
- Incremental update
- Infers purposes and patterns
- Adapts to context
- Supports multiple file naming conventions

### ✅ Robust
- Complete error handling
- Automatic recovery
- Result validation
- Detailed logs

### ✅ Efficient
- Batch processing
- Analysis cache
- Selective update
- Parallelization (optional)

### ✅ Multilingual
- Detects user's language
- Responds in appropriate language
- English, Portuguese, Spanish, and more
- Technical terms always in English

---

## 📊 Usage Examples

### Example 1: First Generation

```
User: generate documentation

Agent: 🚀 Starting CodeWiki documentation generation...

1️⃣ Verifying analysis files...
   ✗ Not found

2️⃣ Installing and executing CodeWiki...
   ✓ Installed and executed (3.5s)

3️⃣ Analyzing repository...
   📊 4 modules, 158 components

4️⃣ Generating documentation...
   [1/4] ✓ src/fe
   [2/4] ✓ src/be
   [3/4] ✓ cli
   [4/4] ✓ src

5️⃣ Finalizing...
   ✓ README.md
   ✓ INDEX.md
   ✓ Diagrams

✅ Documentation complete in ./docs/
📖 Start with: docs/README.md
```

### Example 2: Incremental Update

```
User: I updated code in src/be, update the docs

Agent: 📄 Existing documentation detected

Verifying changes...
   ✓ src/be modified

Updating...
   ✓ src/be updated (32s)

✅ Update completed!
```

### Example 3: Diagnostics

```
User: check status

Agent: 📊 Documentation Status:

Analysis files:
   ✓ .codewiki/module_tree.json (2.1 MB)
   ✓ .codewiki/dependency_graph.json (5.3 MB)

Generated documentation:
   ✓ docs/README.md (15 KB)
   ✓ docs/INDEX.md (8 KB)

Documented modules:
   ✓ src/fe/ (4 files)
   ✓ src/be/ (12 files)
   ✓ cli/ (5 files)

Status: ✅ Complete and up-to-date
```

---

## ⚙️ Configuration (Optional)

### .codewiki.yaml File

Copy `.codewiki.example.yaml` to `.codewiki.yaml` and customize:

```yaml
output:
  directory: ./docs        # Where to generate
  language: auto          # auto-detect or en-US, pt-BR

documentation:
  include_diagrams: true   # Include diagrams
  detail_level: comprehensive  # Detail level

analysis:
  ignore_paths:            # What to ignore
    - node_modules/
    - venv/
```

### Available Commands

| Command | What It Does |
|---------|--------------|
| `generate documentation` | Complete process |
| `check status` | Shows current status |
| `clean and regenerate` | Removes and regenerates all |
| `debug` | Detailed debug mode |
| `update only module X` | Selective update |

---

## 🔧 CI/CD Integration

### GitHub Actions

```yaml
name: Documentation

on:
  push:
    branches: [ main ]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Generate Docs
        run: python3 codewiki_agent_executor.py
        
      - name: Commit
        run: |
          git add docs/
          git commit -m "docs: Update [skip ci]"
          git push
```

### GitLab CI

```yaml
docs:
  stage: deploy
  script:
    - python3 codewiki_agent_executor.py
    - git add docs/
    - git commit -m "docs: Update [skip ci]"
    - git push
  only:
    - main
```

---

## 🎯 Use Cases

### ✅ Initial Documentation
New repository without documentation → Generates everything from scratch

### ✅ Maintenance
Code changed → Updates documentation automatically

### ✅ Onboarding
New team member → Complete documentation ready

### ✅ Architecture Review
Need to understand architecture → Diagrams and explanations

### ✅ Multiple Repos
Several repositories → Documents all automatically

---

## 📈 Documentation Quality

### Quality Metrics

✅ **Completeness**: 100% of components documented
✅ **Clarity**: Professional and clear language
✅ **Visual**: Diagrams at multiple levels
✅ **Navigation**: Complete links and indexes
✅ **Context**: Explains purposes and patterns

### What Is Generated

- **Overview**: README.md with general architecture
- **Navigation**: INDEX.md with all links
- **Modules**: Documentation for each module
- **Components**: Documentation for each component
- **Diagrams**: Mermaid visualizations
- **Patterns**: Architectural analysis
- **Dependencies**: Complete mapping

---

## 🔍 Technical Details

### Technologies

- **Python 3.8+**: Main language
- **CodeWiki**: Code analysis
- **Tree-sitter**: Multi-language parsing
- **Mermaid**: Diagrams
- **Markdown**: Output format

### Supported Languages

✅ Python
✅ JavaScript
✅ TypeScript
✅ Java
✅ C
✅ C++
✅ C#

### Dependencies

**None!** The agent installs everything automatically.

---

## 💡 Usage Tips

### 1. First Time
Let the agent do everything automatically. Don't interrupt.

### 2. Customization
After first generation, personalize:
- Add domain-specific context
- Improve usage examples
- Add custom diagrams

### 3. Regular Update
Configure CI/CD to update automatically on each commit.

### 4. Review
Always review docs/README.md after generation.

### 5. Commit
Commit documentation along with code.

---

## 🎓 Additional Resources

### File Structure

```
codewiki-agent-claude-code/
├── codewiki_agent.md              # Agent definition
├── codewiki_agent_executor.py     # Python executor
├── codewiki_analyzer.py           # Analyzer
├── orchestrator.py                # Orchestrator
├── README.md                      # This guide
└── .codewiki.example.yaml         # Example config
```

### Useful Commands

```bash
# View status
python3 codewiki_agent_executor.py --help

# Debug mode
python3 codewiki_agent_executor.py --debug

# Custom output
python3 codewiki_agent_executor.py --output ./documentation

# Quiet mode
python3 codewiki_agent_executor.py --quiet
```

---

## 📞 Troubleshooting

### Problem: "CodeWiki not found"
**Solution**: Agent will install automatically

### Problem: "Analysis failed"
**Solution**: Execute `debug` to see details

### Problem: "Incomplete documentation"
**Solution**: Execute `clean and regenerate`

### Problem: "Too slow"
**Solution**: Configure parallel processing in `.codewiki.yaml`

---

## 🎉 Start Now

### Step 1: Extract files
```bash
tar -xzf codewiki-agent-claude-code.tar.gz
# or
unzip codewiki-agent-claude-code.zip
```

### Step 2: Copy to project
```bash
cd codewiki-agent-claude-code
cp codewiki_agent.md your-project/.claude/agents/
cp *.py your-project/.claude/scripts/
```

### Step 3: Use
In Claude Code:
```
generate documentation
```

**That's it!** 🚀

---

## 📊 Summary

| Aspect | Detail |
|--------|--------|
| **Automation** | 100% autonomous |
| **Languages** | 7 supported |
| **Size** | ~130 KB total |
| **Time** | ~3-5 min for medium repo |
| **Output** | 20-50 .md files |
| **Quality** | Professional |
| **Cost** | Free |

---

## ✅ Benefits

1. ⚡ **Speed**: From zero to complete documentation in minutes
2. 🎯 **Autonomy**: No configuration needed
3. 📊 **Quality**: Professional documentation with diagrams
4. 🔄 **Maintenance**: Automatic update when code changes
5. 🌍 **Multilingual**: Support for 7 programming languages
6. 🎨 **Visual**: Mermaid diagrams at multiple levels
7. 🔗 **Navigable**: Complete link system
8. 📈 **Scalable**: Works on small and large repos

---

## 🚀 Call to Action

**Ready to document your repository?**

1. ✅ Download files
2. ✅ Copy to `.claude/`
3. ✅ Say "generate documentation"
4. ✅ Receive complete documentation!

**It's that simple! 📚✨**

---

**Developed to simplify developers' lives with Claude Code!**

*Version 1.0 - December 2024*
