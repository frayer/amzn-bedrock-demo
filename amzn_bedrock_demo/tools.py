from datetime import date
from decimal import Decimal
from typing import Literal

from mypy_boto3_bedrock_runtime.type_defs import ToolConfigurationTypeDef

from amzn_bedrock_demo.market_history import market_history
from amzn_bedrock_demo.model import StockPrice
from amzn_bedrock_demo.util import log

"""Tools module for Amazon Bedrock agent interactions.

This module provides tools and configurations for use with Amazon Bedrock's Nova
agents. It includes functions for:

- Stock price lookups and market data queries
- Basic arithmetic operations
- Trading day validation
- Percentage change calculations

The tools are configured to work with Amazon Bedrock's agent system and follow
the required schema for tool definitions.

For more information on using tools with Amazon Nova, see:
https://docs.aws.amazon.com/nova/latest/userguide/tool-use.html
"""


def tool_config() -> ToolConfigurationTypeDef:
    return {
        "tools": [
            {
                "toolSpec": {
                    "name": "is_trading_day",
                    "description": "Return true or false if a given date is a trading day.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "date": {
                                    "type": "string",
                                    "description": "The date to check in YYYY-MM-DD format",
                                },
                            },
                            "required": ["date"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "get_stock_price",
                    "description": "Get the stock open, close, low, and high prices for a given symbol and date.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "symbol": {
                                    "type": "string",
                                    "description": "The symbol of the stock",
                                },
                                "date": {
                                    "type": "string",
                                    "description": "The date of the stock price in YYYY-MM-DD format",
                                },
                            },
                            "required": ["symbol", "date"],
                        }
                    },
                }
            },
            {
                "toolSpec": {
                    "name": "add_subtract_multiply_divide",
                    "description": "Perform addition, subtraction, multiplication, or division on two numbers.",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "operation": {
                                    "type": "string",
                                    "description": "The operation to perform",
                                    "enum": ["add", "subtract", "multiply", "divide"],
                                },
                                "first_num": {
                                    "type": "number",
                                    "description": "The first number",
                                },
                                "second_num": {
                                    "type": "number",
                                    "description": "The second number",
                                },
                            },
                            "required": ["operation", "first_num", "second_num"],
                        },
                    },
                }
            },
            # {
            #     "toolSpec": {
            #         "name": "calculate_percentage_change",
            #         "description": """
            #         Calculate the percentage difference between second_num and
            #         first_num. If the second_num is greater than the first_num,
            #         the result will be positive. If the second_num is less than
            #         the first_num, the result will be negative.
            #         """,
            #         "inputSchema": {
            #             "json": {
            #                 "type": "object",
            #                 "properties": {
            #                     "first_num": {
            #                         "type": "number",
            #                         "description": "The first number",
            #                     },
            #                     "second_num": {
            #                         "type": "number",
            #                         "description": "The second number",
            #                     },
            #                 },
            #                 "required": ["first_num", "second_num"],
            #             }
            #         },
            #     }
            # },
        ]
    }


def add_subtract_multiply_divide(
    operation: str,
    first_num: Decimal,
    second_num: Decimal,
) -> Decimal | None:
    if operation not in ["add", "subtract", "multiply", "divide"]:
        raise ValueError(
            f"Invalid operation '{operation}'. Must be one of: add, subtract, multiply, divide"
        )

    """
    Perform addition, subtraction, multiplication, or division on two numbers.
    """
    log.info(f"Performing {operation} on {first_num:.2f} and {second_num:.2f}")

    if operation == "add":
        return first_num + second_num
    elif operation == "subtract":
        return first_num - second_num
    elif operation == "multiply":
        return first_num * second_num
    elif operation == "divide":
        return first_num / second_num


def is_trading_day(date_str: str) -> bool:
    """
    Check if a given date is a trading day.
    """
    log.info(f"Checking if {date_str} is a trading day")

    parsed_date = date.fromisoformat(date_str)
    return any(sp.trade_date == parsed_date for sp in market_history)


def get_stock_price(symbol: str, date_str: str) -> StockPrice | None:
    """
    Get the stock open, close, low, and high prices for a given symbol and date.
    """
    log.info(f"Getting stock price for {symbol} on {date_str}")

    parsed_date = date.fromisoformat(date_str)
    return next(
        (
            sp
            for sp in market_history
            if sp.symbol == symbol and sp.trade_date == parsed_date
        ),
        None,
    )


def calculate_percentage_change(first_num: Decimal, second_num: Decimal) -> Decimal:
    """
    Calculate the percentage difference between second_num and first_num.
    """
    log.info(f"Calculating percentage change for {first_num:.2f} and {second_num:.2f}")

    return (second_num - first_num) / first_num
