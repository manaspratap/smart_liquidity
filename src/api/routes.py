from flask import Blueprint, request, jsonify
from ..engine.liquidity_engine import SmartLiquidityEngine

# Create blueprint
api = Blueprint('api', __name__)

@api.route('/optimize-liquidation', methods=['POST'])
def optimize_liquidation_api():
    """
    API endpoint for optimizing asset liquidation
    Expected JSON input format:
    {
        "portfolio": {
            "mutual_funds": {
                "member": {
                    "mf_name": net_worth  // Net worth of the MF in rupees
                }
            },
            "stocks": {
                "member": {
                    "stock_id": quantity
                }
            },
            "bank_balances": {
                "member": amount
            }
        },
        "questionnaire": {
            "purpose": "emergency|planned_purchase|loan_repayment|other",
            "timeline": "today|2-3_days|within_week|1-4_weeks|no_timeline",
            "amount_needed": float,
            "recurring_need": "one_time|recurring",
            "has_goals": "yes|no",
            "income_change": "no_change|will_reduce|will_increase",
            "priority_members": ["member_ids"]
        }
    }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        if not data:
            return jsonify({
                'status': 'ERROR',
                'message': 'No JSON data provided'
            }), 400
            
        # Create engine instance and process input
        engine = SmartLiquidityEngine()
        result = engine.process_user_input(data)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'status': 'ERROR',
            'message': f'Error processing request: {str(e)}'
        }), 500 