# Smart Liquidity Engine

A tool for optimizing asset liquidation based on user portfolio and questionnaire data.

## Local Development

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the application:

```bash
python -m src.app
```

The server will start at http://localhost:5001

## API Documentation

### Optimize Liquidation Endpoint

`POST /api/optimize-liquidation`

Request body:

```json
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
```

## Deployment

This application is configured for deployment on Render.com. The deployment is handled automatically through the `render.yaml` configuration file.

### Manual Deployment Steps

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Use the following settings:
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn src.app:create_app()`
   - Environment Variables:
     - PYTHON_VERSION: 3.11.0
     - PORT: 10000
     - HOST: 0.0.0.0
     - FLASK_DEBUG: false
