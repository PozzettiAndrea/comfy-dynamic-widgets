# SPDX-License-Identifier: MIT
# Copyright (C) 2025 ComfyUI-DynamicWidgets Contributors

"""
Node Scanner - Introspects ComfyUI nodes to extract visible_when metadata.
"""

from typing import Any


def scan_all_nodes() -> dict[str, dict]:
    """
    Scan all registered ComfyUI nodes and extract visible_when metadata.

    Returns:
        dict: Mapping of node_class -> visibility configuration
        {
            "NodeClassName": {
                "selectors": {
                    "selector_widget_name": {
                        "selector_value": ["widget1", "widget2"],
                        ...
                    }
                }
            }
        }
    """
    try:
        import nodes
    except ImportError:
        print("[DynamicWidgets] Warning: Could not import ComfyUI nodes module")
        return {}

    # Get the node class mappings from ComfyUI
    node_mappings = getattr(nodes, "NODE_CLASS_MAPPINGS", {})

    return scan_specific_nodes(node_mappings)


def scan_specific_nodes(node_mappings: dict[str, type]) -> dict[str, dict]:
    """
    Scan specific node classes for visible_when metadata.

    Args:
        node_mappings: Dict mapping node names to node classes
                       (same format as NODE_CLASS_MAPPINGS)

    Returns:
        dict: Mapping of node_class -> visibility configuration
    """
    results = {}

    for node_name, node_class in node_mappings.items():
        config = _scan_node_class(node_name, node_class)
        if config:
            results[node_name] = config

    return results


def _scan_node_class(node_name: str, node_class: type) -> dict | None:
    """
    Scan a single node class for visible_when metadata.

    Args:
        node_name: The registered name of the node
        node_class: The node class to scan

    Returns:
        dict or None: Visibility configuration if any visible_when found
    """
    # Get INPUT_TYPES - it's typically a classmethod
    if not hasattr(node_class, "INPUT_TYPES"):
        return None

    try:
        input_types = node_class.INPUT_TYPES()
    except Exception as e:
        print(f"[DynamicWidgets] Warning: Failed to call INPUT_TYPES for {node_name}: {e}")
        return None

    if not isinstance(input_types, dict):
        return None

    # Collect all visible_when entries
    # Structure: selector_name -> selector_value -> [widget_names]
    selectors: dict[str, dict[str, list[str]]] = {}

    # Scan both required and optional inputs
    for section in ["required", "optional"]:
        section_inputs = input_types.get(section, {})
        if not isinstance(section_inputs, dict):
            continue

        for widget_name, widget_def in section_inputs.items():
            visible_when = _extract_visible_when(widget_def)
            if visible_when:
                _add_to_selectors(selectors, widget_name, visible_when)

    if not selectors:
        return None

    return {"selectors": selectors}


def _extract_visible_when(widget_def: Any) -> dict | None:
    """
    Extract visible_when metadata from a widget definition.

    Widget definitions are typically tuples like:
        ("FLOAT", {"default": 0.1, "visible_when": {"backend": ["blender_voxel"]}})

    Args:
        widget_def: The widget definition tuple/list

    Returns:
        dict or None: The visible_when dict if present
    """
    if not isinstance(widget_def, (tuple, list)):
        return None

    if len(widget_def) < 2:
        return None

    # Second element should be the options dict
    options = widget_def[1]
    if not isinstance(options, dict):
        return None

    visible_when = options.get("visible_when")
    if not isinstance(visible_when, dict):
        return None

    return visible_when


def _add_to_selectors(
    selectors: dict[str, dict[str, list[str]]],
    widget_name: str,
    visible_when: dict
) -> None:
    """
    Add widget visibility rules to the selectors structure.

    Args:
        selectors: The selectors dict to update
        widget_name: The name of the widget with visible_when
        visible_when: The visible_when dict, e.g. {"backend": ["blender_voxel"]}
    """
    for selector_name, selector_values in visible_when.items():
        if not isinstance(selector_values, list):
            # Allow single value without list wrapper
            selector_values = [selector_values]

        if selector_name not in selectors:
            selectors[selector_name] = {}

        for value in selector_values:
            value_str = str(value)
            if value_str not in selectors[selector_name]:
                selectors[selector_name][value_str] = []

            if widget_name not in selectors[selector_name][value_str]:
                selectors[selector_name][value_str].append(widget_name)
