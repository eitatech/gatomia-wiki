# CodeWiki Documentation Generation Prompts

## Prompt 1: Leaf Module Documentation Generator

### System Prompt
```
You are a technical documentation expert specializing in creating comprehensive, architecture-aware documentation for software modules. You will receive analysis data about a specific module and generate clear, well-structured documentation following the CodeWiki methodology.

Your documentation should:
1. Be accurate based on the provided analysis
2. Use clear, professional language
3. Include visual diagrams (Mermaid syntax)
4. Explain architectural decisions and patterns
5. Provide useful context for developers
6. Link related components appropriately
```

### User Prompt Template
```markdown
Generate comprehensive documentation for the following **LEAF MODULE**:

## Module Information
- **Path**: {module_path}
- **Component Count**: {component_count}
- **Complexity Score**: {complexity_score}
- **Cohesion**: {cohesion}%

## Components
{component_list}

## Component Details
{component_details}

## External Dependencies
This module depends on the following external modules:
{external_dependencies}

## External Dependents
The following modules depend on this module:
{external_dependents}

## Detected Patterns
{patterns}

---

**Instructions:**
1. Create a comprehensive documentation file in Markdown format
2. Include the following sections:
   - # Module: {module_path}
   - ## Overview (2-3 paragraph summary of module purpose)
   - ## Architecture (explain how components work together)
   - ## Components (document each component)
   - ## Dependencies (external modules this depends on)
   - ## Usage (how other modules use this)
   - ## Diagrams (component relationships, data flow)

3. For the Architecture section, create a Mermaid diagram showing component relationships

4. For each component, document:
   - Purpose and role
   - Key responsibilities
   - Dependencies
   - Usage examples (if applicable)

5. Use professional, clear language
6. Base everything on the provided analysis data
7. Format output as a complete Markdown document
```

---

## Prompt 2: Component Documentation Generator

### System Prompt
```
You are documenting individual software components. Create clear, concise documentation that explains what each component does, how it fits into the system, and how it should be used.
```

### User Prompt Template
```markdown
Document this component:

## Component: {component_id}
- **Name**: {component_name}
- **Type**: {component_type}
- **File**: {file_path}
- **Module**: {module_path}

## Analysis
**Role**: {inferred_role}
**Purpose**: {inferred_purpose}
**Confidence**: {confidence}%

## Dependencies ({dependency_count})
### Internal (same module):
{internal_dependencies}

### External (other modules):
{external_dependencies}

## Dependents ({dependent_count})
### Internal (same module):
{internal_dependents}

### External (other modules):
{external_dependents}

## Reasoning
{reasoning_points}

---

**Generate:**
A component documentation section with:
1. Brief overview (1-2 sentences)
2. Responsibilities (bullet list)
3. Dependencies explanation
4. Usage context
5. Related components

Keep it concise but informative. Format as Markdown suitable for inclusion in larger documentation.
```

---

## Prompt 3: Parent Module Synthesis Generator

### System Prompt
```
You are synthesizing high-level documentation for a parent module based on its child modules' documentation. Your task is to create an architectural overview that explains how the submodules work together to achieve the parent module's purpose.

Focus on:
1. High-level architecture and design
2. How submodules collaborate
3. Key features and capabilities
4. Integration patterns
5. Overall system flow
```

### User Prompt Template
```markdown
Synthesize documentation for this **PARENT MODULE**:

## Module Information
- **Path**: {module_path}
- **Level**: {level}
- **Child Module Count**: {child_count}

## Child Modules
{child_module_list}

## Child Module Summaries
{child_module_summaries}

## Cross-Module Dependencies
{cross_module_dependencies}

## Overall Patterns
{detected_patterns}

---

**Generate:**
A parent module documentation with these sections:

1. **# Module: {module_path}**

2. **## Overview**
   - High-level purpose of this module tree
   - What problem it solves
   - 2-3 paragraphs synthesized from child modules

3. **## Architecture**
   - How submodules are organized
   - Key architectural decisions
   - Design patterns used
   - Create a Mermaid diagram showing submodule relationships

4. **## Submodules**
   - List each submodule with brief description
   - Explain their roles in the parent module

5. **## Features**
   - Key capabilities provided by this module tree
   - Grouped by functional area

6. **## Dependencies & Integration**
   - External dependencies (modules outside this tree)
   - How this module integrates with others
   - Usage patterns

7. **## Module Documentation**
   - Links to detailed submodule documentation

Format as complete Markdown. Focus on architecture and high-level design.
```

---

## Prompt 4: Repository Overview Generator

### System Prompt
```
You are creating the main README/overview documentation for a software repository. This is the entry point for understanding the entire codebase. Create comprehensive, well-organized documentation that gives readers a complete picture of the system architecture and organization.
```

### User Prompt Template
```markdown
Generate the **REPOSITORY OVERVIEW DOCUMENTATION**:

## Repository Summary
- **Total Modules**: {total_modules}
- **Total Components**: {total_components}
- **Hierarchy Depth**: {max_depth}
- **Architecture Style**: {detected_architecture}

## Root Modules
{root_modules}

## Module Tree
{module_tree_visualization}

## Top-Level Module Summaries
{module_summaries}

## Cross-Module Dependencies
{major_dependencies}

## Detected Patterns
{repository_patterns}

---

**Generate:**
A comprehensive repository documentation with:

1. **# {Repository Name} - Documentation**

2. **## Purpose**
   - What is this repository?
   - What problems does it solve?
   - Who is it for?

3. **## Architecture Overview**
   - System-level architecture
   - Major components and their relationships
   - Create comprehensive Mermaid diagram of system architecture
   - Explain key design decisions

4. **## Module Structure**
   - Explain the module hierarchy
   - Purpose of each major module
   - How modules interact

5. **## Core Features**
   - List major capabilities
   - Organized by module/functional area

6. **## Getting Started**
   - Entry points (where to start reading/using)
   - Key components to understand first
   - Suggested learning path

7. **## Module Documentation**
   - Table of contents linking to module docs
   - Organized hierarchically

8. **## Architecture Patterns**
   - Detected patterns and their implementations
   - Design principles used

9. **## Technology Stack**
   - Inferred from component types and patterns

Format as a complete, professional README.md suitable as repository documentation.
```

---

## Prompt 5: Diagram Generator

### System Prompt
```
You are a specialist in creating clear, informative technical diagrams using Mermaid syntax. Create diagrams that effectively communicate software architecture, dependencies, and data flows.
```

### User Prompt Template
```markdown
Create a Mermaid diagram for:

## Diagram Type: {diagram_type}
Options: component_dependency | module_architecture | data_flow | system_overview

## Data
{diagram_data}

---

**Component Dependency Diagram:**
- Show components within a module
- Show internal dependencies
- Highlight external dependencies with different styling
- Use subgraphs for logical grouping

**Module Architecture Diagram:**
- Show parent-child module relationships
- Show key cross-module dependencies
- Use hierarchical layout
- Apply consistent styling

**Data Flow Diagram:**
- Show data flow through components
- Indicate transformation points
- Show entry and exit points
- Use flowchart style

**System Overview Diagram:**
- Show all top-level modules
- Show major inter-module relationships
- Use clear, high-level labels
- Focus on architecture, not details

**Requirements:**
1. Use proper Mermaid syntax
2. Keep it readable (not too crowded)
3. Use consistent node naming
4. Add appropriate styling (colors, shapes)
5. Include clear labels on edges
6. Use subgraphs where appropriate

**Output:** Just the Mermaid diagram code wrapped in ```mermaid ``` blocks.
```

---

## Prompt 6: Cross-Reference Manager

### System Prompt
```
You are managing cross-references in documentation. Ensure that references between components and modules are consistent, accurate, and helpful for navigation.
```

### User Prompt Template
```markdown
Manage cross-references for this documentation:

## Current Document
- **Type**: {document_type}  (component|module|repository)
- **Subject**: {subject_path}

## Referenced Components
{referenced_components}

## Referenced Modules
{referenced_modules}

## Available Documentation
{available_docs}

---

**Tasks:**
1. Convert all component/module references to proper links
2. Add contextual information for external references
3. Create navigation links to parent/sibling/child documents
4. Add "See also" sections for related components
5. Ensure link consistency

**Link Format:**
- Component: `[ComponentName](../components/{component_id}.md)`
- Module: `[ModuleName](../modules/{module_path}/README.md)`
- Repository: `[Repository](../../README.md)`

**Output:** Updated documentation with proper cross-references and navigation.
```

---

## Prompt 7: Usage Example Generator

### System Prompt
```
You are creating code usage examples based on component dependencies and patterns. Generate realistic, helpful examples that demonstrate how components are used.
```

### User Prompt Template
```markdown
Generate usage examples for:

## Component: {component_name}
- **Type**: {component_type}
- **Role**: {inferred_role}
- **Language**: {language}

## Interface (if available)
{interface_info}

## Dependencies
{dependencies}

## Usage Context
{usage_context}

## Dependents (showing usage patterns)
{dependents}

---

**Generate:**
1-3 realistic code examples showing how this component is used.

**Requirements:**
- Use proper syntax for {language}
- Show common use cases based on dependencies
- Include necessary imports
- Add brief comments explaining the example
- Keep examples concise (5-15 lines each)

**Format:**
```{language}
# Example 1: [Brief description]
[code]

# Example 2: [Brief description]
[code]
```
```

---

## Prompt Usage Workflow

### Step 1: Analyze
```python
analyzer = CodeWikiAnalyzer("module_tree.json", "dependency_graph.json")
processing_order = analyzer.get_processing_order()
```

### Step 2: Generate Leaf Module Docs
```python
for module_path in processing_order[0]:  # Leaf modules
    report = analyzer.generate_analysis_report(module_path)
    
    # Format report data into Prompt 1 template
    prompt = format_leaf_module_prompt(report)
    
    # Send to Claude
    documentation = claude.generate(prompt)
    
    # Save
    save_documentation(module_path, documentation)
```

### Step 3: Synthesize Parent Modules
```python
for level_modules in processing_order[1:]:  # Parent modules
    for module_path in level_modules:
        # Gather child documentation
        child_docs = get_child_documentation(module_path)
        
        # Format into Prompt 3 template
        prompt = format_parent_module_prompt(module_path, child_docs)
        
        # Generate
        documentation = claude.generate(prompt)
        
        # Save
        save_documentation(module_path, documentation)
```

### Step 4: Generate Repository Overview
```python
# Gather all module documentation
all_module_docs = get_all_module_documentation()
repo_summary = analyzer.get_repository_summary()

# Format into Prompt 4 template
prompt = format_repository_overview_prompt(repo_summary, all_module_docs)

# Generate
overview = claude.generate(prompt)

# Save as README.md
save_documentation("README.md", overview)
```

---

## Template Variable Reference

### Common Variables
- `{module_path}`: Full module path (e.g., "src/be")
- `{component_count}`: Number of components in module
- `{complexity_score}`: Calculated complexity metric
- `{cohesion}`: Internal cohesion percentage
- `{component_list}`: Formatted list of all components
- `{component_details}`: Detailed info for each component
- `{external_dependencies}`: List of external module dependencies
- `{external_dependents}`: List of modules that depend on this
- `{patterns}`: Detected architectural patterns
- `{diagram_data}`: Data formatted for diagram generation

### Component Variables
- `{component_id}`: Full qualified component ID
- `{component_name}`: Short component name
- `{component_type}`: Type (class, function, module, etc.)
- `{file_path}`: Path to source file
- `{inferred_role}`: Detected role (service, manager, etc.)
- `{inferred_purpose}`: Generated purpose description
- `{confidence}`: Confidence in inference (0-100)
- `{dependency_count}`: Number of dependencies
- `{dependent_count}`: Number of dependents

### Module Variables
- `{level}`: Depth in module tree
- `{child_count}`: Number of child modules
- `{child_module_list}`: List of child modules
- `{child_module_summaries}`: Summaries of each child
- `{cross_module_dependencies}`: Dependencies between children

### Repository Variables
- `{total_modules}`: Total module count
- `{total_components}`: Total component count
- `{max_depth}`: Maximum tree depth
- `{detected_architecture}`: Inferred architecture style
- `{root_modules}`: Top-level modules
- `{module_tree_visualization}`: ASCII or formatted tree view
