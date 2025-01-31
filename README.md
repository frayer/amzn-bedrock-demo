# Amazon Bedrock Demo

This is a demo of using Amazon Bedrock's Nova agent to answer questions about stock prices using locally mocked data.

# Running the demo

1. Install [uv](https://docs.astral.sh/uv/)
2. Sync the dependencies

```bash
uv sync
```

3. Run the demo

```bash
uv run main.py
```

4. Try one of the sample prompts below or enter your own

## Sample promts to test the agent

1. What was the percentage difference between the closing price of AAPL and NVDA on Jan 2, 2024?
1. Was the 1/31/24 closing price of AAPL higher or lower than its 1/2/24 closing price?
1. How much more was a share of NVDA worth compared to AAPL on Jan 29, 2024 expressed as a percentage?
1. Was NVDA or AAPL stock worth more on Jan 31, 2024? Answer with the ticker name and their difference when you know the answer.
1. Which was worth more on Jan 29, 2024? A share of NVDA or a share of AAPL? Reply with the ticker name when you know the answer.
1. How much did NVDA increase in the month of January 2024? Make sure you know whether a date was a trading date or not when retrieving prices.
1. Create a markdown table with the closing price of AAPL, closing price of NVDA, and the price of AAPL subtracted from the price of NVDA for the dates 1/2/24, 1/3/24, and 1/4/24.

## Example output from "How much more was a share of NVDA worth compared to AAPL on Jan 29, 2024 expressed as a percentage?"

```
Enter a prompt: How much more was a share of NVDA worth compared to AAPL on Jan 29, 2024 expressed as a percentage?

Thought » To calculate the percentage difference in price between NVDA and AAPL on January 29, 2024, I first need to retrieve the closing prices for both stocks on that date. I will use the 'get_stock_price' tool for this. After obtaining the prices, I will use the 'add_subtract_multiply_divide' tool to find the difference and then calculate the percentage difference.
Output »

2025-01-31 04:04:44 [info ] Getting stock price for NVDA on 2024-01-29
2025-01-31 04:04:44 [info ] Getting stock price for AAPL on 2024-01-29

Thought » I have retrieved the closing prices for NVDA and AAPL on January 29, 2024. The closing price for NVDA was $544.67, and for AAPL, it was $193.45. To find out how much more NVDA was worth compared to AAPL, I will subtract the AAPL price from the NVDA price and then divide by the AAPL price. Finally, I will multiply by 100 to express the result as a percentage.
Output »

2025-01-31 04:04:46 [info ] Performing subtract on 544.67 and 193.45
2025-01-31 04:04:46 [info ] Performing divide on 544.67 and 193.45
2025-01-31 04:04:46 [info ] Performing multiply on 100.00 and 544.67

Thought » The subtraction tool result indicates that NVDA was $351.22 more expensive than AAPL on January 29, 2024. The division tool result shows that NVDA was approximately 2.816 times more expensive than AAPL. To express this as a percentage, I will multiply the division result by 100 and subtract 100 to account for the base value of AAPL (100%).
Output »

2025-01-31 04:04:48 [info ] Performing subtract on 2.82 and 1.00
2025-01-31 04:04:48 [info ] Performing multiply on 100.00 and 2.82

Thought » The result from the subtraction tool indicates that NVDA was 1.81555957611786 times more expensive than AAPL. To convert this to a percentage, I will multiply by 100, which gives me the percentage difference.
Output »
A share of NVDA was approximately 181.56% more expensive than a share of AAPL on January 29, 2024.
```

## Example output from "How much more was a share of NVDA worth compared to AAPL on Jan 29, 2024 expressed as a percentage?"

```
Enter a prompt: Create a markdown table with the closing price of AAPL, closing price of NVDA, and their dollar difference for the dates 1/2/24, 1/3/24, and 1/4/24

Thought » I need to first verify if these dates are trading days. Then, I need to get the closing prices for AAPL and NVDA for these dates, and finally calculate the dollar difference between the two. I will need to use the `is_trading_day`, `get_stock_price`, and `add_subtract_multiply_divide` tools for this task.
Output »

2025-01-31 03:38:03 [info ] Checking if 2024-01-02 is a trading day
2025-01-31 03:38:03 [info ] Checking if 2024-01-03 is a trading day
2025-01-31 03:38:03 [info ] Checking if 2024-01-04 is a trading day
Thought » All three dates are trading days. I will now get the closing prices for AAPL and NVDA for these dates.
Output »

2025-01-31 03:38:04 [info ] Getting stock price for AAPL on 2024-01-02
2025-01-31 03:38:04 [info ] Getting stock price for AAPL on 2024-01-03
2025-01-31 03:38:04 [info ] Getting stock price for AAPL on 2024-01-04
2025-01-31 03:38:04 [info ] Getting stock price for NVDA on 2024-01-02
2025-01-31 03:38:04 [info ] Getting stock price for NVDA on 2024-01-03
2025-01-31 03:38:04 [info ] Getting stock price for NVDA on 2024-01-04

Thought » I now have the closing prices for AAPL and NVDA for the three dates. The next step is to calculate the dollar difference between the closing prices of AAPL and NVDA for each date.
Output »

2025-01-31 03:38:06 [info ] Performing subtract on 185.64 and 492.16
2025-01-31 03:38:06 [info ] Performing subtract on 181.91 and 488.23
2025-01-31 03:38:06 [info ] Performing subtract on 183.98 and 482.11

Thought » I have calculated the dollar difference between the closing prices of AAPL and NVDA for the three dates. The final step is to create a markdown table with the closing prices of AAPL, closing prices of NVDA, and their dollar difference for the dates 1/2/24, 1/3/24, and 1/4/24.
Output »
| Date | AAPL Closing Price | NVDA Closing Price | Dollar Difference |
|------------|--------------------|--------------------|-------------------|
| 1/2/24 | 185.64 | 492.16 | -306.52 |
| 1/3/24 | 181.91 | 488.23 | -306.32 |
| 1/4/24 | 183.98 | 482.11 | -298.13 |
```
