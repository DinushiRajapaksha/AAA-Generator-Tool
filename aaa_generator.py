"""
AAA Generator Tool
Automatically generates AAA (Arrange, Act, Assert) blocks for SAR scripts 
based on IFS documentation.
"""

import re
from typing import Dict, Optional
from jinja2 import Template


class AAAGenerator:
    """
    Generator for AAA (Arrange, Act, Assert) blocks from IFS documentation.
    """
    
    def __init__(self):
        self.template = self._create_template()
    
    def _create_template(self) -> Template:
        """
        Create Jinja2 template for AAA block formatting.
        """
        template_str = """## {{ activity_id }} - {{ activity_name }}

### Description
{{ description }}

### Arrange
{% if arrange %}{{ arrange }}{% else %}*[No prerequisites found - please add manually]*{% endif %}

### Act
{% if act_steps %}{% for step in act_steps %}{{ loop.index }}. {{ step }}
{% endfor %}{% else %}*[No action steps found - please add manually]*
{% endif %}
### Assert
{% if assert_section %}{{ assert_section }}{% else %}*[No system effects found - please add manually]*{% endif %}
"""
        return Template(template_str)
    
    def extract_section(self, documentation: str, section_name: str) -> Optional[str]:
        """
        Extract a specific section from IFS documentation.
        
        Args:
            documentation: Full documentation text
            section_name: Name of section to extract (e.g., "Explanation", "Prerequisites")
        
        Returns:
            Extracted section text or None if not found
        """
        # Pattern to match section headers and their content
        # Handles various formats: "Section Name:", "Section Name\n", "**Section Name**"
        patterns = [
            rf"{section_name}\s*:?\s*\n(.*?)(?=\n\s*(?:[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s*:|\Z))",
            rf"\*\*{section_name}\*\*\s*:?\s*\n(.*?)(?=\n\s*\*\*[A-Z]|\Z)",
            rf"#{1,3}\s*{section_name}\s*\n(.*?)(?=\n\s*#{1,3}\s*[A-Z]|\Z)"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, documentation, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                return content if content else None
        
        return None
    
    def extract_description(self, explanation: str) -> str:
        """
        Extract description from Explanation section (first sentence).
        
        Args:
            explanation: Explanation section text
        
        Returns:
            First sentence as description
        """
        if not explanation:
            return "*[No description found]*"
        
        # Extract first sentence
        match = re.match(r'^(.*?[.!?])\s', explanation)
        if match:
            return match.group(1).strip()
        
        # If no sentence ending found, take first line or up to 150 chars
        first_line = explanation.split('\n')[0]
        if len(first_line) > 150:
            return first_line[:147] + "..."
        return first_line
    
    def extract_act_steps(self, explanation: str) -> list:
        """
        Extract action steps from Explanation section.
        Looks for numbered lists, bullet points, or sentences.
        
        Args:
            explanation: Explanation section text
        
        Returns:
            List of action steps
        """
        if not explanation:
            return []
        
        steps = []
        
        # Try to find numbered lists first (1. , 2. , etc.)
        numbered_pattern = r'^\s*\d+\.\s+(.+?)(?=\n\s*\d+\.|\Z)'
        numbered_matches = re.findall(numbered_pattern, explanation, re.MULTILINE | re.DOTALL)
        if numbered_matches:
            steps = [step.strip().replace('\n', ' ') for step in numbered_matches]
            return steps
        
        # Try to find bullet points (-, *, •)
        bullet_pattern = r'^\s*[-*•]\s+(.+?)(?=\n\s*[-*•]|\Z)'
        bullet_matches = re.findall(bullet_pattern, explanation, re.MULTILINE | re.DOTALL)
        if bullet_matches:
            steps = [step.strip().replace('\n', ' ') for step in bullet_matches]
            return steps
        
        # Fall back to splitting by sentences
        sentences = re.split(r'[.!?]\s+', explanation)
        steps = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
        
        return steps[:10]  # Limit to 10 steps to avoid too many
    
    def format_arrange_section(self, prerequisites: str) -> str:
        """
        Format the Arrange section with test data structure.
        
        Args:
            prerequisites: Prerequisites text
        
        Returns:
            Formatted Arrange section
        """
        if not prerequisites:
            return ""
        
        # Check if it already has structure
        if "Existing test data:" in prerequisites or "Non-existing test data:" in prerequisites:
            return prerequisites
        
        # Format with standard structure
        formatted = f"""Existing test data:
- *[To be determined]*

Non-existing test data:
- {prerequisites}"""
        
        return formatted
    
    def format_assert_section(self, system_effects: str) -> str:
        """
        Format the Assert section as verification checks.
        
        Args:
            system_effects: System Effects text
        
        Returns:
            Formatted Assert section
        """
        if not system_effects:
            return ""
        
        # If it starts with "Check", keep as is
        if system_effects.lower().startswith("check"):
            return system_effects
        
        # Otherwise, prepend "Check if"
        return f"Check if {system_effects[0].lower()}{system_effects[1:]}"
    
    def generate(self, activity_id: str, activity_name: str, documentation: str) -> str:
        """
        Generate AAA block from IFS documentation.
        
        Args:
            activity_id: Activity Diagram ID (e.g., "2.11.1.1")
            activity_name: Activity Name
            documentation: Full documentation text
        
        Returns:
            Formatted AAA block in Markdown
        """
        # Extract sections
        explanation = self.extract_section(documentation, "Explanation")
        prerequisites = self.extract_section(documentation, "Prerequisites")
        system_effects = self.extract_section(documentation, "System Effects")
        
        # Process extracted sections
        description = self.extract_description(explanation) if explanation else "*[No description found]*"
        act_steps = self.extract_act_steps(explanation) if explanation else []
        arrange = self.format_arrange_section(prerequisites) if prerequisites else ""
        assert_section = self.format_assert_section(system_effects) if system_effects else ""
        
        # Generate using template
        result = self.template.render(
            activity_id=activity_id,
            activity_name=activity_name,
            description=description,
            arrange=arrange,
            act_steps=act_steps,
            assert_section=assert_section
        )
        
        return result


def get_user_input() -> Dict[str, str]:
    """
    Get input from user interactively.
    
    Returns:
        Dictionary with activity_id, activity_name, and documentation
    """
    print("=" * 60)
    print("AAA Generator Tool for SAR Scripts")
    print("=" * 60)
    print()
    
    activity_id = input("Enter Activity Diagram ID (e.g., 2.11.1.1): ").strip()
    activity_name = input("Enter Activity Name: ").strip()
    
    print("\nEnter IFS Documentation (paste text, then press Enter and type 'END' on a new line):")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    
    documentation = '\n'.join(lines)
    
    return {
        'activity_id': activity_id,
        'activity_name': activity_name,
        'documentation': documentation
    }


def main():
    """
    Main entry point for the AAA generator tool.
    """
    generator = AAAGenerator()
    
    # Get input from user
    user_input = get_user_input()
    
    # Generate AAA block
    print("\n" + "=" * 60)
    print("Generated AAA Block:")
    print("=" * 60)
    print()
    
    result = generator.generate(
        activity_id=user_input['activity_id'],
        activity_name=user_input['activity_name'],
        documentation=user_input['documentation']
    )
    
    print(result)
    
    # Optionally save to file
    save = input("\nSave to file? (y/n): ").strip().lower()
    if save == 'y':
        filename = f"aaa_{user_input['activity_id'].replace('.', '_')}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Saved to {filename}")


if __name__ == "__main__":
    main()
