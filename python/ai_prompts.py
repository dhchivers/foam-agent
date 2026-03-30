#!/usr/bin/env python3
"""
AI Prompt Manager - Templates and utilities for LLM-based CAD generation

This module provides prompt engineering for generating CADQuery code
from natural language descriptions.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class PromptExample:
    """Example input/output pair for few-shot learning."""
    description: str
    cadquery_code: str
    notes: Optional[str] = None


class AIPromptManager:
    """
    Manager for AI prompts and templates for CADQuery generation.
    """
    
    # System prompt for CADQuery generation
    SYSTEM_PROMPT = """You are an expert CAD engineer and Python programmer specializing in CADQuery.
Your task is to generate valid CADQuery Python code from natural language descriptions.

Key requirements:
1. Always assign the final geometry to a variable named 'result'
2. Use proper CADQuery syntax and best practices
3. Include proper units (assume mm unless specified)
4. Generate clean, commented code
5. Handle common geometric operations: boxes, cylinders, spheres, extrusions, cuts, fillets
6. Use parametric design when appropriate

Output only valid Python code that can be executed directly.
Do NOT include markdown code blocks, explanations, or anything except the Python code.
"""

    # Few-shot examples for better generation
    EXAMPLES = [
        PromptExample(
            description="Create a simple cylinder with radius 10mm and height 50mm",
            cadquery_code="""import cadquery as cq

# Simple cylinder
result = cq.Workplane("XY").circle(10).extrude(50)
""",
            notes="Basic cylinder using circle and extrude"
        ),
        PromptExample(
            description="Create a box 20x30x40mm with 2mm fillets on all edges",
            cadquery_code="""import cadquery as cq

# Box with filleted edges
result = (cq.Workplane("XY")
    .box(20, 30, 40)
    .edges()
    .fillet(2)
)
""",
            notes="Box with edge fillets"
        ),
        PromptExample(
            description="Create a hollow cube 50mm on each side with 5mm wall thickness",
            cadquery_code="""import cadquery as cq

# Hollow cube using shell
result = (cq.Workplane("XY")
    .box(50, 50, 50)
    .faces(">Z")
    .shell(-5)
)
""",
            notes="Hollow cube created with shell operation"
        ),
        PromptExample(
            description="Create a 100mm long beam with I-shaped cross section",
            cadquery_code="""import cadquery as cq

# I-beam profile
# Dimensions: 50mm height, 30mm flange width, 5mm web thickness, 8mm flange thickness
result = (cq.Workplane("XY")
    .hLine(15).vLine(8).hLine(-10).vLine(34).hLine(10).vLine(8)
    .hLine(15).vLine(-50).close()
    .extrude(100)
)
""",
            notes="I-beam using polyline and extrude"
        ),
        PromptExample(
            description="Create a simple mounting bracket with holes",
            cadquery_code="""import cadquery as cq

# Mounting bracket
bracket = (cq.Workplane("XY")
    .box(60, 40, 10)
    .faces(">Z")
    .workplane()
    .rarray(40, 20, 2, 2)
    .circle(3)
    .cutThruAll()
    .edges("|Z")
    .fillet(2)
)

result = bracket
""",
            notes="Bracket with bolt holes in rectangular array"
        ),
    ]
    
    def __init__(self, model: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the AI prompt manager.
        
        Args:
            model: AI model to use (gpt-4, claude-3-opus, etc.)
            temperature: Sampling temperature (0-1)
        """
        self.model = model
        self.temperature = temperature
    
    def build_cadquery_prompt(
        self, 
        description: str,
        include_examples: bool = True,
        num_examples: int = 3,
        additional_context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build a complete prompt for CADQuery code generation.
        
        Args:
            description: User's natural language description
            include_examples: Whether to include few-shot examples
            num_examples: Number of examples to include
            additional_context: Additional context or constraints
            
        Returns:
            List of message dictionaries for chat-based APIs
        """
        messages = [
            {"role": "system", "content": self.SYSTEM_PROMPT}
        ]
        
        # Add few-shot examples
        if include_examples and num_examples > 0:
            examples_to_use = self.EXAMPLES[:min(num_examples, len(self.EXAMPLES))]
            for example in examples_to_use:
                messages.append({
                    "role": "user",
                    "content": example.description
                })
                messages.append({
                    "role": "assistant",
                    "content": example.cadquery_code
                })
        
        # Add the actual user request
        user_content = description
        if additional_context:
            user_content = f"{description}\n\nAdditional requirements:\n{additional_context}"
        
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        return messages
    
    def extract_code_from_response(self, response: str) -> str:
        """
        Extract Python code from AI response, removing markdown formatting if present.
        
        Args:
            response: Raw AI response
            
        Returns:
            Cleaned Python code
        """
        # Remove markdown code blocks if present
        code = response.strip()
        
        # Remove ```python or ```
        if code.startswith("```python"):
            code = code[9:]
        elif code.startswith("```"):
            code = code[3:]
        
        if code.endswith("```"):
            code = code[:-3]
        
        return code.strip()
    
    def validate_code_structure(self, code: str) -> Dict[str, any]:
        """
        Validate that generated code has required structure.
        
        Args:
            code: Generated Python code
            
        Returns:
            Dictionary with validation results
        """
        validation = {
            'valid': True,
            'errors': [],
            'warnings': []
        }
        
        # Check for 'result' variable
        if 'result' not in code and 'result=' not in code:
            validation['errors'].append("Code must define a 'result' variable")
            validation['valid'] = False
        
        # Check for CADQuery import
        if 'import cadquery' not in code and 'import cq' not in code:
            validation['warnings'].append("Code should import cadquery")
        
        # Check for Workplane usage
        if 'Workplane' not in code and 'workplane' not in code:
            validation['warnings'].append("Code should use Workplane")
        
        # Basic syntax check
        try:
            compile(code, '<string>', 'exec')
        except SyntaxError as e:
            validation['errors'].append(f"Syntax error: {str(e)}")
            validation['valid'] = False
        
        return validation
    
    def generate_template(self, shape_type: str) -> str:
        """
        Generate a template for common shape types.
        
        Args:
            shape_type: Type of shape (box, cylinder, sphere, etc.)
            
        Returns:
            CADQuery code template
        """
        templates = {
            'box': '''import cadquery as cq

# Box with dimensions {length} x {width} x {height} mm
result = cq.Workplane("XY").box({length}, {width}, {height})
''',
            'cylinder': '''import cadquery as cq

# Cylinder with radius {radius} mm and height {height} mm
result = cq.Workplane("XY").circle({radius}).extrude({height})
''',
            'sphere': '''import cadquery as cq

# Sphere with radius {radius} mm
result = cq.Workplane("XY").sphere({radius})
''',
            'cone': '''import cadquery as cq

# Cone with base radius {base_radius} mm, top radius {top_radius} mm, height {height} mm
result = (cq.Workplane("XY")
    .circle({base_radius})
    .workplane(offset={height})
    .circle({top_radius})
    .loft()
)
''',
        }
        
        return templates.get(shape_type.lower(), templates['box'])
    
    # libfive-specific prompts and methods
    
    LIBFIVE_SYSTEM_PROMPT = """You are an expert in functional representation (F-Rep) 3D modeling using libfive.
Your task is to generate valid libfive Python code from natural language descriptions.

Key requirements:
1. Always assign the final geometry to a variable named 'result' or 'shape'
2. Import necessary functions from libfive.stdlib
3. Use signed distance functions and CSG operations
4. Objects are defined as mathematical functions f(x,y,z)
5. Common operations: sphere, box, cylinder, union, intersection, difference, translate, scale
6. libfive uses functional composition - operations return new functions

Output only valid Python code that can be executed directly.
Do NOT include markdown code blocks, explanations, or anything except the Python code.
"""

    LIBFIVE_EXAMPLES = [
        PromptExample(
            description="Create a sphere with radius 5mm",
            cadquery_code="""from libfive.stdlib import *

# Sphere at origin with radius 5
result = sphere(5, [0, 0, 0])
""",
            notes="Basic sphere using libfive"
        ),
        PromptExample(
            description="Create a box 10x10x10mm",
            cadquery_code="""from libfive.stdlib import *

# Box centered at origin
result = box([-5, -5, -5], [5, 5, 5])
""",
            notes="Box defined by corner points"
        ),
        PromptExample(
            description="Create a cylinder with radius 5mm and height 20mm",
            cadquery_code="""from libfive.stdlib import *

# Cylinder along Z axis
cyl = cylinder(5, -10, 10)
result = cyl
""",
            notes="Cylinder with radius and Z range"
        ),
        PromptExample(
            description="Create a union of a sphere and a box",
            cadquery_code="""from libfive.stdlib import *

# Sphere
s = sphere(5, [0, 0, 0])

# Box
b = box([-3, -3, -3], [3, 3, 3])

# Union them
result = union(s, b)
""",
            notes="CSG union operation"
        ),
        PromptExample(
            description="Create a sphere with a cylindrical hole through it",
            cadquery_code="""from libfive.stdlib import *

# Sphere
s = sphere(10, [0, 0, 0])

# Cylinder for the hole
c = cylinder(3, -15, 15)

# Subtract cylinder from sphere
result = difference(s, c)
""",
            notes="Boolean difference operation"
        ),
    ]
    
    def build_libfive_prompt(
        self,
        description: str,
        include_examples: bool = True,
        num_examples: int = 3,
        additional_context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Build a complete prompt for libfive code generation.
        
        Args:
            description: User's natural language description
            include_examples: Whether to include few-shot examples
            num_examples: Number of examples to include
            additional_context: Additional context or constraints
            
        Returns:
            List of message dictionaries for chat-based APIs
        """
        messages = [
            {"role": "system", "content": self.LIBFIVE_SYSTEM_PROMPT}
        ]
        
        # Add few-shot examples
        if include_examples and num_examples > 0:
            examples_to_use = self.LIBFIVE_EXAMPLES[:min(num_examples, len(self.LIBFIVE_EXAMPLES))]
            for example in examples_to_use:
                messages.append({
                    "role": "user",
                    "content": example.description
                })
                messages.append({
                    "role": "assistant",
                    "content": example.cadquery_code  # Using same field name for consistency
                })
        
        # Add the actual user request
        user_content = description
        if additional_context:
            user_content = f"{description}\n\nAdditional requirements:\n{additional_context}"
        
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        return messages
    
    def generate_libfive_template(self, shape_type: str) -> str:
        """
        Generate a libfive template for common shape types.
        
        Args:
            shape_type: Type of shape (sphere, box, cylinder, etc.)
            
        Returns:
            libfive code template
        """
        templates = {
            'sphere': '''from libfive.stdlib import *

# Sphere with radius {radius} at position [{x}, {y}, {z}]
result = sphere({radius}, [{x}, {y}, {z}])
''',
            'box': '''from libfive.stdlib import *

# Box from corner1 to corner2
result = box([{x1}, {y1}, {z1}], [{x2}, {y2}, {z2}])
''',
            'cylinder': '''from libfive.stdlib import *

# Cylinder with radius {radius} from z={z1} to z={z2}
result = cylinder({radius}, {z1}, {z2})
''',
            'union': '''from libfive.stdlib import *

# Create two shapes
shape1 = sphere({radius1}, [0, 0, 0])
shape2 = box([{x}, {y}, {z}], [{x2}, {y2}, {z2}])

# Union them together
result = union(shape1, shape2)
''',
        }
        
        return templates.get(shape_type.lower(), templates['sphere'])


def main():
    """Example usage of AIPromptManager."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python ai_prompts.py <description>")
        sys.exit(1)
    
    description = " ".join(sys.argv[1:])
    
    manager = AIPromptManager()
    messages = manager.build_cadquery_prompt(description)
    
    print(json.dumps(messages, indent=2))


if __name__ == '__main__':
    main()
