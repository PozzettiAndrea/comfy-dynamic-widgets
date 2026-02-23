# SPDX-License-Identifier: MIT
# Copyright (C) 2025 ComfyUI-DynamicWidgets Contributors

"""
Mapping Generator - Transforms node visibility configs into JS-friendly JSON format.

Version 2 format uses widget-centric rules with multi-selector AND logic:
{
    "version": 2,
    "nodes": {
        "NodeClassName": {
            "selectors": ["backend", "output_dim"],
            "rules": {
                "widget_name": {"backend": ["GMSH"], "output_dim": ["3D Volume"]},
                ...
            }
        }
    }
}
"""


def generate_mappings(node_configs: dict) -> dict:
    """
    Transform node visibility configs into JS-friendly format.

    Args:
        node_configs: Output from scan_all_nodes() / scan_specific_nodes()

    Returns:
        dict: JS-friendly mapping format (version 2)
    """
    return {
        "version": 2,
        "nodes": node_configs,
    }


def write_mappings(node_mappings: dict, caller_file: str) -> None:
    """Scan nodes for visible_when metadata and write mappings.json.

    Args:
        node_mappings: NODE_CLASS_MAPPINGS dict from the custom node package.
        caller_file: __file__ from the calling __init__.py, used to resolve
                     the output path (web/js/mappings.json relative to it).
    """
    import json
    import os
    from .scanner import scan_specific_nodes

    configs = scan_specific_nodes(node_mappings)
    if not configs:
        return

    mappings = generate_mappings(configs)
    output_path = os.path.join(os.path.dirname(caller_file), "web", "js", "mappings.json")
    with open(output_path, "w") as f:
        json.dump(mappings, f, indent=2)
