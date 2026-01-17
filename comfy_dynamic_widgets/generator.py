# SPDX-License-Identifier: MIT
# Copyright (C) 2025 ComfyUI-DynamicWidgets Contributors

"""
Mapping Generator - Transforms node visibility configs into JS-friendly JSON format.
"""


def generate_mappings(node_configs: dict) -> dict:
    """
    Transform node visibility configs into JS-friendly format.

    Args:
        node_configs: Output from scan_all_nodes()
        {
            "NodeClassName": {
                "selectors": {
                    "backend": {
                        "blender_voxel": ["voxel_size"],
                        ...
                    }
                }
            }
        }

    Returns:
        dict: JS-friendly mapping format
        {
            "version": 1,
            "nodes": {
                "NodeClassName": {
                    "selectors": {
                        "backend": {
                            "blender_voxel": ["voxel_size"],
                            ...
                        }
                    }
                }
            }
        }
    """
    return {
        "version": 1,
        "nodes": node_configs,
    }
