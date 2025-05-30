from dataclasses import dataclass
from .enums import SEBIRiskCategory

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