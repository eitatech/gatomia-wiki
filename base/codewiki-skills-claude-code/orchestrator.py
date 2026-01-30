#!/usr/bin/env python3
"""
CodeWiki Documentation Orchestrator
Coordinates the entire documentation generation process.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from codewiki_analyzer import CodeWikiAnalyzer


class CodeWikiOrchestrator:
    """Orchestrates the CodeWiki documentation generation process."""
    
    def __init__(self, module_tree_path: str, dependency_graph_path: str, 
                 output_dir: str = "./docs"):
        """Initialize orchestrator."""
        self.analyzer = CodeWikiAnalyzer(module_tree_path, dependency_graph_path)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Track generated docs
        self.generated_docs = {}
        
    def generate_all_documentation(self):
        """Generate complete documentation suite."""
        print("CodeWiki Documentation Generator")
        print("=" * 60)
        
        # Step 1: Analyze repository
        print("\nStep 1: Analyzing repository...")
        summary = self.analyzer.get_repository_summary()
        print(f"  Modules: {summary['total_modules']}")
        print(f"  Components: {summary['total_components']}")
        print(f"  Depth: {summary['max_depth']}")
        
        # Step 2: Get processing order
        print("\nStep 2: Determining processing order...")
        processing_order = self.analyzer.get_processing_order()
        print(f"  Levels to process: {len(processing_order)}")
        
        # Step 3: Generate leaf module documentation
        print("\nStep 3: Generating leaf module documentation...")
        leaf_count = 0
        for module_path in processing_order[0]:
            self._generate_leaf_module_doc(module_path)
            leaf_count += 1
            print(f"  [{leaf_count}/{len(processing_order[0])}] {module_path}")
        
        # Step 4: Generate parent module documentation
        if len(processing_order) > 1:
            print("\nStep 4: Generating parent module documentation...")
            parent_count = 0
            total_parents = sum(len(level) for level in processing_order[1:])
            
            for level_idx, level_modules in enumerate(processing_order[1:], 1):
                for module_path in level_modules:
                    self._generate_parent_module_doc(module_path)
                    parent_count += 1
                    print(f"  [{parent_count}/{total_parents}] Level {level_idx}: {module_path}")
        
        # Step 5: Generate repository overview
        print("\nStep 5: Generating repository overview...")
        self._generate_repository_overview()
        print("  ✓ README.md generated")
        
        # Step 6: Generate index and navigation
        print("\nStep 6: Generating navigation...")
        self._generate_navigation()
        print("  ✓ Navigation generated")
        
        print("\n" + "=" * 60)
        print(f"Documentation generated in: {self.output_dir}")
        print(f"Total files: {len(self.generated_docs)}")
        print("=" * 60)
    
    def _generate_leaf_module_doc(self, module_path: str):
        """Generate documentation for a leaf module."""
        # Get analysis
        report = self.analyzer.generate_analysis_report(module_path)
        
        # Build prompt data
        prompt_data = self._build_leaf_module_prompt_data(report)
        
        # Generate markdown (this would call Claude in production)
        markdown = self._format_leaf_module_markdown(report, prompt_data)
        
        # Save
        output_path = self._get_module_doc_path(module_path)
        self._save_documentation(output_path, markdown)
        self.generated_docs[module_path] = output_path
    
    def _generate_parent_module_doc(self, module_path: str):
        """Generate documentation for a parent module."""
        # Get module info
        module_info = self.analyzer.parsed_tree['modules'][module_path]
        
        # Get child documentation
        child_docs = {}
        for child_path in self._get_child_modules(module_path):
            if child_path in self.generated_docs:
                child_docs[child_path] = self._load_documentation(
                    self.generated_docs[child_path]
                )
        
        # Build prompt data
        prompt_data = self._build_parent_module_prompt_data(
            module_path, module_info, child_docs
        )
        
        # Generate markdown
        markdown = self._format_parent_module_markdown(
            module_path, module_info, child_docs, prompt_data
        )
        
        # Save
        output_path = self._get_module_doc_path(module_path)
        self._save_documentation(output_path, markdown)
        self.generated_docs[module_path] = output_path
    
    def _generate_repository_overview(self):
        """Generate repository-level overview documentation."""
        summary = self.analyzer.get_repository_summary()
        
        # Get all module summaries
        module_summaries = {}
        for module_path in self.analyzer.parsed_tree['root_modules']:
            if module_path in self.generated_docs:
                module_summaries[module_path] = self._extract_module_summary(
                    self.generated_docs[module_path]
                )
        
        # Generate markdown
        markdown = self._format_repository_overview_markdown(
            summary, module_summaries
        )
        
        # Save
        output_path = self.output_dir / "README.md"
        self._save_documentation(output_path, markdown)
        self.generated_docs['_repository_overview'] = output_path
    
    def _generate_navigation(self):
        """Generate navigation index."""
        nav_content = "# Documentation Index\n\n"
        nav_content += "## Module Documentation\n\n"
        
        # Build tree view
        for module_path in sorted(self.generated_docs.keys()):
            if module_path.startswith('_'):
                continue
            
            level = self.analyzer.parsed_tree['modules'][module_path]['level']
            indent = "  " * level
            rel_path = self._get_relative_path(
                self.output_dir / "INDEX.md",
                self.generated_docs[module_path]
            )
            
            nav_content += f"{indent}- [{module_path}]({rel_path})\n"
        
        # Save
        output_path = self.output_dir / "INDEX.md"
        self._save_documentation(output_path, nav_content)
    
    # ===== PROMPT DATA BUILDERS =====
    
    def _build_leaf_module_prompt_data(self, report: Dict) -> Dict:
        """Build data dictionary for leaf module prompt."""
        module_info = report['summary']
        
        # Component list
        component_list = []
        for comp_id in report['components']:
            comp_info = report['components'][comp_id]['info']
            purpose = report['components'][comp_id]['purpose']
            component_list.append(
                f"- **{comp_info['name']}** ({comp_info['component_type']}): "
                f"{purpose['primary_purpose']}"
            )
        
        # External dependencies
        ext_deps = []
        for dep in report['dependencies']:
            ext_deps.append(
                f"- **{dep['target_module']}** "
                f"({len(dep['relationships'])} relationships)"
            )
        
        # External dependents
        ext_dependents = []
        for dep in report['dependents']:
            ext_dependents.append(
                f"- **{dep['source_module']}** "
                f"({len(dep['relationships'])} relationships)"
            )
        
        return {
            'module_path': report['module'],
            'component_count': module_info['component_count'],
            'complexity_score': report['complexity']['internal_edge_count'] + 
                              report['complexity']['external_edge_count'],
            'cohesion': round(report['complexity']['cohesion_score'] * 100, 2),
            'component_list': '\n'.join(component_list),
            'external_dependencies': '\n'.join(ext_deps) if ext_deps else "None",
            'external_dependents': '\n'.join(ext_dependents) if ext_dependents else "None",
            'patterns': self._format_patterns(report['patterns'])
        }
    
    def _build_parent_module_prompt_data(self, module_path: str, 
                                        module_info: Dict, 
                                        child_docs: Dict) -> Dict:
        """Build data dictionary for parent module prompt."""
        child_list = []
        for child_path in self._get_child_modules(module_path):
            if child_path in child_docs:
                summary = self._extract_module_summary_from_content(
                    child_docs[child_path]
                )
                child_list.append(f"- **{child_path}**: {summary}")
        
        return {
            'module_path': module_path,
            'level': module_info['level'],
            'child_count': len(module_info['children']),
            'child_module_list': '\n'.join(child_list)
        }
    
    # ===== MARKDOWN FORMATTERS =====
    
    def _format_leaf_module_markdown(self, report: Dict, 
                                     prompt_data: Dict) -> str:
        """Format leaf module documentation as markdown."""
        md = f"# Module: {report['module']}\n\n"
        
        # Overview
        md += "## Overview\n\n"
        md += f"This module contains {report['summary']['component_count']} components "
        md += f"with a cohesion score of {prompt_data['cohesion']}%. "
        md += self._infer_module_purpose(report) + "\n\n"
        
        # Architecture
        md += "## Architecture\n\n"
        md += self._generate_architecture_description(report) + "\n\n"
        md += self._generate_component_diagram(report) + "\n\n"
        
        # Components
        md += "## Components\n\n"
        for comp_id, comp_data in report['components'].items():
            md += self._format_component_section(comp_id, comp_data)
        
        # Dependencies
        if report['dependencies']:
            md += "## External Dependencies\n\n"
            for dep in report['dependencies']:
                md += f"### {dep['target_module']}\n"
                md += f"- {len(dep['relationships'])} relationship(s)\n\n"
        
        # Dependents
        if report['dependents']:
            md += "## Used By\n\n"
            for dep in report['dependents']:
                md += f"### {dep['source_module']}\n"
                md += f"- {len(dep['relationships'])} relationship(s)\n\n"
        
        # Patterns
        if report['patterns']['patterns']:
            md += "## Architectural Patterns\n\n"
            for pattern in report['patterns']['patterns']:
                md += f"### {pattern['type'].title()} Pattern\n"
                md += f"- **Confidence**: {pattern['confidence'] * 100:.0f}%\n"
                md += f"- **Evidence**: {', '.join(pattern['evidence'])}\n\n"
        
        return md
    
    def _format_parent_module_markdown(self, module_path: str, 
                                      module_info: Dict,
                                      child_docs: Dict,
                                      prompt_data: Dict) -> str:
        """Format parent module documentation as markdown."""
        md = f"# Module: {module_path}\n\n"
        
        # Overview
        md += "## Overview\n\n"
        md += f"This is a parent module containing {len(module_info['children'])} submodules. "
        md += self._infer_parent_module_purpose(module_path, child_docs) + "\n\n"
        
        # Architecture
        md += "## Architecture\n\n"
        md += self._generate_parent_architecture_description(
            module_path, child_docs
        ) + "\n\n"
        md += self._generate_module_hierarchy_diagram(module_path) + "\n\n"
        
        # Submodules
        md += "## Submodules\n\n"
        for child_path in self._get_child_modules(module_path):
            if child_path in child_docs:
                summary = self._extract_module_summary_from_content(
                    child_docs[child_path]
                )
                rel_path = self._get_relative_path(
                    self._get_module_doc_path(module_path),
                    self.generated_docs[child_path]
                )
                md += f"### [{child_path}]({rel_path})\n"
                md += f"{summary}\n\n"
        
        return md
    
    def _format_repository_overview_markdown(self, summary: Dict,
                                           module_summaries: Dict) -> str:
        """Format repository overview documentation as markdown."""
        md = "# Repository Documentation\n\n"
        
        # Purpose (would need repo name from config or inference)
        md += "## Purpose\n\n"
        md += "This repository contains a modular software system organized into "
        md += f"{summary['total_modules']} modules with {summary['total_components']} components.\n\n"
        
        # Architecture Overview
        md += "## Architecture Overview\n\n"
        md += f"The system is organized in a {summary['max_depth']}-level hierarchy:\n\n"
        md += self._generate_repository_architecture_diagram() + "\n\n"
        
        # Module Structure
        md += "## Module Structure\n\n"
        for module_path, module_summary in module_summaries.items():
            if module_path in self.generated_docs:
                rel_path = self._get_relative_path(
                    self.output_dir / "README.md",
                    self.generated_docs[module_path]
                )
                md += f"### [{module_path}]({rel_path})\n"
                md += f"{module_summary}\n\n"
        
        # Getting Started
        md += "## Getting Started\n\n"
        md += "Start by exploring the root modules:\n\n"
        for module_path in self.analyzer.parsed_tree['root_modules']:
            if module_path in self.generated_docs:
                rel_path = self._get_relative_path(
                    self.output_dir / "README.md",
                    self.generated_docs[module_path]
                )
                md += f"- [{module_path}]({rel_path})\n"
        
        return md
    
    # ===== HELPER METHODS =====
    
    def _infer_module_purpose(self, report: Dict) -> str:
        """Infer module purpose from components."""
        # Collect component roles
        roles = []
        for comp_data in report['components'].values():
            roles.append(comp_data['purpose']['role'])
        
        # Determine dominant pattern
        if 'analyzer' in roles or 'parser' in roles:
            return "It provides data analysis and parsing capabilities."
        elif 'service' in roles:
            return "It implements business logic and services."
        elif 'manager' in roles:
            return "It manages resources and orchestrates operations."
        elif 'generator' in roles:
            return "It generates or constructs data and objects."
        else:
            return "It provides core functionality for the system."
    
    def _infer_parent_module_purpose(self, module_path: str, 
                                    child_docs: Dict) -> str:
        """Infer parent module purpose from children."""
        # Simple heuristic based on module path
        if 'fe' in module_path.lower():
            return "It manages the frontend layer of the application."
        elif 'be' in module_path.lower():
            return "It manages the backend layer of the application."
        elif 'cli' in module_path.lower():
            return "It provides command-line interface functionality."
        else:
            return "It coordinates its submodules to provide system functionality."
    
    def _generate_architecture_description(self, report: Dict) -> str:
        """Generate architecture description for a module."""
        desc = "The module is organized with the following structure:\n\n"
        
        # Describe component relationships
        internal_count = report['complexity']['internal_edge_count']
        external_count = report['complexity']['external_edge_count']
        
        if internal_count > 0:
            desc += f"- **Internal Dependencies**: {internal_count} relationships between components\n"
        
        if external_count > 0:
            desc += f"- **External Dependencies**: {external_count} relationships with other modules\n"
        
        # Describe cohesion
        cohesion = report['complexity']['cohesion_score']
        if cohesion > 0.7:
            desc += "- **High cohesion**: Components are closely related\n"
        elif cohesion > 0.4:
            desc += "- **Moderate cohesion**: Components have some independence\n"
        else:
            desc += "- **Low cohesion**: Components are relatively independent\n"
        
        return desc
    
    def _generate_parent_architecture_description(self, module_path: str,
                                                 child_docs: Dict) -> str:
        """Generate architecture description for parent module."""
        desc = "The parent module coordinates the following submodules:\n\n"
        
        for child_path in self._get_child_modules(module_path):
            if child_path in child_docs:
                desc += f"- **{child_path}**: "
                desc += self._extract_module_summary_from_content(child_docs[child_path])
                desc += "\n"
        
        return desc
    
    def _generate_component_diagram(self, report: Dict) -> str:
        """Generate Mermaid diagram for components."""
        diagram = "```mermaid\ngraph LR\n"
        
        # Add nodes for each component
        comp_nodes = {}
        for idx, comp_id in enumerate(report['components']):
            node_id = f"C{idx}"
            comp_name = report['components'][comp_id]['info']['name']
            comp_nodes[comp_id] = node_id
            diagram += f"    {node_id}[{comp_name}]\n"
        
        # Add internal edges
        for dep in report.get('internal_dependencies', []):
            from_id = comp_nodes.get(dep['from'])
            to_id = comp_nodes.get(dep['to'])
            if from_id and to_id:
                diagram += f"    {from_id} --> {to_id}\n"
        
        # Style
        for node_id in comp_nodes.values():
            diagram += f"    style {node_id} fill:#e1f5ff\n"
        
        diagram += "```\n"
        return diagram
    
    def _generate_module_hierarchy_diagram(self, module_path: str) -> str:
        """Generate Mermaid diagram for module hierarchy."""
        diagram = "```mermaid\ngraph TB\n"
        
        module_info = self.analyzer.parsed_tree['modules'][module_path]
        
        # Parent node
        diagram += f"    P[{module_path}]\n"
        
        # Child nodes
        for idx, child_path in enumerate(self._get_child_modules(module_path)):
            child_id = f"C{idx}"
            diagram += f"    {child_id}[{child_path}]\n"
            diagram += f"    P --> {child_id}\n"
        
        diagram += "```\n"
        return diagram
    
    def _generate_repository_architecture_diagram(self) -> str:
        """Generate Mermaid diagram for repository architecture."""
        diagram = "```mermaid\ngraph TB\n"
        
        # Root modules
        for idx, module_path in enumerate(self.analyzer.parsed_tree['root_modules']):
            mod_id = f"M{idx}"
            diagram += f"    {mod_id}[{module_path}]\n"
        
        diagram += "```\n"
        return diagram
    
    def _format_component_section(self, comp_id: str, comp_data: Dict) -> str:
        """Format a component section."""
        info = comp_data['info']
        purpose = comp_data['purpose']
        deps = comp_data['dependencies']
        
        md = f"### {info['name']}\n\n"
        md += f"**Type**: {info['component_type']}\n"
        md += f"**File**: `{info['relative_path']}`\n\n"
        md += f"**Purpose**: {purpose['primary_purpose']}\n\n"
        
        if deps['internal_dependencies']:
            md += "**Internal Dependencies**:\n"
            for dep in deps['internal_dependencies']:
                md += f"- {dep['name']}\n"
            md += "\n"
        
        if deps['external_dependencies']:
            md += "**External Dependencies**:\n"
            for dep in deps['external_dependencies']:
                md += f"- {dep['name']} ({dep.get('module', 'unknown')})\n"
            md += "\n"
        
        return md
    
    def _format_patterns(self, patterns: Dict) -> str:
        """Format detected patterns."""
        if not patterns['patterns']:
            return "No specific patterns detected."
        
        result = []
        for pattern in patterns['patterns']:
            result.append(
                f"- **{pattern['type'].title()}**: "
                f"{pattern['confidence'] * 100:.0f}% confidence"
            )
        
        return '\n'.join(result)
    
    def _get_child_modules(self, module_path: str) -> List[str]:
        """Get direct children of a module."""
        module_info = self.analyzer.parsed_tree['modules'][module_path]
        return list(module_info['children'].keys())
    
    def _get_module_doc_path(self, module_path: str) -> Path:
        """Get output path for module documentation."""
        # Convert module path to file path
        path_parts = module_path.split('/')
        doc_path = self.output_dir / "modules"
        
        for part in path_parts:
            doc_path = doc_path / part
        
        doc_path.mkdir(parents=True, exist_ok=True)
        return doc_path / "README.md"
    
    def _get_relative_path(self, from_path: Path, to_path: Path) -> str:
        """Get relative path between two paths."""
        try:
            return os.path.relpath(to_path, from_path.parent)
        except:
            return str(to_path)
    
    def _save_documentation(self, path: Path, content: str):
        """Save documentation to file."""
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def _load_documentation(self, path: Path) -> str:
        """Load documentation from file."""
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _extract_module_summary(self, doc_path: Path) -> str:
        """Extract summary from module documentation."""
        content = self._load_documentation(doc_path)
        return self._extract_module_summary_from_content(content)
    
    def _extract_module_summary_from_content(self, content: str) -> str:
        """Extract summary from documentation content."""
        # Extract first paragraph under "## Overview"
        lines = content.split('\n')
        in_overview = False
        summary_lines = []
        
        for line in lines:
            if line.startswith('## Overview'):
                in_overview = True
                continue
            
            if in_overview:
                if line.startswith('#'):
                    break
                if line.strip():
                    summary_lines.append(line.strip())
                    if len(summary_lines) >= 2:  # First 2 sentences
                        break
        
        return ' '.join(summary_lines) if summary_lines else "Module documentation."


def main():
    """Main entry point."""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python orchestrator.py <module_tree.json> <dependency_graph.json> [output_dir]")
        sys.exit(1)
    
    module_tree_path = sys.argv[1]
    dep_graph_path = sys.argv[2]
    output_dir = sys.argv[3] if len(sys.argv) > 3 else "./docs"
    
    orchestrator = CodeWikiOrchestrator(module_tree_path, dep_graph_path, output_dir)
    orchestrator.generate_all_documentation()


if __name__ == '__main__':
    main()
