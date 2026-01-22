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

import os

__version__ = "0.0.3"

from .scanner import scan_all_nodes, scan_specific_nodes
from .generator import generate_mappings


def get_js_path() -> str:
    """Return path to the dynamic_widgets.js file in this package."""
    return os.path.join(os.path.dirname(__file__), "web", "js", "dynamic_widgets.js")


def get_web_dir() -> str:
    """Return path to the web/js directory in this package."""
    return os.path.join(os.path.dirname(__file__), "web", "js")


__all__ = ["scan_all_nodes", "scan_specific_nodes", "generate_mappings", "get_js_path", "get_web_dir", "__version__"]
