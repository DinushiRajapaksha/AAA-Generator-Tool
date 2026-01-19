"""
Example usage of AAA Generator Tool
Demonstrates how to use the tool with sample IFS documentation
"""

from aaa_generator import AAAGenerator


# Sample IFS Documentation
SAMPLE_DOC_1 = """
Explanation:
Use this activity to specify the users assigned to a credit analyst position. The credit analyst is responsible for approving or rejecting credit limits for customers. Open the Credit Management Basic Data window. Click the Credit Analyst User tab. Create a new record and enter the user ID and other relevant information. Save the record.

Prerequisites:
A credit analyst must be created.

System Effects:
The entered credit analyst user information is saved in the system and becomes visible for future operations.
"""

SAMPLE_DOC_2 = """
**Explanation**
Enter customer order information using the Customer Order window. This activity allows you to create new customer orders with header information including order date, delivery date, and customer details. The system will validate the customer information and calculate initial prices based on the price list.

**Prerequisites**
The customer must exist in the system.
Valid price lists must be configured.

**System Effects**
A new customer order is created with status 'Planned'.
The order is available for further processing.
"""

SAMPLE_DOC_3 = """
### Explanation
This activity enables inventory counting at a specific location.

1. Navigate to the Inventory Part in Stock window.
2. Select the location to count.
3. Click the Count Inventory button.
4. Enter the counted quantity.
5. Confirm the count.

### Prerequisites
- Inventory parts must exist at the location.
- User must have counting permissions.

### System Effects
Inventory differences are recorded and can be reviewed in the Count Report.
"""


def run_example(example_num: int, activity_id: str, activity_name: str, documentation: str):
    """
    Run a single example through the generator.
    """
    print("\n" + "=" * 70)
    print(f"EXAMPLE {example_num}: {activity_id}")
    print("=" * 70)
    
    generator = AAAGenerator()
    result = generator.generate(activity_id, activity_name, documentation)
    
    print(result)
    print("\n")


def main():
    """
    Run all examples to demonstrate the tool.
    """
    print("AAA Generator Tool - Examples")
    print("=" * 70)
    
    # Example 1: Standard format with colon-based sections
    run_example(
        1,
        "2.11.1.1",
        "BDR for Customer Credit Information - Enter Credit Analyst User",
        SAMPLE_DOC_1
    )
    
    # Example 2: Bold markdown sections
    run_example(
        2,
        "3.5.2.1",
        "Customer Order - Enter Customer Order",
        SAMPLE_DOC_2
    )
    
    # Example 3: Header-based sections with numbered steps
    run_example(
        3,
        "4.12.3.2",
        "Inventory Management - Count Inventory",
        SAMPLE_DOC_3
    )
    
    print("=" * 70)
    print("Examples complete! You can now use aaa_generator.py interactively.")
    print("=" * 70)


if __name__ == "__main__":
    main()
