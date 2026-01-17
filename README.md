# comfy-dynamic-widgets

A Python library that enables conditional widget visibility in ComfyUI nodes via simple metadata.

## Installation

```bash
pip install comfy-dynamic-widgets
```

## Usage

### For Node Authors

Add `visible_when` metadata to widget definitions:

```python
@classmethod
def INPUT_TYPES(cls):
    return {
        "required": {
            "backend": (["option_a", "option_b", "option_c"], {"default": "option_a"}),
        },
        "optional": {
            "param_for_a": ("FLOAT", {
                "default": 0.1,
                "visible_when": {"backend": ["option_a"]},
            }),
            "param_for_b_and_c": ("INT", {
                "default": 10,
                "visible_when": {"backend": ["option_b", "option_c"]},
            }),
        }
    }
```

### For Custom Node Package Authors

In your `prestartup_script.py`:

```python
import json
import os

def generate_widget_mappings():
    try:
        from comfy_dynamic_widgets import scan_all_nodes, generate_mappings

        configs = scan_all_nodes()
        if not configs:
            return

        mappings = generate_mappings(configs)

        output_path = os.path.join(
            os.path.dirname(__file__), "web", "js", "mappings.json"
        )
        with open(output_path, "w") as f:
            json.dump(mappings, f, indent=2)

    except ImportError:
        print("comfy-dynamic-widgets not installed")

generate_widget_mappings()
```

Copy the `dynamic_widgets.js` from this package to your `web/js/` folder and update the mappings path.

## API

### `scan_all_nodes() -> dict`

Scans all registered ComfyUI nodes and extracts `visible_when` metadata.

### `generate_mappings(configs: dict) -> dict`

Transforms node visibility configs into a JS-friendly JSON format.

## License

MIT
