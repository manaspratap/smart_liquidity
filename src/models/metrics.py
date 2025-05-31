from dataclasses import dataclass
from .enums import SEBIRiskCategory

@dataclass
class StockMetrics:
    """Metrics for evaluating stocks"""
    pe_ratio: float = 25.0  # P/E Ratio
    rsi_14d: float = 50.0  # RSI 14-day (decimal percentage)
    pledged_promoter_holdings: float = 0.0  # Pledged promoter holdings (decimal percentage)
    promoter_holding: float = 0.5  # Promoter holding (decimal percentage)
    beta: float = 1.0  # Beta
    six_month_return_vs_nifty: float = 0.0  # 6M Return vs Nifty (decimal percentage)
    five_year_cagr: float = 0.12  # 5Y CAGR (decimal percentage)
    debt_to_equity: float = 0.5  # Debt to Equity ratio
    roce: float = 0.15  # Return on Capital Employed (decimal percentage)
    return_on_equity: float = 0.15  # Return on Equity (decimal percentage)
    dividend_yield: float = 0.02  # Dividend Yield (decimal percentage)
    free_cash_flow: float = 1000.0  # Free Cash Flow (in crores)
    months_held: int = 12  # Months asset has been held
    is_goal_linked: bool = False  # Whether asset is linked to financial goals

@dataclass
class MFMetrics:
    """Metrics for evaluating mutual funds"""
    cagr_3y: float = 0.12  # 3Y CAGR (decimal percentage)
    expense_ratio: float = 0.015  # Expense ratio (decimal percentage)
    volatility: float = 0.15  # Volatility (decimal percentage)
    sharpe_ratio: float = 1.0  # Sharpe Ratio
    alpha: float = 0.0  # Alpha
    sortino_ratio: float = 1.2  # Sortino Ratio
    tracking_error: float = 3.0  # Tracking Error
    time_since_inception: int = 60  # Time since inception in months
    sebi_risk_category: SEBIRiskCategory = SEBIRiskCategory.MODERATE  # SEBI Risk Category
    months_held: int = 12  # Months asset has been held
    is_goal_linked: bool = False  # Whether asset is linked to financial goals 