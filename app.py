"""
Flask Web Application for AAA Generator Tool
Provides a web interface for generating AAA blocks
"""

from flask import Flask, render_template, request, jsonify
from aaa_generator import AAAGenerator

app = Flask(__name__)
generator = AAAGenerator()


@app.route('/')
def index():
    """
    Serve the main web interface.
    """
    return render_template('index.html')


@app.route('/generate', methods=['POST'])
def generate():
    """
    API endpoint to generate AAA block from documentation.
    
    Expected JSON payload:
    {
        "activity_id": "2.11.1.1",
        "activity_name": "Enter Credit Analyst User",
        "documentation": "Explanation: ..."
    }
    
    Returns:
    {
        "success": true,
        "result": "## Generated AAA Block..."
    }
    """
    try:
        data = request.get_json()
        
        activity_id = data.get('activity_id', '').strip()
        activity_name = data.get('activity_name', '').strip()
        documentation = data.get('documentation', '').strip()
        
        # Validation
        if not activity_id:
            return jsonify({
                'success': False,
                'error': 'Activity ID is required'
            }), 400
        
        if not activity_name:
            return jsonify({
                'success': False,
                'error': 'Activity Name is required'
            }), 400
        
        if not documentation:
            return jsonify({
                'success': False,
                'error': 'Documentation text is required'
            }), 400
        
        # Generate AAA block
        result = generator.generate(activity_id, activity_name, documentation)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """
    Get example documentation for demo purposes.
    """
    examples = [
        {
            "name": "Credit Analyst User",
            "activity_id": "2.11.1.1",
            "activity_name": "BDR for Customer Credit Information - Enter Credit Analyst User",
            "documentation": """Explanation:
Use this activity to specify the users assigned to a credit analyst position. The credit analyst is responsible for approving or rejecting credit limits for customers. Open the Credit Management Basic Data window. Click the Credit Analyst User tab. Create a new record and enter the user ID and other relevant information. Save the record.

Prerequisites:
A credit analyst must be created.

System Effects:
The entered credit analyst user information is saved in the system and becomes visible for future operations."""
        },
        {
            "name": "Customer Order",
            "activity_id": "3.5.2.1",
            "activity_name": "Customer Order - Enter Customer Order",
            "documentation": """**Explanation**
Enter customer order information using the Customer Order window. This activity allows you to create new customer orders with header information including order date, delivery date, and customer details. The system will validate the customer information and calculate initial prices based on the price list.

**Prerequisites**
The customer must exist in the system.
Valid price lists must be configured.

**System Effects**
A new customer order is created with status 'Planned'.
The order is available for further processing."""
        },
        {
            "name": "Inventory Count",
            "activity_id": "4.12.3.2",
            "activity_name": "Inventory Management - Count Inventory",
            "documentation": """### Explanation
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
Inventory differences are recorded and can be reviewed in the Count Report."""
        }
    ]
    
    return jsonify({
        'success': True,
        'examples': examples
    })


if __name__ == '__main__':
    print("=" * 70)
    print("AAA Generator Tool - Web Interface")
    print("=" * 70)
    print("Starting server at http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 70)
    app.run(debug=True, host='0.0.0.0', port=5000)
