import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from amzn_bedrock_demo.model import StockPrice

market_history: list[StockPrice] = []

csv_path = Path(__file__).parent / "data" / "market_history.csv"
with open(csv_path) as f:
    reader = csv.DictReader(f)
    for row in reader:
        market_history.append(
            StockPrice(
                symbol=row["symbol"],
                trade_date=date.fromisoformat(row["trade_date"]),
                open_price=Decimal(row["open_price"]),
                close_price=Decimal(row["close_price"]),
                low_price=Decimal(row["low_price"]),
                high_price=Decimal(row["high_price"]),
            )
        )
