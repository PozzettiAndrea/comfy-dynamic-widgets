# SPDX-License-Identifier: MIT
# Copyright (C) 2025 Comfy-DynamicWidgets Contributors

"""
Comfy Dynamic Widgets

A standalone package that enables conditional widget visibility in ComfyUI nodes
via simple metadata. Node authors can use "visible_when" in widget definitions
to show/hide widgets based on selector values.

Usage in node definitions:
    "voxel_size": ("FLOAT", {
        "default": 0.1,
        "visible_when": {"backend": ["blender_voxel"]},
    })
"""

__version__ = "0.0.2"

from .scanner import scan_all_nodes
from .generator import generate_mappings

__all__ = ["scan_all_nodes", "generate_mappings", "__version__"]
