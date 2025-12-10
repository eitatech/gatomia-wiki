from typing import List, Dict, Any
from collections import defaultdict
import logging
logger = logging.getLogger(__name__)

from gatowiki.src.be.dependency_analyzer.models.core import Node
from gatowiki.src.be.utils import count_tokens
from gatowiki.src.config import MAX_TOKEN_PER_MODULE, Config

# NOTE: LLM-based clustering removed - GitHub Copilot agents handle module clustering
# through chat interface. This file kept for reference but clustering functions are deprecated.


# Prompt templates for module clustering
CLUSTER_REPO_PROMPT = """
Here is list of all potential core components of the repository (It's normal that some components are not essential to the repository):
<POTENTIAL_CORE_COMPONENTS>
{potential_core_components}
</POTENTIAL_CORE_COMPONENTS>

Please group the components into groups such that each group is a set of components that are closely related to each other and together they form a module. DO NOT include components that are not essential to the repository.
Firstly reason about the components and then group them and return the result in the following format:
<GROUPED_COMPONENTS>
{{
    "module_name_1": {{
        "path": <path_to_the_module_1>, # the path to the module can be file or directory
        "components": [
            <component_name_1>,
            <component_name_2>,
            ...
        ]
    }},
    "module_name_2": {{
        "path": <path_to_the_module_2>,
        "components": [
            <component_name_1>,
            <component_name_2>,
            ...
        ]
    }},
    ...
}}
</GROUPED_COMPONENTS>
""".strip()

CLUSTER_MODULE_PROMPT = """
Here is the module tree of a repository:

<MODULE_TREE>
{module_tree}
</MODULE_TREE>

Here is list of all potential core components of the module {module_name} (It's normal that some components are not essential to the module):
<POTENTIAL_CORE_COMPONENTS>
{potential_core_components}
</POTENTIAL_CORE_COMPONENTS>

Please group the components into groups such that each group is a set of components that are closely related to each other and together they form a smaller module. DO NOT include components that are not essential to the module.

Firstly reason based on given context and then group them and return the result in the following format:
<GROUPED_COMPONENTS>
{{
    "module_name_1": {{
        "path": <path_to_the_module_1>, # the path to the module can be file or directory
        "components": [
            <component_name_1>,
            <component_name_2>,
            ...
        ]
    }},
    "module_name_2": {{
        "path": <path_to_the_module_2>,
        "components": [
            <component_name_1>,
            <component_name_2>,
            ...
        ]
    }},
    ...
}}
</GROUPED_COMPONENTS>
""".strip()


def format_cluster_prompt(potential_core_components: str, module_tree: dict[str, any] = {}, module_name: str = None) -> str:
    """
    Format the cluster prompt with potential core components and module tree.
    """

    # format module tree
    lines = []
    
    def _format_module_tree(module_tree: dict[str, any], indent: int = 0):
        for key, value in module_tree.items():
            if key == module_name:
                lines.append(f"{'  ' * indent}{key} (current module)")
            else:
                lines.append(f"{'  ' * indent}{key}")
            
            lines.append(f"{'  ' * (indent + 1)} Core components: {', '.join(value['components'])}")
            if ("children" in value) and isinstance(value["children"], dict) and len(value["children"]) > 0:
                lines.append(f"{'  ' * (indent + 1)} Children:")
                _format_module_tree(value["children"], indent + 2)
    
    _format_module_tree(module_tree, 0)
    formatted_module_tree = "\n".join(lines)

    if module_tree == {}:
        return CLUSTER_REPO_PROMPT.format(potential_core_components=potential_core_components)
    else:
        return CLUSTER_MODULE_PROMPT.format(potential_core_components=potential_core_components, module_tree=formatted_module_tree, module_name=module_name)


def format_potential_core_components(leaf_nodes: List[str], components: Dict[str, Node]) -> tuple[str, str]:
    """
    Format the potential core components into a string that can be used in the prompt.
    """
    # Filter out any invalid leaf nodes that don't exist in components
    valid_leaf_nodes = []
    for leaf_node in leaf_nodes:
        if leaf_node in components:
            valid_leaf_nodes.append(leaf_node)
        else:
            logger.warning(f"Skipping invalid leaf node '{leaf_node}' - not found in components")
    
    #group leaf nodes by file
    leaf_nodes_by_file = defaultdict(list)
    for leaf_node in valid_leaf_nodes:
        leaf_nodes_by_file[components[leaf_node].relative_path].append(leaf_node)

    potential_core_components = ""
    potential_core_components_with_code = ""
    for file, leaf_nodes in dict(sorted(leaf_nodes_by_file.items())).items():
        potential_core_components += f"# {file}\n"
        potential_core_components_with_code += f"# {file}\n"
        for leaf_node in leaf_nodes:
            potential_core_components += f"\t{leaf_node}\n"
            potential_core_components_with_code += f"\t{leaf_node}\n"
            potential_core_components_with_code += f"{components[leaf_node].source_code}\n"

    return potential_core_components, potential_core_components_with_code


def cluster_modules(
    leaf_nodes: List[str],
    components: Dict[str, Node],
    config: Config,
    current_module_tree: dict[str, Any] = {},
    current_module_name: str = None,
    current_module_path: List[str] = []
) -> Dict[str, Any]:
    """
    Basic directory-based clustering for initial module tree.
    
    Groups components by their directory structure to create a starting point
    for GitHub Copilot agents. Agents can refine this clustering through chat.
    
    Returns:
        Dict mapping module names to their components and metadata
    """
    logger.info("Clustering components into modules...")
    
    # Group components by directory
    modules_by_dir = defaultdict(lambda: {"components": [], "children": {}})
    
    for leaf_node in leaf_nodes:
        if leaf_node not in components:
            continue
            
        component = components[leaf_node]
        file_path = component.relative_path
        
        # Extract directory path
        # e.g., "gatowiki/cli/commands/config.py" -> "cli"
        #       "src/be/analyzer/parser.py" -> "be"
        parts = file_path.split('/')
        
        # Skip if file is at root
        if len(parts) <= 1:
            continue
        
        # Skip common top-level directories and use next level
        # e.g., "gatowiki/cli/..." -> "cli", "gatowiki/src/be/..." -> "src/be"
        if parts[0] in ['gatowiki', 'lib', 'app'] and len(parts) > 2:
            # For gatowiki/cli -> "cli", gatowiki/src/be -> "src/be"
            if parts[1] == 'src' and len(parts) > 3:
                module_name = f"{parts[1]}/{parts[2]}"  # src/be, src/fe, etc
            else:
                module_name = parts[1]  # cli, etc
        elif parts[0] == 'src' and len(parts) > 2:
            # For src/be/... -> "be"
            module_name = parts[1]
        else:
            module_name = parts[0]
        
        # Add component to module
        modules_by_dir[module_name]["components"].append(leaf_node)
        modules_by_dir[module_name]["path"] = module_name
    
    # Convert to regular dict and filter empty modules
    module_tree = {}
    for module_name, module_data in modules_by_dir.items():
        if module_data["components"]:
            module_tree[module_name] = {
                "components": sorted(module_data["components"]),
                "path": module_data["path"],
                "children": module_data["children"]
            }
    
    logger.info(f"Clustered {len(leaf_nodes)} components into {len(module_tree)} top-level modules")
    logger.info(f"Module names: {', '.join(sorted(module_tree.keys()))}")
    
    return module_tree
