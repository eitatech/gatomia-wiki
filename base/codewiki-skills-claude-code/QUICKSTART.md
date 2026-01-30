# CodeWiki Skills - Quick Start Guide

Get started with CodeWiki documentation generation in 5 minutes!

## 📦 What You Have

```
codewiki-skills-complete/
├── SKILL.md                    # Master skill (read first!)
├── analyzer-helper.md          # Analysis methodology
├── prompt-templates.md         # Documentation prompts
├── codewiki_analyzer.py       # Python analyzer
├── orchestrator.py            # Documentation orchestrator
├── README.md                  # Complete documentation
├── INTERACTIVE_GUIDE.md       # Claude usage patterns
├── QUICKSTART.md              # This file
└── example-output/            # Example generated docs
    ├── README.md              # Repository overview
    ├── INDEX.md               # Navigation
    └── modules/               # Module documentation
```

## 🚀 Three Ways to Use

### Option 1: Automated Generation (Python)

**Perfect for**: Generating complete documentation automatically

```bash
# Install Python 3.8+ (no dependencies needed!)

# Generate documentation
python3 orchestrator.py module_tree.json dependency_graph.json ./output

# View results
cd output
cat README.md
```

**What you get**:
- Complete documentation in ./output/
- All modules documented
- Architecture diagrams
- Navigation index
- Ready to commit to repo!

### Option 2: Interactive with Claude (Recommended)

**Perfect for**: Customized, high-quality documentation with Claude's help

**Step 1**: Upload your files to Claude
- `module_tree.json`
- `dependency_graph.json`

**Step 2**: Tell Claude:
```
"Using the CodeWiki Skills system, generate comprehensive documentation for my repository"
```

**Step 3**: Claude will:
1. ✅ Analyze your repository structure
2. ✅ Generate module documentation (with diagrams!)
3. ✅ Create repository overview
4. ✅ Build navigation
5. ✅ Explain architectural patterns

**Step 4**: Iterate with Claude:
- "Explain the src/be module in more detail"
- "Create an architecture diagram showing all interactions"
- "What patterns does this codebase use?"

See [INTERACTIVE_GUIDE.md](INTERACTIVE_GUIDE.md) for conversation patterns.

### Option 3: Hybrid Approach

**Perfect for**: Automated analysis + Claude generation

**Step 1**: Run Python analyzer
```bash
python3 codewiki_analyzer.py module_tree.json dependency_graph.json > analysis.txt
```

**Step 2**: Give analysis to Claude
```
"Here's an analysis of my repository:
[paste analysis.txt]

Please generate CodeWiki-style documentation using the prompt templates."
```

**Step 3**: Claude generates high-quality docs based on analysis

## 💡 Example Workflow

### Using the Actual GatoWiki Repository

Your `module_tree.json` and `dependency_graph.json` were analyzed:

**Repository Structure**:
```
4 modules, 158 components
├── src/fe (10 components) - Frontend web application
├── src/be (19 components) - Backend analysis engine
├── cli (12 components) - Command-line interface
└── src (2 components) - Shared configuration
```

**Generated Documentation** (see example-output/):
- [README.md](example-output/README.md) - Repository overview with architecture
- [INDEX.md](example-output/INDEX.md) - Complete navigation
- [src/fe/README.md](example-output/modules/src/fe/README.md) - Frontend docs with diagrams
- [src/be/README.md](example-output/modules/src/be/README.md) - Backend docs
- [cli/README.md](example-output/modules/cli/README.md) - CLI docs
- [src/README.md](example-output/modules/src/README.md) - Core docs

## 🎯 What Gets Generated

### For Each Module:
```markdown
# Module: src/fe

## Overview
[High-level purpose and context]

## Architecture
[How components work together]

```mermaid
graph LR
    [Component dependency diagram]
```

## Components
### BackgroundWorker
**Type**: class
**Purpose**: Orchestrates async documentation generation
**Dependencies**: [internal and external]

[... all components documented ...]

## External Dependencies
[Modules this depends on]

## Used By
[Modules that use this]

## Patterns
[Detected architectural patterns]
```

### Repository Overview:
```markdown
# Repository Documentation

## Purpose
[What the system does]

## Architecture Overview
[System-level design]

```mermaid
graph TB
    [System architecture diagram]
```

## Module Structure
[All modules with links]

## Getting Started
[Where to start reading]
```

## 🔑 Key Features

✅ **Complete Coverage**: All modules and components
✅ **Visual Diagrams**: Mermaid architecture diagrams
✅ **Pattern Detection**: Identifies architectural patterns
✅ **Hierarchical**: Follows codebase structure
✅ **Navigable**: Easy cross-referencing
✅ **Professional**: Production-ready documentation

## 📚 Next Steps

1. **Read the Skills**: Start with [SKILL.md](SKILL.md)
2. **Try Example**: Look at [example-output/](example-output/)
3. **Generate Your Own**: Use orchestrator.py or Claude
4. **Customize**: Extend with your own patterns/templates

## 🤔 Common Questions

**Q: Do I need the Python reference implementation?**
A: No! This is a completely separate Skills/Prompts-based system.

**Q: Can I use this with Claude Code?**
A: Yes! Claude Code can read these skills and generate documentation.

**Q: What if I want to customize the output?**
A: Edit [prompt-templates.md](prompt-templates.md) or extend the Python analyzer.

**Q: Does this work for all programming languages?**
A: Yes, but you may want to add language-specific inference rules.

**Q: Can I integrate this into CI/CD?**
A: Absolutely! Run orchestrator.py in your pipeline.

## 💪 Power User Tips

### Tip 1: Language-Specific Customization
Add your language patterns to `infer_component_purpose()`:
```python
if language == 'java':
    if name.endswith('Controller'):
        return 'REST API controller'
    # ... more patterns
```

### Tip 2: Custom Diagrams
Extend diagram generation:
```python
def generate_sequence_diagram(component_id):
    # Create sequence diagram for interactions
    return mermaid_code
```

### Tip 3: Progressive Documentation
Document most important modules first:
```python
priority_modules = ['src/be', 'src/fe']
for module in priority_modules:
    generate_documentation(module)
```

### Tip 4: Incremental Updates
Only regenerate changed modules:
```python
changed = detect_changes(old_tree, new_tree)
for module in changed:
    update_documentation(module)
```

## 🎓 Learning Path

**Beginner**:
1. Read QUICKSTART.md (you are here!)
2. Look at example-output/
3. Run orchestrator.py on your files

**Intermediate**:
4. Read SKILL.md for methodology
5. Try interactive generation with Claude
6. Customize prompt templates

**Advanced**:
7. Extend Python analyzer
8. Add custom pattern detection
9. Integrate into your workflow
10. Contribute improvements!

## 🏁 Ready to Start?

### Automated:
```bash
python3 orchestrator.py module_tree.json dependency_graph.json ./docs
```

### With Claude:
```
Upload your files, then say:
"Generate CodeWiki documentation using the Skills system"
```

### Hybrid:
```bash
python3 codewiki_analyzer.py module_tree.json dependency_graph.json > analysis.txt
# Give analysis.txt to Claude for generation
```

---

**Questions?** Read the [README.md](README.md) for comprehensive documentation.

**Need examples?** Check [example-output/](example-output/) for actual generated docs.

**Want interactive?** See [INTERACTIVE_GUIDE.md](INTERACTIVE_GUIDE.md) for Claude patterns.

**Happy documenting! 📚✨**
