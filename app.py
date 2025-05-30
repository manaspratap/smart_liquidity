import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import random
from flask import Flask, request, jsonify

class Purpose(Enum):
    EMERGENCY = "emergency"
    PLANNED_PURCHASE = "planned_purchase"
    LOAN_REPAYMENT = "loan_repayment"
    OTHER = "other"

class Timeline(Enum):
    IMMEDIATE = "immediate"
    WITHIN_WEEK = "within_week"
    ONE_TO_FOUR_WEEKS = "1-4_weeks"
    NO_URGENCY = "no_urgency"

class SEBIRiskCategory(Enum):
    LOW = "low"
    MODERATELY_LOW = "moderately_low"
    MODERATE = "moderate"
    MODERATELY_HIGH = "moderately_high"
    HIGH = "high"
    VERY_HIGH = "very_high"

@dataclass
class StockMetrics:
    """Metrics for evaluating stocks"""
    pe_ratio: float = 25.0  # P/E Ratio
    rsi_14d: float = 50.0  # RSI 14-day
    pledged_promoter_holdings: float = 0.0  # Pledged promoter holdings percentage
    promoter_holding: float = 50.0  # Promoter holding percentage
    beta: float = 1.0  # Beta
    six_month_return_vs_nifty: float = 0.0  # 6M Return vs Nifty
    five_year_cagr: float = 12.0  # 5Y CAGR
    debt_to_equity: float = 0.5  # Debt to Equity ratio
    roce: float = 15.0  # Return on Capital Employed
    return_on_equity: float = 15.0  # Return on Equity
    dividend_yield: float = 2.0  # Dividend Yield
    free_cash_flow: float = 1000.0  # Free Cash Flow (in crores)
    months_held: int = 12  # Months asset has been held
    is_goal_linked: bool = False  # Whether asset is linked to financial goals

@dataclass
class MFMetrics:
    """Metrics for evaluating mutual funds"""
    cagr_3y: float = 12.0  # 3Y CAGR
    expense_ratio: float = 1.5  # Expense ratio
    volatility: float = 15.0  # Volatility percentage
    sharpe_ratio: float = 1.0  # Sharpe Ratio
    alpha: float = 0.0  # Alpha
    sortino_ratio: float = 1.2  # Sortino Ratio
    tracking_error: float = 3.0  # Tracking Error
    time_since_inception: int = 60  # Time since inception in months
    sebi_risk_category: SEBIRiskCategory = SEBIRiskCategory.MODERATE  # SEBI Risk Category
    months_held: int = 12  # Months asset has been held
    is_goal_linked: bool = False  # Whether asset is linked to financial goals

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

class SmartLiquidityEngine:
    def __init__(self):
        # Sample asset metrics database (in real scenario, this would come from API/database)
        self.stock_metrics = {}
        self.mf_metrics = {}
        self.tax_slab_exhausted = {}  # Track tax slab usage by family member
        
    def initialize_sample_data(self):
        """Initialize sample asset metrics for demonstration"""
        # Sample stock metrics
        stock_samples = ["RELIANCE", "TCS", "HDFC", "INFY", "ITC", "WIPRO", "BAJFINANCE", "HCLTECH"]
        for stock in stock_samples:
            self.stock_metrics[stock] = StockMetrics(
                pe_ratio=random.uniform(10, 50),
                rsi_14d=random.uniform(20, 80),
                pledged_promoter_holdings=random.uniform(0, 30),
                promoter_holding=random.uniform(30, 80),
                beta=random.uniform(0.3, 2.5),
                six_month_return_vs_nifty=random.uniform(-25, 35),
                five_year_cagr=random.uniform(5, 30),
                debt_to_equity=random.uniform(0, 2.0),
                roce=random.uniform(5, 30),
                return_on_equity=random.uniform(5, 35),
                dividend_yield=random.uniform(0, 8),
                free_cash_flow=random.uniform(-500, 5000),
                months_held=random.randint(6, 36),
                is_goal_linked=random.choice([True, False])
            )
        
        # Sample MF metrics
        mf_samples = ["HDFC_FLEXICAP", "AXIS_BLUECHIP", "SBI_SMALLCAP", "ICICI_BALANCED", "HDFC_DEBT"]
        for mf in mf_samples:
            self.mf_metrics[mf] = MFMetrics(
                cagr_3y=random.uniform(6, 20),
                expense_ratio=random.uniform(0.5, 2.5),
                volatility=random.uniform(8, 25),
                sharpe_ratio=random.uniform(0.2, 2.0),
                alpha=random.uniform(-5, 8),
                sortino_ratio=random.uniform(0.5, 2.5),
                tracking_error=random.uniform(1, 8),
                time_since_inception=random.randint(12, 180),
                sebi_risk_category=random.choice(list(SEBIRiskCategory)),
                months_held=random.randint(6, 36),
                is_goal_linked=random.choice([True, False])
            )

    def calculate_total_aum(self, mf_map: Dict, stock_map: Dict, bank_balances: Dict) -> float:
        """Calculate total Assets Under Management"""
        # In real scenario, this would fetch actual values from portfolio
        # For demo, assuming average values
        total_aum = 0
        for member, stocks in stock_map.items():
            total_aum += len(stocks) * 50000  # Assuming avg 50k per stock
        for member, mfs in mf_map.items():
            total_aum += len(mfs) * 100000  # Assuming avg 1L per MF
        for member, balance in bank_balances.items():
            total_aum += balance
        return total_aum

    def get_target_bank_percentage(self, purpose: Purpose, timeline: Timeline) -> float:
        """Determine target bank balance percentage of total AUM"""
        if purpose == Purpose.EMERGENCY:
            if timeline == Timeline.IMMEDIATE or timeline == Timeline.WITHIN_WEEK:
                return 0.05  # Keep only 5% in bank
            elif timeline == Timeline.ONE_TO_FOUR_WEEKS:
                return 0.03  # Keep only 3% in bank (more aggressive)
        elif purpose == Purpose.PLANNED_PURCHASE:
            if timeline == Timeline.NO_URGENCY:
                return 0.05  # Keep 5% in bank
            else:  # Large or urgent
                return 0.02  # Keep only 2% in bank
        elif purpose == Purpose.LOAN_REPAYMENT:
            return 0.05  # Keep 5% in bank
        else:  # Other
            return 0.02  # Keep only 2% in bank
        
        return 0.05  # Default to 5%

    def score_stock_for_sale(self, stock_id: str, purpose: Purpose, 
                           timeline: Timeline) -> float:
        """Score a stock for sale priority (higher score = sell first)"""
        if stock_id not in self.stock_metrics:
            return 0.0
            
        metrics = self.stock_metrics[stock_id]
        score = 0.0
        
        # High priority sell indicators based on new parameters
        if metrics.pe_ratio > 40:  # Overvalued
            score += 25
        if metrics.rsi_14d > 70:  # Overbought
            score += 30
        if metrics.pledged_promoter_holdings > 20:  # High pledged holdings
            score += 30
        if metrics.promoter_holding < 40:  # Low promoter holding
            score += 20
        if metrics.beta > 1.8:  # High volatility
            score += 15
        if metrics.six_month_return_vs_nifty < -15:  # Poor recent performance
            score += 25
        if metrics.five_year_cagr < 8:  # Poor long-term performance
            score += 20
        if metrics.debt_to_equity > 1.5:  # High debt
            score += 15
        if metrics.roce < 10:  # Poor capital efficiency
            score += 15
        if metrics.return_on_equity < 10:  # Poor equity returns
            score += 15
        if metrics.free_cash_flow < 0:  # Negative cash flow
            score += 20
        
        # Purpose-specific scoring
        if purpose == Purpose.EMERGENCY:
            if metrics.beta > 1.5:  # Sell high-risk assets first
                score += 25
            if metrics.dividend_yield < 1:  # Prefer to keep dividend-paying stocks
                score += 10
        elif purpose == Purpose.PLANNED_PURCHASE:
            if metrics.five_year_cagr < 12:  # Sell low long-term performers
                score += 20
        
        # Goal-linked assets should be avoided
        if metrics.is_goal_linked:
            score -= 50
            
        # High dividend yield assets (for income generation)
        if metrics.dividend_yield > 4:
            score -= 15
            
        # Near LTCG assets (11-12 months) for tax efficiency
        if 11 <= metrics.months_held <= 12:
            score += 10
            
        return max(0, score)

    def score_mf_for_sale(self, mf_id: str, purpose: Purpose, 
                         timeline: Timeline) -> float:
        """Score a mutual fund for sale priority (higher score = sell first)"""
        if mf_id not in self.mf_metrics:
            return 0.0
            
        metrics = self.mf_metrics[mf_id]
        score = 0.0
        
        # High priority sell indicators for MFs based on new parameters
        if metrics.cagr_3y < 10:  # Poor 3Y performance
            score += 25
        if metrics.expense_ratio > 2.0:  # High expense ratio
            score += 20
        if metrics.volatility > 20:  # High volatility
            score += 15
        if metrics.sharpe_ratio < 0.5:  # Poor risk-adjusted returns
            score += 20
        if metrics.alpha < -2:  # Negative alpha (underperforming benchmark)
            score += 25
        if metrics.sortino_ratio < 0.8:  # Poor downside risk management
            score += 15
        if metrics.tracking_error > 6:  # High tracking error
            score += 15
        if metrics.time_since_inception < 24:  # Very new fund
            score += 10
        
        # SEBI Risk Category scoring
        risk_scores = {
            SEBIRiskCategory.VERY_HIGH: 20,
            SEBIRiskCategory.HIGH: 15,
            SEBIRiskCategory.MODERATELY_HIGH: 10,
            SEBIRiskCategory.MODERATE: 5,
            SEBIRiskCategory.MODERATELY_LOW: 0,
            SEBIRiskCategory.LOW: -5
        }
        score += risk_scores.get(metrics.sebi_risk_category, 0)
        
        # Purpose-specific scoring
        if purpose == Purpose.EMERGENCY:
            if metrics.sebi_risk_category in [SEBIRiskCategory.HIGH, SEBIRiskCategory.VERY_HIGH]:
                score += 25  # Sell high-risk funds first
            if metrics.volatility > 15:
                score += 20
        elif purpose == Purpose.PLANNED_PURCHASE:
            if metrics.cagr_3y < 12:  # Sell underperformers
                score += 15
        
        # Goal-linked funds should be avoided
        if metrics.is_goal_linked:
            score -= 50
            
        return max(0, score)

    def identify_poor_performers(self, mf_map: Dict, stock_map: Dict) -> Tuple[Dict, float]:
        """Identify additional poor performing assets for reinvestment suggestions"""
        poor_assets = {}
        total_poor_value = 0
        
        # Check stocks for poor performance
        for member, stocks in stock_map.items():
            poor_assets[member] = []
            for stock in stocks:
                if stock in self.stock_metrics:
                    metrics = self.stock_metrics[stock]
                    score = self.score_stock_for_sale(stock, Purpose.OTHER, Timeline.NO_URGENCY)
                    
                    # Consider it poor if score is high (but not goal-linked)
                    if score > 35 and not metrics.is_goal_linked:
                        poor_assets[member].append({
                            'asset_id': stock,
                            'type': 'stock',
                            'estimated_value': 50000,  # Sample value
                            'issues': self._get_stock_sell_reason(stock, score),
                            'recommendation': 'Consider switching to fundamentally stronger stocks'
                        })
                        total_poor_value += 50000
        
        # Check MFs for poor performance
        for member, mfs in mf_map.items():
            if member not in poor_assets:
                poor_assets[member] = []
            for mf in mfs:
                if mf in self.mf_metrics:
                    metrics = self.mf_metrics[mf]
                    score = self.score_mf_for_sale(mf, Purpose.OTHER, Timeline.NO_URGENCY)
                    
                    # Consider it poor if score is high (but not goal-linked)
                    if score > 30 and not metrics.is_goal_linked:
                        poor_assets[member].append({
                            'asset_id': mf,
                            'type': 'mf',
                            'estimated_value': 100000,  # Sample value
                            'issues': self._get_mf_sell_reason(mf, score),
                            'recommendation': 'Consider switching to better performing funds with lower costs'
                        })
                        total_poor_value += 100000
        
        return poor_assets, total_poor_value

    def optimize_liquidation(self, mf_map: Dict, stock_map: Dict, 
                           bank_balances: Dict, question_answers: Dict) -> Dict:
        """
        Main function to optimize asset liquidation based on decision tree
        
        Inputs:
        - mf_map: {family_member: [mf_ids]}
        - stock_map: {family_member: [stock_ids]}
        - bank_balances: {family_member: float}
        - question_answers: dict with user responses
        
        Returns:
        - dict: {family_member: [{asset_id: percentage_to_sell}]} or error message
        """
        
        # Initialize sample data for demonstration
        self.initialize_sample_data()
        
        # Parse user inputs
        purpose = Purpose(question_answers.get('purpose', 'other'))
        timeline_map = {
            'today': Timeline.IMMEDIATE,
            '2-3_days': Timeline.IMMEDIATE,
            'within_week': Timeline.WITHIN_WEEK,
            '1-4_weeks': Timeline.ONE_TO_FOUR_WEEKS,
            'no_timeline': Timeline.NO_URGENCY
        }
        timeline = timeline_map.get(question_answers.get('timeline', 'no_timeline'), Timeline.NO_URGENCY)
        amount_needed = float(question_answers.get('amount_needed', 0))
        recurring_need = question_answers.get('recurring_need', 'one_time') != 'one_time'
        has_goals = question_answers.get('has_goals', 'no') == 'yes'
        income_change = question_answers.get('income_change', 'no_change')
        priority_members = question_answers.get('priority_members', [])
        
        # Calculate total AUM
        total_aum = self.calculate_total_aum(mf_map, stock_map, bank_balances)
        
        # CHECK 1: If liquidation amount is > 80% of net worth, reject
        liquidation_percentage = (amount_needed / total_aum) * 100
        if liquidation_percentage > 80:
            return {
                'status': 'REJECTED',
                'message': f'Cannot process liquidation request. You are asking to liquidate {liquidation_percentage:.1f}% of your total net worth (₹{amount_needed:,.0f} out of ₹{total_aum:,.0f}). This would severely impact your financial stability.',
                'recommendation': 'Consider alternative funding sources like loans, or reduce the required amount.',
                'max_safe_liquidation': f'₹{total_aum * 0.8:,.0f} (80% of net worth)'
            }
        
        liquidation_plan = {}
        remaining_amount = amount_needed
        
        # Step 1: Calculate bank balance optimization
        target_bank_percentage = self.get_target_bank_percentage(purpose, timeline)
        target_bank_balance = total_aum * target_bank_percentage
        total_bank_balance = sum(bank_balances.values())
        
        # Calculate how much to liquidate from bank (sell until it's only target% of AUM)
        bank_liquidation_amount = max(0, total_bank_balance - target_bank_balance)
        bank_liquidation_amount = min(bank_liquidation_amount, remaining_amount)
        
        if bank_liquidation_amount > 0:
            # Distribute bank liquidation proportionally
            for member, balance in bank_balances.items():
                if balance > 0 and bank_liquidation_amount > 0:
                    member_liquidation = min(balance, (balance/total_bank_balance) * bank_liquidation_amount)
                    if member not in liquidation_plan:
                        liquidation_plan[member] = []
                    liquidation_plan[member].append({
                        f"BANK_{member}": {
                            'amount_to_liquidate': round(member_liquidation, 2),
                            'reason': f'Optimizing bank balance to {target_bank_percentage*100:.0f}% of total AUM',
                            'remaining_bank_balance': round(balance - member_liquidation, 2)
                        }
                    })
                    remaining_amount -= member_liquidation
                    bank_liquidation_amount -= member_liquidation
        
        # Step 2: If more money needed, sell assets
        if remaining_amount > 0:
            # Create list of all assets with scores
            all_assets = []
            
            # Score all stocks
            for member, stocks in stock_map.items():
                # Skip if member should be prioritized to retain
                if member in priority_members:
                    continue
                    
                for stock in stocks:
                    score = self.score_stock_for_sale(stock, purpose, timeline)
                    all_assets.append({
                        'member': member,
                        'asset_id': stock,
                        'type': 'stock',
                        'score': score,
                        'estimated_value': 50000  # Sample value
                    })
            
            # Score all MFs
            for member, mfs in mf_map.items():
                # Skip if member should be prioritized to retain
                if member in priority_members:
                    continue
                    
                for mf in mfs:
                    score = self.score_mf_for_sale(mf, purpose, timeline)
                    all_assets.append({
                        'member': member,
                        'asset_id': mf,
                        'type': 'mf',
                        'score': score,
                        'estimated_value': 100000  # Sample value
                    })
            
            # Sort by score (highest first - most suitable to sell)
            all_assets.sort(key=lambda x: x['score'], reverse=True)
            
            # Select assets to sell
            for asset in all_assets:
                if remaining_amount <= 0:
                    break
                    
                member = asset['member']
                asset_id = asset['asset_id']
                estimated_value = asset['estimated_value']
                
                # Calculate percentage to sell
                if remaining_amount >= estimated_value:
                    percentage_to_sell = 100.0
                    amount_from_asset = estimated_value
                else:
                    percentage_to_sell = (remaining_amount / estimated_value) * 100
                    amount_from_asset = remaining_amount
                
                # Add to liquidation plan
                if member not in liquidation_plan:
                    liquidation_plan[member] = []
                
                if asset['type'] == 'stock':
                    reason = self._get_stock_sell_reason(asset_id, asset['score'])
                else:
                    reason = self._get_mf_sell_reason(asset_id, asset['score'])
                
                liquidation_plan[member].append({
                    asset_id: {
                        'percentage_to_sell': round(percentage_to_sell, 2),
                        'estimated_amount': round(amount_from_asset, 2),
                        'reason': reason
                    }
                })
                
                remaining_amount -= amount_from_asset
        
        # Step 3: Identify additional poor performers for reinvestment suggestions
        poor_assets, total_poor_value = self.identify_poor_performers(mf_map, stock_map)
        
        # Add summary and recommendations
        liquidation_plan['status'] = 'SUCCESS'
        liquidation_plan['primary_liquidation'] = {
            'total_amount_needed': amount_needed,
            'total_aum': round(total_aum, 2),
            'liquidation_percentage': round(liquidation_percentage, 2),
            'bank_optimization': {
                'current_bank_balance': round(total_bank_balance, 2),
                'target_bank_balance': round(target_bank_balance, 2),
                'bank_liquidation_amount': round(total_bank_balance - target_bank_balance, 2) if total_bank_balance > target_bank_balance else 0
            },
            'assets_liquidated': round(amount_needed - max(0, remaining_amount), 2),
            'shortfall': round(max(0, remaining_amount), 2)
        }
        
        # Business opportunity - suggest additional poor performers to optimize
        liquidation_plan['additional_optimization_opportunity'] = {
            'message': f'Beyond your immediate need of ₹{amount_needed:,.0f}, we identified ₹{total_poor_value:,.0f} worth of underperforming assets that you should consider optimizing.',
            'total_poor_assets_value': round(total_poor_value, 2),
            'poor_assets_by_member': poor_assets,
            'business_pitch': 'Let us help you reinvest these underperforming assets into better opportunities for higher returns!'
        }
        
        liquidation_plan['recommendations'] = self._generate_recommendations(purpose, timeline, has_goals, income_change, liquidation_percentage)
        
        return liquidation_plan
    
    def _get_stock_sell_reason(self, stock_id: str, score: float) -> str:
        """Generate reason for selling a stock"""
        if stock_id not in self.stock_metrics:
            return "Stock metrics not available"
            
        metrics = self.stock_metrics[stock_id]
        reasons = []
        
        if metrics.pe_ratio > 40:
            reasons.append("Overvalued (PE > 40)")
        if metrics.rsi_14d > 70:
            reasons.append("Overbought (RSI > 70)")
        if metrics.pledged_promoter_holdings > 20:
            reasons.append("High pledged holdings")
        if metrics.promoter_holding < 40:
            reasons.append("Low promoter holding")
        if metrics.six_month_return_vs_nifty < -15:
            reasons.append("Poor recent performance")
        if metrics.five_year_cagr < 8:
            reasons.append("Poor long-term returns")
        if metrics.debt_to_equity > 1.5:
            reasons.append("High debt levels")
        if metrics.roce < 10:
            reasons.append("Low ROCE")
        if metrics.return_on_equity < 10:
            reasons.append("Low ROE")
        if metrics.free_cash_flow < 0:
            reasons.append("Negative free cash flow")
        
        return "; ".join(reasons) if reasons else f"Priority score: {score:.1f}"
    
    def _get_mf_sell_reason(self, mf_id: str, score: float) -> str:
        """Generate reason for selling a mutual fund"""
        if mf_id not in self.mf_metrics:
            return "MF metrics not available"
            
        metrics = self.mf_metrics[mf_id]
        reasons = []
        
        if metrics.cagr_3y < 10:
            reasons.append("Poor 3Y CAGR")
        if metrics.expense_ratio > 2.0:
            reasons.append("High expense ratio")
        if metrics.volatility > 20:
            reasons.append("High volatility")
        if metrics.sharpe_ratio < 0.5:
            reasons.append("Poor Sharpe ratio")
        if metrics.alpha < -2:
            reasons.append("Negative alpha")
        if metrics.sortino_ratio < 0.8:
            reasons.append("Poor Sortino ratio")
        if metrics.tracking_error > 6:
            reasons.append("High tracking error")
        if metrics.sebi_risk_category in [SEBIRiskCategory.HIGH, SEBIRiskCategory.VERY_HIGH]:
            reasons.append(f"High risk ({metrics.sebi_risk_category.value})")
        
        return "; ".join(reasons) if reasons else f"Priority score: {score:.1f}"
    
    def _generate_recommendations(self, purpose: Purpose, timeline: Timeline, 
                                has_goals: bool, income_change: str, liquidation_percentage: float) -> List[str]:
        """Generate additional recommendations"""
        recommendations = []
        
        if liquidation_percentage > 50:
            recommendations.append("⚠️ High liquidation percentage - consider exploring loan options to preserve investments")
        elif liquidation_percentage > 30:
            recommendations.append("⚠️ Moderate liquidation - review if this amount is truly necessary")
        
        if purpose == Purpose.EMERGENCY:
            recommendations.append("💡 Build a larger emergency fund (6-12 months expenses) to avoid future asset liquidation")
            
        if timeline == Timeline.IMMEDIATE:
            recommendations.append("💡 Maintain higher liquid funds for urgent needs")
            
        if has_goals:
            recommendations.append("🎯 Review and rebalance remaining portfolio to stay on track with financial goals")
            
        if income_change == "will_reduce":
            recommendations.append("📈 Consider creating additional passive income sources before income reduction")
            
        recommendations.append("📊 Monitor market conditions for optimal timing of liquidation")
        recommendations.append("🏛️ Consult tax advisor for optimizing capital gains tax")
        recommendations.append("🔄 Plan re-entry strategy for sold positions when market conditions improve")
        
        return recommendations

    def process_user_input(self, combined_json: Dict) -> Dict:
        """
        Main entry point for processing combined user input
        
        Args:
            combined_json: Combined user portfolio and questionnaire data
            
        Returns:
            Optimization result or validation error
        """        
        # Parse input
        try:
            mf_map, stock_map, bank_balances, question_answers = UserDataParser.parse_user_input(combined_json)
        except Exception as e:
            return {
                'status': 'PARSING_ERROR',
                'message': f'Error parsing input data: {str(e)}'
            }
        
        # Run optimization
        return self.optimize_liquidation(mf_map, stock_map, bank_balances, question_answers)

# Create Flask app
app = Flask(__name__)

@app.route('/api/optimize-liquidation', methods=['POST'])
def optimize_liquidation_api():
    """
    API endpoint for optimizing asset liquidation
    Expected JSON input format:
    {
        "portfolio": {
            "mutual_funds": {"member": ["mf_ids"]},
            "stocks": {"member": ["stock_ids"]},
            "bank_balances": {"member": amount}
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

if __name__ == "__main__":
    app.run(debug=True, port=5000, host='0.0.0.0')