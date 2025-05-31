import os
import random
import pandas as pd
from typing import Dict, List, Tuple
from ..models.enums import Purpose, Timeline, SEBIRiskCategory
from ..models.metrics import StockMetrics, MFMetrics
from ..utils.parser import UserDataParser

class SmartLiquidityEngine:
    def __init__(self):
        self.stock_metrics = {}
        self.mf_metrics = {}
        self.stock_prices = {}
        self.tax_slab_exhausted = {}

    def initialize_sample_data(self):
        """Initialize asset metrics from CSV files"""
        try:
            current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            stock_csv_path = os.path.join(current_dir, 'assets', 'Stock_Screener.csv')
            mf_csv_path = os.path.join(current_dir, 'assets', 'Mutual_Fund_Screener.csv')
            
            self._load_stock_data(stock_csv_path)
            self._load_mf_data(mf_csv_path)
                
        except Exception as e:
            print(f"Error initializing data: {str(e)}")
            self._initialize_sample_stock_data()
            self._initialize_sample_mf_data()

    def _load_stock_data(self, stock_csv_path: str):
        """Load stock data from CSV"""
        if os.path.exists(stock_csv_path):
            df = pd.read_csv(
                stock_csv_path,
                encoding='utf-8',
                on_bad_lines='warn',
                quoting=1,
                skipinitialspace=True
            )
            
            # Store stock prices
            for _, row in df.iterrows():
                ticker = row['Ticker']
                if pd.notna(ticker) and pd.notna(row['Close Price']):
                    self.stock_prices[ticker] = float(row['Close Price'])
            
            # Process each stock
            for _, row in df.iterrows():
                try:
                    ticker = row['Ticker']
                    if pd.isna(ticker):
                        continue
                        
                    self.stock_metrics[ticker] = StockMetrics(
                        pe_ratio=float(row['PE Ratio']) if pd.notna(row['PE Ratio']) else 25.0,
                        rsi_14d=float(row['RSI – 14D']) if pd.notna(row['RSI – 14D']) else 50.0,
                        pledged_promoter_holdings=float(row['Pledged Promoter Holdings']) if pd.notna(row['Pledged Promoter Holdings']) else 0.0,
                        promoter_holding=float(row['Promoter Holding']) if pd.notna(row['Promoter Holding']) else 50.0,
                        beta=float(row['Beta']) if pd.notna(row['Beta']) else 1.0,
                        six_month_return_vs_nifty=float(row['6M Return vs Nifty']) if pd.notna(row['6M Return vs Nifty']) else 0.0,
                        five_year_cagr=float(row['5Y CAGR']) if pd.notna(row['5Y CAGR']) else 12.0,
                        debt_to_equity=float(row['Debt to Equity']) if pd.notna(row['Debt to Equity']) else 0.5,
                        roce=float(row['ROCE']) if pd.notna(row['ROCE']) else 15.0,
                        return_on_equity=float(row['Return on Equity']) if pd.notna(row['Return on Equity']) else 15.0,
                        dividend_yield=float(row['Dividend Yield']) if pd.notna(row['Dividend Yield']) else 2.0,
                        free_cash_flow=float(row['Free Cash Flow']) if pd.notna(row['Free Cash Flow']) else 1000.0,
                        months_held=random.randint(6, 36),
                        is_goal_linked=random.choice([True, False])
                    )
                except Exception as e:
                    print(f"Error processing stock row for ticker {ticker}: {str(e)}")
                    continue
        else:
            print(f"Warning: Stock screener CSV not found at {stock_csv_path}")
            self._initialize_sample_stock_data()

    def _load_mf_data(self, mf_csv_path: str):
        """Load mutual fund data from CSV"""
        if os.path.exists(mf_csv_path):
            mf_df = pd.read_csv(
                mf_csv_path,
                encoding='utf-8',
                on_bad_lines='warn',
                quoting=1,
                skipinitialspace=True
            )
            
            # Process each MF
            for _, row in mf_df.iterrows():
                try:
                    mf_name = row['Name']
                    if pd.isna(mf_name):
                        continue
                        
                    # Convert time since inception to months
                    time_since_inception = row['Time since inception']
                    months = 0
                    if isinstance(time_since_inception, str):
                        if 'year' in time_since_inception.lower():
                            years = float(time_since_inception.split()[0])
                            months = int(years * 12)
                        elif 'month' in time_since_inception.lower():
                            months = int(time_since_inception.split()[0])
                    
                    # Map SEBI risk category
                    sebi_risk = row['SEBI Risk Category']
                    sebi_risk_category = SEBIRiskCategory.MODERATE  # default
                    if isinstance(sebi_risk, str):
                        sebi_risk = sebi_risk.lower().strip()
                        if 'very high' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.VERY_HIGH
                        elif 'high' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.HIGH
                        elif 'moderately high' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.MODERATELY_HIGH
                        elif 'moderate' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.MODERATE
                        elif 'moderately low' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.MODERATELY_LOW
                        elif 'low' in sebi_risk:
                            sebi_risk_category = SEBIRiskCategory.LOW
                    
                    self.mf_metrics[mf_name] = MFMetrics(
                        cagr_3y=float(row['CAGR 3Y']) if pd.notna(row['CAGR 3Y']) else 12.0,
                        expense_ratio=float(row['Expense Ratio']) if pd.notna(row['Expense Ratio']) else 1.5,
                        volatility=float(row['Volatility']) if pd.notna(row['Volatility']) else 15.0,
                        sharpe_ratio=float(row['Sharpe Ratio']) if pd.notna(row['Sharpe Ratio']) else 1.0,
                        alpha=float(row['Alpha']) if pd.notna(row['Alpha']) else 0.0,
                        sortino_ratio=float(row['Sortino Ratio']) if pd.notna(row['Sortino Ratio']) else 1.2,
                        tracking_error=float(row['Tracking Error']) if pd.notna(row['Tracking Error']) else 3.0,
                        time_since_inception=months,
                        sebi_risk_category=sebi_risk_category,
                        months_held=random.randint(6, 36),
                        is_goal_linked=random.choice([True, False])
                    )
                except Exception as e:
                    print(f"Error processing MF row for {mf_name}: {str(e)}")
                    continue
        else:
            print(f"Warning: Mutual Fund screener CSV not found at {mf_csv_path}")
            self._initialize_sample_mf_data()

    def _initialize_sample_stock_data(self):
        """Fallback method to initialize sample stock data"""
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
    
    def _initialize_sample_mf_data(self):
        """Initialize sample mutual fund data"""
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
        """Calculate total Assets Under Management using actual prices"""
        total_aum = 0
        
        # Calculate stock AUM
        for member, stocks in stock_map.items():
            for stock, quantity in stocks.items():
                if stock in self.stock_prices:
                    total_aum += quantity * self.stock_prices[stock]
                else:
                    print(f"Warning: Price not found for stock {stock}")
        
        # Calculate MF AUM - now using direct net worth values
        for member, mfs in mf_map.items():
            for mf_name, net_worth in mfs.items():
                total_aum += net_worth  # net_worth is now directly the value in rupees
        
        # Add bank balances
        for member, balance in bank_balances.items():
            total_aum += balance
            
        return total_aum

    def get_target_bank_percentage(self, purpose: Purpose, timeline: Timeline) -> float:
        """Determine target bank balance percentage of total AUM for optimization"""
        if purpose == Purpose.EMERGENCY:
            if timeline == Timeline.IMMEDIATE or timeline == Timeline.WITHIN_WEEK:
                return 0.15  # Keep 15% in bank for immediate emergencies
            elif timeline == Timeline.ONE_TO_FOUR_WEEKS:
                return 0.12  # Keep 12% in bank for near-term emergencies
            else:
                return 0.10  # Keep 10% for non-urgent emergencies
        elif purpose == Purpose.PLANNED_PURCHASE:
            if timeline == Timeline.NO_URGENCY:
                return 0.05  # Keep 5% in bank for planned purchases with no urgency
            else:  # Urgent planned purchases
                return 0.10  # Keep 10% in bank for urgent purchases
        elif purpose == Purpose.LOAN_REPAYMENT:
            return 0.12  # Keep 12% in bank for loan repayments
        else:  # Other
            return 0.08  # Keep 8% in bank for other purposes
            
        return 0.08  # Default to 8%

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

    def optimize_liquidation(self, mf_map: Dict, stock_map: Dict, 
                           bank_balances: Dict, question_answers: Dict) -> Dict:
        """
        Main function to optimize asset liquidation based on decision tree
        
        Inputs:
        - mf_map: {family_member: {mf_name: quantity}}
        - stock_map: {family_member: {stock_id: quantity}}
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
        
        # Initialize response structure
        response = {
            "primary_liquidation": {},
            "secondary_liquidation": {}
        }
        
        remaining_amount = amount_needed
        
        # Step 1: Bank balance optimization
        target_bank_percentage = self.get_target_bank_percentage(purpose, timeline)
        total_bank_balance = sum(bank_balances.values())
        current_bank_percentage = (total_bank_balance / total_aum) * 100
        target_bank_balance = total_aum * target_bank_percentage
        
        # Only liquidate bank funds if current percentage exceeds target percentage
        bank_liquidation_amount = 0
        if current_bank_percentage > (target_bank_percentage * 100):
            # Calculate excess bank balance that can be liquidated
            excess_bank_balance = total_bank_balance - target_bank_balance
            bank_liquidation_amount = min(excess_bank_balance, remaining_amount)
        else:
            # Bank balance is below or at target - don't liquidate any bank funds
            bank_liquidation_amount = 0
        
        if bank_liquidation_amount > 0:
            # Distribute bank liquidation proportionally across members
            for member, balance in bank_balances.items():
                if balance > 0 and bank_liquidation_amount > 0:
                    # Calculate this member's proportion of total bank balance
                    member_proportion = balance / total_bank_balance
                    member_liquidation = member_proportion * bank_liquidation_amount
                    
                    # Ensure we don't liquidate more than the member's balance
                    member_liquidation = min(member_liquidation, balance)
                    
                    if member_liquidation > 0:
                        if member not in response["primary_liquidation"]:
                            response["primary_liquidation"][member] = {}
                        response["primary_liquidation"][member]["Bank"] = {
                            "id": "Bank",
                            "value_to_sell": round(member_liquidation, 2),
                            "reason": f'Bank balance ({current_bank_percentage:.1f}%) exceeds target ({target_bank_percentage*100:.1f}%)'
                        }
                        remaining_amount -= member_liquidation
        
        # Step 2: If more money needed, sell assets
        if remaining_amount > 0:
            # Create list of all assets with scores
            all_assets = []
            
            # Score all stocks
            for member, stocks in stock_map.items():
                # Skip if member should be prioritized to retain
                if member in priority_members:
                    continue
                    
                for stock, quantity in stocks.items():
                    score = self.score_stock_for_sale(stock, purpose, timeline)
                    if stock in self.stock_prices:
                        estimated_value = quantity * self.stock_prices[stock]
                        all_assets.append({
                            'member': member,
                            'asset_id': stock,
                            'type': 'stock',
                            'score': score,
                            'estimated_value': estimated_value
                        })
            
            # Score all MFs
            for member, mfs in mf_map.items():
                # Skip if member should be prioritized to retain
                if member in priority_members:
                    continue
                    
                for mf_name, net_worth in mfs.items():
                    score = self.score_mf_for_sale(mf_name, purpose, timeline)
                    if mf_name in self.mf_metrics:
                        all_assets.append({
                            'member': member,
                            'asset_id': mf_name,
                            'type': 'mf',
                            'score': score,
                            'estimated_value': net_worth
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
                
                # Add to response
                if member not in response["primary_liquidation"]:
                    response["primary_liquidation"][member] = {}
                
                asset_type = "Stock" if asset['type'] == 'stock' else "MF"
                if asset_type not in response["primary_liquidation"][member]:
                    response["primary_liquidation"][member][asset_type] = {
                        "id": asset_type,
                        "value_to_sell": 0,
                        "reason": ""
                    }
                
                response["primary_liquidation"][member][asset_type]["value_to_sell"] += round(amount_from_asset, 2)
                if asset['type'] == 'stock':
                    reason = self._get_stock_sell_reason(asset_id, asset['score'])
                else:
                    reason = self._get_mf_sell_reason(asset_id, asset['score'])
                response["primary_liquidation"][member][asset_type]["reason"] = reason
                
                remaining_amount -= amount_from_asset
        
        # Step 3: Identify additional poor performers for reinvestment suggestions
        poor_assets, total_poor_value = self.identify_poor_performers(mf_map, stock_map)
        
        # Add secondary liquidation (poor performers)
        for member, assets in poor_assets.items():
            if assets:  # Only add if there are assets to liquidate
                response["secondary_liquidation"][member] = []
                for asset in assets:
                    asset_type = "Stock" if asset["type"] == "stock" else "MF"
                    response["secondary_liquidation"][member].append({
                        "id": asset_type,
                        "value_to_sell": asset["estimated_value"],
                        "reason": asset["issues"]
                    })
        
        return response

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