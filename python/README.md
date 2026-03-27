# Python CAD Bridge Utilities

This directory contains Python utilities for AI-driven CAD generation and geometry processing.

## Modules

### `cadquery_bridge.py`
Bridge between the Qt GUI and CADQuery for parametric 3D modeling.

**Features:**
- Execute CADQuery scripts
- Generate STEP and STL files
- Validate geometry
- Error handling and logging

**Usage:**
```python
from cadquery_bridge import CADQueryBridge

bridge = CADQueryBridge()
result = bridge.execute_script(cadquery_code)
bridge.export_step(result, "output.step")
bridge.export_stl(result, "output.stl")
```

### `ai_prompts.py`
Prompt templates and engineering for LLM-based CAD generation.

**Features:**
- Pre-defined prompt templates
- Context management
- Few-shot examples
- Parameter extraction

**Usage:**
```python
from ai_prompts import AIPromptManager

manager = AIPromptManager()
prompt = manager.build_cadquery_prompt("Create a cylinder with radius 10mm and height 50mm")
```

### `stl_converter.py`
Utilities for STL/STEP file conversion and mesh processing.

**Features:**
- STEP to STL conversion
- Mesh quality checks
- Mesh repair and optimization
- Volume and surface area calculations

**Usage:**
```python
from stl_converter import STLConverter

converter = STLConverter()
converter.step_to_stl("input.step", "output.stl", resolution=0.1)
stats = converter.analyze_mesh("output.stl")
```

### `config.py`
Configuration management for API keys and settings.

**Features:**
- Environment variable loading
- API key management
- Default settings
- Validation

**Usage:**
```python
from config import get_config

config = get_config()
api_key = config.get_openai_key()
```

## Environment Variables

Create a `.env` file in the `/work` directory with:

```bash
# AI Provider API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Model Selection
DEFAULT_AI_MODEL=gpt-4
TEMPERATURE=0.7

# CADQuery Settings
DEFAULT_RESOLUTION=0.1
STL_LINEAR_DEFLECTION=0.001
STL_ANGULAR_DEFLECTION=0.5
```

## Dependencies

All dependencies are installed via `docker/requirements.txt`.

## Integration with Qt

The Python utilities are called from C++ using `QProcess` to execute Python scripts:

```cpp
QProcess *process = new QProcess();
process->start("python3", QStringList() 
    << "/app/python/cadquery_bridge.py" 
    << "--input" << userInput
    << "--output" << outputPath);
```
