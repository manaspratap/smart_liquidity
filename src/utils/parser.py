from typing import Dict, Tuple

class UserDataParser:
    """Parser for combined user portfolio and questionnaire data"""
    
    @staticmethod
    def parse_user_input(combined_json: Dict) -> Tuple[Dict, Dict, Dict, Dict]:
        """
        Parse combined JSON input into separate components
        
        Args:
            combined_json: Combined user data in JSON format
            
        Returns:
            Tuple of (mf_map, stock_map, bank_balances, question_answers)
        """
        # Extract portfolio data
        portfolio = combined_json.get('portfolio', {})
        mf_map = portfolio.get('mutual_funds', {})
        stock_map = portfolio.get('stocks', {})
        bank_balances = portfolio.get('bank_balances', {})
        
        # Extract questionnaire responses
        questionnaire = combined_json.get('questionnaire', {})
        question_answers = {
            'purpose': questionnaire.get('purpose', 'other'),
            'timeline': questionnaire.get('timeline', 'no_timeline'),
            'amount_needed': float(questionnaire.get('amount_needed', 0)),
            'recurring_need': questionnaire.get('recurring_need', 'one_time'),
            'has_goals': questionnaire.get('has_goals', 'no'),
            'income_change': questionnaire.get('income_change', 'no_change'),
            'priority_members': questionnaire.get('priority_members', [])
        }
        
        return mf_map, stock_map, bank_balances, question_answers 