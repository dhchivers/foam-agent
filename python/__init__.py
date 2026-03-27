"""
FoamAgent Python CAD Bridge Utilities

This package provides utilities for AI-driven CAD generation,
geometry processing, and integration with CADQuery.
"""

__version__ = "1.0.0"
__author__ = "FoamAgent Development Team"

from .cadquery_bridge import CADQueryBridge
from .ai_prompts import AIPromptManager
from .stl_converter import STLConverter
from .config import get_config, Config

__all__ = [
    "CADQueryBridge",
    "AIPromptManager",
    "STLConverter",
    "get_config",
    "Config",
]
