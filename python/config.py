#!/usr/bin/env python3
"""
Configuration Manager - Handle API keys and settings

This module manages configuration for AI providers, CADQuery settings,
and other application parameters.
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class Config:
    """
    Configuration manager for FoamAgent Python utilities.
    """
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file (defaults to /work/.env)
        """
        # Default to /work/.env for persistent storage
        if env_file is None:
            env_file = "/work/.env"
        
        self.env_file = env_file
        
        # Load environment variables from .env file if it exists
        if os.path.exists(env_file):
            load_dotenv(env_file)
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load all configuration values."""
        # AI Provider Settings
        self.openai_api_key = os.getenv('OPENAI_API_KEY', '')
        self.anthropic_api_key = os.getenv('ANTHROPIC_API_KEY', '')
        self.default_ai_model = os.getenv('DEFAULT_AI_MODEL', 'gpt-4')
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        
        # CADQuery Settings
        self.default_resolution = float(os.getenv('DEFAULT_RESOLUTION', '0.1'))
        self.stl_linear_deflection = float(os.getenv('STL_LINEAR_DEFLECTION', '0.001'))
        self.stl_angular_deflection = float(os.getenv('STL_ANGULAR_DEFLECTION', '0.5'))
        
        # Working directories
        self.work_dir = os.getenv('WORK_DIR', '/work')
        self.output_dir = os.getenv('OUTPUT_DIR', f'{self.work_dir}/cad_outputs')
        
        # Ensure output directory exists
        Path(self.output_dir).mkdir(parents=True, exist_ok=True)
    
    def get_openai_key(self) -> str:
        """Get OpenAI API key."""
        if not self.openai_api_key:
            raise ValueError(
                "OpenAI API key not found. "
                "Set OPENAI_API_KEY in /work/.env or environment variable."
            )
        return self.openai_api_key
    
    def get_anthropic_key(self) -> str:
        """Get Anthropic API key."""
        if not self.anthropic_api_key:
            raise ValueError(
                "Anthropic API key not found. "
                "Set ANTHROPIC_API_KEY in /work/.env or environment variable."
            )
        return self.anthropic_api_key
    
    def has_openai_key(self) -> bool:
        """Check if OpenAI API key is configured."""
        return bool(self.openai_api_key)
    
    def has_anthropic_key(self) -> bool:
        """Check if Anthropic API key is configured."""
        return bool(self.anthropic_api_key)
    
    def get_ai_provider(self) -> str:
        """
        Determine which AI provider to use based on available keys.
        
        Returns:
            'openai', 'anthropic', or 'none'
        """
        if self.has_openai_key():
            return 'openai'
        elif self.has_anthropic_key():
            return 'anthropic'
        else:
            return 'none'
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Export configuration as dictionary.
        
        Returns:
            Dictionary of configuration values (excluding sensitive keys)
        """
        return {
            'ai': {
                'default_model': self.default_ai_model,
                'temperature': self.temperature,
                'max_tokens': self.max_tokens,
                'has_openai_key': self.has_openai_key(),
                'has_anthropic_key': self.has_anthropic_key(),
                'provider': self.get_ai_provider()
            },
            'cadquery': {
                'default_resolution': self.default_resolution,
                'stl_linear_deflection': self.stl_linear_deflection,
                'stl_angular_deflection': self.stl_angular_deflection
            },
            'paths': {
                'work_dir': self.work_dir,
                'output_dir': self.output_dir,
                'env_file': self.env_file
            }
        }
    
    def create_env_template(self, output_path: Optional[str] = None):
        """
        Create a template .env file with all available settings.
        
        Args:
            output_path: Path to output file (defaults to /work/.env.template)
        """
        if output_path is None:
            output_path = f"{self.work_dir}/.env.template"
        
        template = """# FoamAgent Python Utilities Configuration
# Copy this file to .env and fill in your API keys

# ============================================
# AI Provider API Keys
# ============================================
# OpenAI API Key (for GPT-4, GPT-3.5, etc.)
# Get your key from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-your-key-here

# Anthropic API Key (for Claude models)
# Get your key from: https://console.anthropic.com/
ANTHROPIC_API_KEY=sk-ant-your-key-here

# ============================================
# AI Model Settings
# ============================================
# Default model to use (gpt-4, gpt-3.5-turbo, claude-3-opus-20240229, etc.)
DEFAULT_AI_MODEL=gpt-4

# Temperature for generation (0.0-1.0, higher = more creative)
TEMPERATURE=0.7

# Maximum tokens in response
MAX_TOKENS=2000

# ============================================
# CADQuery Settings
# ============================================
# Default mesh resolution (smaller = finer detail)
DEFAULT_RESOLUTION=0.1

# STL export linear deflection (smaller = smoother curves)
STL_LINEAR_DEFLECTION=0.001

# STL export angular deflection in degrees
STL_ANGULAR_DEFLECTION=0.5

# ============================================
# Directory Settings
# ============================================
# Working directory for cases and outputs
WORK_DIR=/work

# Output directory for CAD files
OUTPUT_DIR=/work/cad_outputs
"""
        
        with open(output_path, 'w') as f:
            f.write(template)
        
        return output_path


# Global configuration instance
_config_instance: Optional[Config] = None


def get_config(env_file: Optional[str] = None, reload: bool = False) -> Config:
    """
    Get the global configuration instance.
    
    Args:
        env_file: Path to .env file (only used on first call or if reload=True)
        reload: Force reload of configuration
        
    Returns:
        Config instance
    """
    global _config_instance
    
    if _config_instance is None or reload:
        _config_instance = Config(env_file)
    
    return _config_instance


def main():
    """Command-line interface for configuration management."""
    import sys
    import json
    
    if len(sys.argv) > 1 and sys.argv[1] == 'create-template':
        config = get_config()
        template_path = config.create_env_template()
        print(f"Created template at: {template_path}")
        print("\nEdit this file and save as .env to configure your API keys.")
    else:
        config = get_config()
        print(json.dumps(config.to_dict(), indent=2))


if __name__ == '__main__':
    main()
