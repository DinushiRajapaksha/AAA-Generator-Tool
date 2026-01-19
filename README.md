# AAA Generator Tool

A Python tool that automatically generates AAA (Arrange, Act, Assert) blocks for SAR scripts based on IFS documentation.

## Overview

This tool parses IFS documentation and extracts key sections to generate structured test case documentation following the AAA pattern:
- **Arrange**: Prerequisites and test data setup
- **Act**: Steps to perform the action
- **Assert**: Expected results and system effects

## Features

✅ **Intelligent Section Extraction**: Automatically extracts Explanation, Prerequisites, and System Effects from various documentation formats
✅ **Multiple Format Support**: Handles different section headers (colons, bold markdown, headers)
✅ **Smart Step Detection**: Recognizes numbered lists, bullet points, or splits text into logical steps
✅ **Clean Markdown Output**: Generates well-formatted AAA blocks ready to use
✅ **Interactive Mode**: User-friendly prompts for input
✅ **File Export**: Save generated AAA blocks to markdown files

## Installation

1. Clone or download this repository
2. Install dependencies:
```powershell
pip install -r requirements.txt
```

## Usage

### Interactive Mode

Run the main script and follow the prompts:

```powershell
python aaa_generator.py
```

You'll be asked to provide:
1. Activity Diagram ID (e.g., "2.11.1.1")
2. Activity Name (e.g., "BDR for Customer Credit Information")
3. IFS Documentation text (paste and type 'END' when finished)

### Example Usage

See examples in action:

```powershell
python example_usage.py
```

This demonstrates the tool with three different documentation formats.

### Programmatic Usage

You can also use the tool in your own Python scripts:

```python
from aaa_generator import AAAGenerator

generator = AAAGenerator()

documentation = """
Explanation:
Use this activity to create a customer order...

Prerequisites:
Customer must exist in the system.

System Effects:
A new customer order is created.
"""

result = generator.generate(
    activity_id="3.5.2.1",
    activity_name="Enter Customer Order",
    documentation=documentation
)

print(result)
```

## Output Format

The tool generates AAA blocks in the following format:

```markdown
## 2.11.1.1 - BDR for Customer Credit Information - Enter Credit Analyst User

### Description
Use this activity to specify the users assigned to a credit analyst position.

### Arrange
Existing test data:
- *[To be determined]*

Non-existing test data:
- A credit analyst must be created.

### Act
1. Open the Credit Management Basic Data window
2. Click the Credit Analyst User tab
3. Create a new record
4. Enter the user ID and other relevant information
5. Save the record

### Assert
Check if the entered credit analyst user information is saved in the system and becomes visible for future operations.
```

## Supported Documentation Formats

The tool can parse various IFS documentation formats:

### Format 1: Colon-based sections
```
Explanation:
Text here...

Prerequisites:
Text here...

System Effects:
Text here...
```

### Format 2: Bold markdown
```
**Explanation**
Text here...

**Prerequisites**
Text here...

**System Effects**
Text here...
```

### Format 3: Markdown headers
```
### Explanation
Text here...

### Prerequisites
Text here...

### System Effects
Text here...
```

## Future Enhancements

🔮 Planned features:
- [ ] Confluence API integration to fetch documentation automatically
- [ ] NLP-based extraction using spaCy for better accuracy
- [ ] CLI tool with command-line arguments
- [ ] Batch processing for multiple activities
- [ ] Custom template support
- [ ] Export to different formats (JSON, CSV, etc.)

## Project Structure

```
aaa_generator_tool/
├── aaa_generator.py      # Main generator script
├── example_usage.py      # Example demonstrations
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Requirements

- Python 3.7+
- Jinja2 3.1.0+

## License

This tool is provided as-is for internal use.

## Contributing

To improve the tool:
1. Add more regex patterns for different documentation formats
2. Enhance step extraction logic
3. Add more test examples
4. Implement additional output formats

---

**Created for**: SAR Script Documentation Automation
**Version**: 1.0.0
**Last Updated**: November 24, 2025
