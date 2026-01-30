# CodeWiki Documentation Generator - Skills System

A comprehensive system for generating CodeWiki-style repository documentation using Claude's Skills, SubAgents, and Prompts. This system reads module trees and dependency graphs to generate hierarchical, architecture-aware documentation with visual artifacts.

## 📋 Table of Contents

- [Overview](#overview)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [How It Works](#how-it-works)
- [Files Overview](#files-overview)
- [Usage Examples](#usage-examples)
- [Integration with Claude](#integration-with-claude)
- [Advanced Usage](#advanced-usage)
- [Extending the System](#extending-the-system)

## 🎯 Overview

This implementation provides a complete CodeWiki documentation generation system that:

- ✅ Reads `module_tree.json` and `dependency_graph.json` files
- ✅ Analyzes repository structure and dependencies
- ✅ Generates hierarchical documentation (leaf → parent → repository)
- ✅ Creates architectural diagrams using Mermaid
- ✅ Infers component purposes and architectural patterns
- ✅ Produces professional, navigable documentation
- ✅ Supports both automated and Claude-assisted generation

**Key Innovation**: This is NOT a reimplementation of the Python reference. Instead, it's a Prompt/Skills-based system that leverages Claude's capabilities to generate documentation through structured analysis and prompt engineering.

## 🏗️ System Architecture

```
CodeWiki Skills System
├── SKILL.md                    # Master skill definition
├── analyzer-helper.md          # Analysis methodology 
├── prompt-templates.md         # Prompt templates for documentation
├── codewiki_analyzer.py       # Python analyzer implementation
├── orchestrator.py            # Documentation generation orchestrator
└── README.md                  # This file

Generated Output:
├── docs/
│   ├── README.md              # Repository overview
│   ├── INDEX.md               # Navigation index
│   └── modules/
│       ├── src/fe/
│       │   └── README.md      # Module documentation
│       ├── src/be/
│       │   └── README.md
│       └── cli/
│           └── README.md
```

### Three-Phase Process

**Phase 1: Analysis**
- Parse module tree structure
- Build component dependency maps
- Detect patterns and infer purposes
- Calculate complexity metrics

**Phase 2: Generation**
- Document leaf modules (bottom-up)
- Synthesize parent modules
- Generate visual artifacts
- Create cross-references

**Phase 3: Assembly**
- Generate repository overview
- Create navigation index
- Link all documentation
- Validate completeness

## 🚀 Quick Start

### 1. Prepare Your Files

Ensure you have:
- `module_tree.json` - Hierarchical module structure
- `dependency_graph.json` - Component dependencies

### 2. Run Analysis

```bash
python3 codewiki_analyzer.py module_tree.json dependency_graph.json
```

This will show you:
- Repository summary (modules, components)
- Processing order (bottom-up)
- Module analysis preview

### 3. Generate Documentation

```bash
python3 orchestrator.py module_tree.json dependency_graph.json ./docs
```

This generates:
- Complete documentation in `./docs/`
- Module documentation hierarchy
- Repository overview
- Navigation index

### 4. Review Output

```bash
cd docs
ls -R
# View README.md, modules/, INDEX.md
```

## 💡 How It Works

### 1. Module Tree Structure

```json
{
    "src/fe": {
        "components": [
            "gatowiki.src.fe.background_worker.BackgroundWorker",
            "gatowiki.src.fe.cache_manager.CacheManager"
        ],
        "path": "src/fe",
        "children": {}
    }
}
```

- **Path**: Module location
- **Components**: List of component IDs
- **Children**: Nested modules (for hierarchical structure)

### 2. Dependency Graph Structure

```json
{
    "gatowiki.src.fe.background_worker.BackgroundWorker": {
        "id": "gatowiki.src.fe.background_worker.BackgroundWorker",
        "name": "BackgroundWorker",
        "component_type": "class",
        "file_path": "/path/to/file.py",
        "relative_path": "gatowiki/src/fe/background_worker.py",
        "depends_on": ["component.id.1", "component.id.2"]
    }
}
```

### 3. Analysis Process

The analyzer:

1. **Parses Module Tree**
   - Identifies leaf vs parent modules
   - Maps components to modules
   - Determines processing order (bottom-up)

2. **Builds Component Maps**
   - Creates comprehensive component info
   - Builds reverse dependency lookup
   - Calculates metrics (fan-in, fan-out)

3. **Analyzes Dependencies**
   - Internal (same module) vs external
   - Module-level dependency patterns
   - Cross-module relationships

4. **Detects Patterns**
   - Infers component purposes from names and dependencies
   - Detects architectural patterns (layered, plugin, facade)
   - Assigns roles (service, manager, model, etc.)

5. **Generates Reports**
   - Per-component analysis
   - Per-module analysis
   - Repository-level summary

### 4. Documentation Generation

For each module:

1. **Analyze**: Run comprehensive analysis
2. **Format**: Prepare data for prompts/templates
3. **Generate**: Create markdown documentation
4. **Visualize**: Generate Mermaid diagrams
5. **Save**: Write to appropriate location

### 5. Hierarchical Synthesis

Parent modules are synthesized from children:

1. Load child documentation
2. Extract key themes and patterns
3. Generate architectural overview
4. Create module hierarchy diagram
5. Link to child documentation

## 📁 Files Overview

### Core Skills

#### `SKILL.md`
The master skill definition containing:
- Complete methodology
- Template structures
- Best practices
- Pattern detection heuristics
- Diagram generation guidelines

**Use this**: When Claude needs to understand the complete CodeWiki approach.

#### `analyzer-helper.md`
Helper skill with:
- Data structure definitions
- Analysis algorithms
- Utility functions
- Complexity calculations
- Pattern detection logic

**Use this**: For understanding analysis methodologies.

#### `prompt-templates.md`
Collection of prompts for:
- Leaf module documentation
- Component documentation
- Parent module synthesis
- Repository overview
- Diagram generation
- Cross-reference management

**Use this**: As templates for Claude-generated documentation.

### Implementation

#### `codewiki_analyzer.py`
Python implementation providing:
- `CodeWikiAnalyzer` class
- Module tree parsing
- Dependency analysis
- Pattern detection
- Report generation
- Command-line interface

**Use this**: For automated analysis and data preparation.

#### `orchestrator.py`
Orchestration system providing:
- `CodeWikiOrchestrator` class
- End-to-end documentation generation
- Hierarchical processing
- File management
- Navigation generation

**Use this**: For complete automated documentation generation.

## 🔧 Usage Examples

### Example 1: Interactive Claude Generation

```python
# 1. Analyze with Python
analyzer = CodeWikiAnalyzer("module_tree.json", "dependency_graph.json")
report = analyzer.generate_analysis_report("src/fe")

# 2. Format for Claude
prompt_data = format_leaf_module_prompt(report)

# 3. Send to Claude with prompt template
# Claude generates: comprehensive markdown documentation

# 4. Save result
save_documentation("docs/modules/src/fe/README.md", claude_output)
```

### Example 2: Automated Generation

```python
orchestrator = CodeWikiOrchestrator(
    "module_tree.json",
    "dependency_graph.json",
    "./docs"
)
orchestrator.generate_all_documentation()
```

### Example 3: Custom Analysis

```python
analyzer = CodeWikiAnalyzer("module_tree.json", "dependency_graph.json")

# Analyze specific component
comp_analysis = analyzer.analyze_dependencies("gatowiki.src.fe.BackgroundWorker")
purpose = analyzer.infer_component_purpose("gatowiki.src.fe.BackgroundWorker")

# Detect module patterns
patterns = analyzer.detect_module_patterns("src/fe")

# Get processing order
order = analyzer.get_processing_order()
```

### Example 4: Generate Specific Diagrams

```python
# Component dependency diagram
report = analyzer.generate_analysis_report("src/fe")
diagram = generate_component_diagram(report)
# Returns: Mermaid diagram code

# Module hierarchy
hierarchy_diagram = generate_module_hierarchy_diagram("src")
# Returns: Module tree visualization

# System architecture
arch_diagram = generate_repository_architecture_diagram()
# Returns: High-level system view
```

## 🤖 Integration with Claude

### Method 1: Using Skills in Conversations

When a user uploads `module_tree.json` and `dependency_graph.json`:

1. **Claude recognizes the task** via the SKILL.md
2. **Runs the analyzer** to understand structure
3. **Generates documentation** module by module
4. **Creates visualizations** using Mermaid
5. **Assembles complete documentation** hierarchically

### Method 2: Using Prompt Templates

For each documentation task, Claude can use the appropriate prompt template:

```
User: "Document the src/fe module"

Claude: 
1. Reads module_tree.json and dependency_graph.json
2. Analyzes src/fe module
3. Uses "Leaf Module Documentation Generator" prompt
4. Generates comprehensive markdown
5. Returns formatted documentation
```

### Method 3: Progressive Generation

```
User: "Generate CodeWiki documentation for my repository"

Claude:
1. "Analyzing repository structure..."
   [Shows summary: 4 modules, 158 components]

2. "Documenting leaf modules..."
   [Generates src/fe, src/be, cli, src]

3. "Creating repository overview..."
   [Generates README.md with architecture diagrams]

4. "Building navigation..."
   [Creates INDEX.md]

5. "Documentation complete! Here's your structure..."
   [Shows documentation tree]
```

### Method 4: Hybrid Approach

```python
# Python does analysis
analyzer = CodeWikiAnalyzer("module_tree.json", "dependency_graph.json")
report = analyzer.generate_analysis_report("src/fe")

# Claude does generation
prompt = f"""
Based on this analysis:
{json.dumps(report, indent=2)}

Generate comprehensive module documentation following CodeWiki methodology.
Include:
- Overview and purpose
- Architecture description
- Component documentation
- Mermaid diagrams
- Dependencies and relationships
"""

# Claude generates high-quality documentation
documentation = claude.generate(prompt)
```

## 🎨 Advanced Usage

### Custom Pattern Detection

Add your own pattern detection:

```python
def detect_custom_pattern(module_analysis):
    """Detect domain-specific patterns."""
    patterns = []
    
    # Example: Detect microservice pattern
    if has_api_endpoints(module_analysis):
        if has_service_layer(module_analysis):
            patterns.append({
                'type': 'microservice',
                'confidence': 0.8,
                'evidence': ['API endpoints', 'Service layer'],
                'components': get_service_components(module_analysis)
            })
    
    return patterns
```

### Custom Documentation Templates

Create specialized templates:

```markdown
# API Service Module Documentation

## Endpoints
[List all API endpoints from analysis]

## Service Layer
[Document business logic services]

## Data Access
[Document repository/DAO components]

## Authentication
[Document auth-related components]
```

### Multi-Language Support

Adapt for different programming languages:

```python
def infer_component_purpose_java(component_id, comp_info):
    """Java-specific purpose inference."""
    name = comp_info['name']
    
    if name.endswith('Controller'):
        return 'REST API controller handling HTTP requests'
    elif name.endswith('Service'):
        return 'Business logic service'
    elif name.endswith('Repository'):
        return 'Data access layer'
    elif name.endswith('DTO'):
        return 'Data transfer object'
    # ... more patterns
```

### Incremental Updates

Handle repository changes:

```python
def update_documentation(old_tree, new_tree, changed_modules):
    """Update only changed modules."""
    analyzer = CodeWikiAnalyzer(new_tree, dep_graph)
    
    for module in changed_modules:
        # Regenerate this module
        report = analyzer.generate_analysis_report(module)
        doc = generate_documentation(report)
        save_documentation(module, doc)
        
        # Update parent modules
        update_parent_chain(module)
```

## 🔌 Extending the System

### Add New Analysis Metrics

```python
class CodeWikiAnalyzer:
    def calculate_maintainability_index(self, module_path):
        """Calculate maintainability index."""
        complexity = self.calculate_module_complexity(module_path)
        
        # Halstead volume, cyclomatic complexity, LOC
        # MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(L)
        
        return maintainability_index
```

### Add New Diagram Types

```python
def generate_sequence_diagram(component_id, max_depth=3):
    """Generate sequence diagram for component interactions."""
    diagram = "```mermaid\nsequenceDiagram\n"
    
    # Trace call sequences
    calls = trace_execution_flow(component_id, max_depth)
    
    for call in calls:
        diagram += f"    {call['from']} ->> {call['to']}: {call['method']}\n"
    
    diagram += "```\n"
    return diagram
```

### Add New Documentation Sections

```python
def generate_testing_guide(module_path, report):
    """Generate testing guidance for module."""
    md = "## Testing Guide\n\n"
    
    # Identify testable components
    for comp_id in report['components']:
        if is_testable(comp_id):
            md += generate_test_guidance(comp_id)
    
    return md
```

## 📊 Output Quality

The generated documentation includes:

✅ **Comprehensive Coverage**
- All modules documented
- All components documented
- All relationships captured

✅ **Architecture Awareness**
- Hierarchical organization
- Cross-module dependencies
- Architectural patterns

✅ **Visual Artifacts**
- Component dependency diagrams
- Module hierarchy diagrams
- System architecture diagrams
- Data flow diagrams

✅ **Developer-Friendly**
- Clear, concise language
- Practical examples (where applicable)
- Easy navigation
- Consistent structure

✅ **Maintainable**
- Markdown format
- Version control friendly
- Incrementally updatable
- Link integrity

## 🤝 Contributing

To extend this system:

1. **Add new patterns**: Update `detect_patterns()` in analyzer
2. **Add new prompts**: Add to `prompt-templates.md`
3. **Add new diagrams**: Extend diagram generation functions
4. **Add new metrics**: Extend complexity calculation
5. **Add new languages**: Add language-specific inference

## 📝 License

This is an implementation of the CodeWiki methodology described in the research paper:
"CodeWiki: Evaluating AI's Ability to Generate Holistic Documentation for Large-Scale Codebases"

Reference implementation: https://github.com/FSoft-AI4Code/CodeWiki

## 🙏 Acknowledgments

Based on the CodeWiki research paper by Anh Nguyen Hoang, Minh Le-Anh, Bach Le, and Nghi D.Q. Bui from FPT Software AI Center and University of Melbourne.

This Skills/Prompts implementation provides an alternative approach using Claude's capabilities to generate documentation through structured analysis and prompt engineering, rather than reimplementing the Python reference code.

---

**Ready to generate documentation?**

```bash
# Quick start
python3 orchestrator.py module_tree.json dependency_graph.json ./docs

# View results
cd docs && ls -R
```

**Need help?** The system is self-documenting - read the SKILL.md for comprehensive methodology!
