from pydantic import BaseModel
from datetime import date
from decimal import Decimal


class StockPrice(BaseModel):
    symbol: str
    trade_date: date
    open_price: Decimal
    close_price: Decimal
    low_price: Decimal
    high_price: Decimal
