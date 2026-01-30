# CodeWiki Data Analyzer - Helper Skill

## Purpose
This sub-skill provides utilities for analyzing module trees and dependency graphs to extract structured information needed for documentation generation.

## Core Functions

### 1. Module Tree Analysis

#### Parse Module Tree
```python
def parse_module_tree(module_tree_json):
    """
    Parse the module tree structure and extract:
    - All modules (leaf and parent)
    - Module hierarchy relationships
    - Component assignments to modules
    
    Returns:
    {
        'modules': {
            'module_path': {
                'path': str,
                'components': [list of component IDs],
                'children': {dict of child modules},
                'parent': parent_module_path or None,
                'is_leaf': bool,
                'level': int  # depth in tree
            }
        },
        'leaf_modules': [list of leaf module paths],
        'parent_modules': [list of parent module paths],
        'root_modules': [list of top-level modules],
        'component_to_module': {component_id: module_path}
    }
    """
```

#### Identify Processing Order
```python
def get_processing_order(parsed_tree):
    """
    Determine the order to process modules for bottom-up synthesis.
    
    Returns: [
        [level_0_leaf_modules],  # Process first
        [level_1_parent_modules],
        [level_2_parent_modules],
        ...
        [root_level_modules]  # Process last
    ]
    """
```

### 2. Dependency Graph Analysis

#### Build Component Map
```python
def build_component_map(dependency_graph):
    """
    Create comprehensive component information map.
    
    Returns: {
        component_id: {
            'id': str,
            'name': str,
            'component_type': str,
            'file_path': str,
            'relative_path': str,
            'depends_on': [list of component IDs],
            'depended_by': [list of component IDs],  # Reverse lookup
            'module': module_path,
            'dependency_count': int,
            'dependent_count': int
        }
    }
    """
```

#### Analyze Dependencies
```python
def analyze_dependencies(component_id, component_map, module_map):
    """
    Analyze dependencies for a specific component.
    
    Returns: {
        'internal_dependencies': [  # Same module
            {'id': str, 'name': str, 'type': str}
        ],
        'external_dependencies': [  # Different module
            {'id': str, 'name': str, 'type': str, 'module': str}
        ],
        'internal_dependents': [  # Same module depends on this
            {'id': str, 'name': str, 'type': str}
        ],
        'external_dependents': [  # Different module depends on this
            {'id': str, 'name': str, 'type': str, 'module': str}
        ],
        'dependency_modules': [unique list of external modules depended on],
        'dependent_modules': [unique list of modules that depend on this]
    }
    """
```

### 3. Module-Level Analysis

#### Analyze Module Dependencies
```python
def analyze_module_dependencies(module_path, parsed_tree, component_map):
    """
    Analyze dependencies at the module level.
    
    Returns: {
        'module': module_path,
        'components': [list of component IDs],
        'internal_dependencies': [  # Dependencies within module
            {'from': component_id, 'to': component_id, 'type': str}
        ],
        'external_dependencies': [  # Module dependencies
            {
                'target_module': module_path,
                'relationships': [
                    {'from_component': id, 'to_component': id}
                ]
            }
        ],
        'external_dependents': [  # Modules that depend on this
            {
                'source_module': module_path,
                'relationships': [
                    {'from_component': id, 'to_component': id}
                ]
            }
        ],
        'complexity': {
            'component_count': int,
            'internal_edge_count': int,
            'external_edge_count': int,
            'cohesion_score': float  # internal/(internal+external)
        }
    }
    """
```

### 4. Pattern Detection

#### Detect Architectural Patterns
```python
def detect_patterns(module_analysis):
    """
    Detect common architectural patterns in a module.
    
    Returns: {
        'patterns': [
            {
                'type': 'layered|plugin|adapter|factory|observer|...',
                'confidence': float,
                'evidence': [list of supporting observations],
                'components': [relevant component IDs]
            }
        ],
        'component_roles': {
            component_id: {
                'role': 'controller|service|model|utility|adapter|...',
                'confidence': float,
                'reasoning': str
            }
        }
    }
    """
```

#### Infer Component Purpose
```python
def infer_component_purpose(component_id, component_info, dependencies):
    """
    Infer the purpose of a component based on available information.
    
    Returns: {
        'primary_purpose': str,  # Short description
        'role': str,  # controller|service|model|utility|adapter|...
        'key_responsibilities': [list of inferred responsibilities],
        'confidence': float,
        'reasoning': [list of evidence points]
    }
    """
    
    # Analysis heuristics:
    # 1. Name-based inference
    # 2. Type-based inference (class vs function vs module)
    # 3. Dependency pattern analysis
    # 4. Dependent pattern analysis
```

### 5. Data Flow Analysis

#### Trace Data Flow
```python
def trace_data_flow(start_component, component_map, max_depth=3):
    """
    Trace data flow from a starting component.
    
    Returns: {
        'flows': [
            {
                'path': [component_id_1, component_id_2, ...],
                'description': str,
                'type': 'sequential|branching|converging'
            }
        ],
        'entry_points': [components with no dependencies],
        'exit_points': [components with no dependents],
        'critical_components': [components on many paths]
    }
    """
```

### 6. Complexity Metrics

#### Calculate Module Complexity
```python
def calculate_module_complexity(module_path, module_analysis):
    """
    Calculate various complexity metrics.
    
    Returns: {
        'component_count': int,
        'total_dependencies': int,
        'external_dependency_count': int,
        'cyclomatic_complexity_estimate': int,
        'coupling': float,  # External deps / total deps
        'cohesion': float,  # Internal deps / total deps
        'fan_in': int,  # Modules depending on this
        'fan_out': int,  # Modules this depends on
        'instability': float,  # fan_out / (fan_in + fan_out)
        'abstractness_estimate': float,  # Based on component types
        'maintainability_index': float  # Composite score
    }
    """
```

## Usage Examples

### Example 1: Analyze a Leaf Module
```python
# Load data
module_tree = load_json("module_tree.json")
dep_graph = load_json("dependency_graph.json")

# Parse
parsed = parse_module_tree(module_tree)
comp_map = build_component_map(dep_graph)

# Analyze specific module
module_path = "src/fe"
module_analysis = analyze_module_dependencies(module_path, parsed, comp_map)

# Detect patterns
patterns = detect_patterns(module_analysis)

# Get component purposes
for comp_id in parsed['modules'][module_path]['components']:
    purpose = infer_component_purpose(
        comp_id,
        comp_map[comp_id],
        module_analysis
    )
    print(f"{comp_id}: {purpose['primary_purpose']}")
```

### Example 2: Get Processing Order
```python
parsed = parse_module_tree(module_tree)
order = get_processing_order(parsed)

for level, modules in enumerate(order):
    print(f"Level {level}: {modules}")
```

### Example 3: Full Module Analysis Report
```python
def generate_module_analysis_report(module_path):
    # Load and parse
    module_tree = load_json("module_tree.json")
    dep_graph = load_json("dependency_graph.json")
    parsed = parse_module_tree(module_tree)
    comp_map = build_component_map(dep_graph)
    
    # Analyze
    analysis = analyze_module_dependencies(module_path, parsed, comp_map)
    patterns = detect_patterns(analysis)
    complexity = calculate_module_complexity(module_path, analysis)
    
    # Generate report
    report = {
        'module': module_path,
        'summary': {
            'components': len(analysis['components']),
            'is_leaf': parsed['modules'][module_path]['is_leaf'],
            'level': parsed['modules'][module_path]['level']
        },
        'dependencies': analysis['external_dependencies'],
        'dependents': analysis['external_dependents'],
        'patterns': patterns,
        'complexity': complexity,
        'components': {}
    }
    
    # Analyze each component
    for comp_id in analysis['components']:
        comp_deps = analyze_dependencies(comp_id, comp_map, parsed['component_to_module'])
        purpose = infer_component_purpose(comp_id, comp_map[comp_id], comp_deps)
        
        report['components'][comp_id] = {
            'info': comp_map[comp_id],
            'dependencies': comp_deps,
            'purpose': purpose
        }
    
    return report
```

## Pattern Detection Heuristics

### Layered Architecture
```python
# Detect by checking if dependencies flow in one direction
# Components can be grouped into layers with no upward dependencies
def detect_layered(module_analysis):
    # Check for clear dependency direction
    # Look for groupings with minimal cross-group dependencies
    pass
```

### Plugin/Extension Pattern
```python
# Multiple components with similar interfaces
# Common base or interface component
def detect_plugin(module_analysis, component_map):
    # Look for components with similar names (e.g., *Plugin, *Analyzer, *Handler)
    # Check for common dependencies suggesting shared interface
    pass
```

### Facade Pattern
```python
# Single component with many dependents from outside
# That component uses many internal components
def detect_facade(module_analysis):
    # Find component with high external fan-in, high internal fan-out
    pass
```

### Observer/Event Pattern
```python
# Components named *Event, *Listener, *Handler
# One-to-many dependency relationships
def detect_observer(component_map):
    # Look for event-related naming
    # Check for one component having many dependents
    pass
```

## Implementation Strategy

### Phase 1: Data Loading
```python
def load_and_validate():
    """Load JSON files and validate structure."""
    try:
        module_tree = load_json("module_tree.json")
        dep_graph = load_json("dependency_graph.json")
        
        # Validate structure
        assert isinstance(module_tree, dict)
        assert isinstance(dep_graph, dict)
        
        return module_tree, dep_graph
    except Exception as e:
        raise ValueError(f"Invalid input files: {e}")
```

### Phase 2: Parsing
```python
def parse_all_data(module_tree, dep_graph):
    """Parse and cross-reference all data."""
    parsed_tree = parse_module_tree(module_tree)
    component_map = build_component_map(dep_graph)
    
    # Cross-reference: assign modules to components
    for comp_id, comp_info in component_map.items():
        if comp_id in parsed_tree['component_to_module']:
            comp_info['module'] = parsed_tree['component_to_module'][comp_id]
    
    return parsed_tree, component_map
```

### Phase 3: Analysis
```python
def analyze_repository(parsed_tree, component_map):
    """Perform comprehensive repository analysis."""
    results = {
        'summary': {
            'total_modules': len(parsed_tree['modules']),
            'leaf_modules': len(parsed_tree['leaf_modules']),
            'total_components': len(component_map)
        },
        'modules': {},
        'processing_order': get_processing_order(parsed_tree)
    }
    
    # Analyze each module
    for module_path in parsed_tree['modules']:
        results['modules'][module_path] = generate_module_analysis_report(module_path)
    
    return results
```

## Quick Reference: Key Metrics

### Component-Level Metrics
- **Fan-In**: Number of components that depend on this one
- **Fan-Out**: Number of components this depends on
- **Coupling**: Degree of interdependence with other components
- **Role**: Inferred responsibility (controller, service, model, etc.)

### Module-Level Metrics
- **Cohesion**: How closely related components are (internal deps / total deps)
- **Coupling**: How dependent on other modules (external deps / total deps)
- **Complexity**: Number of components and relationships
- **Stability**: Resistance to change (based on dependents)

### Repository-Level Metrics
- **Modularity**: How well-separated concerns are
- **Hierarchy Depth**: Levels in module tree
- **Cross-Module Coupling**: Average module coupling
- **Architectural Clarity**: How clearly patterns emerge

## Notes
- All analysis functions should be **deterministic** and **efficient**
- Use **caching** for expensive computations
- Provide **progress indicators** for large repositories
- Handle **missing data** gracefully (some components may not be in module tree)
- Support **incremental analysis** for interactive use
