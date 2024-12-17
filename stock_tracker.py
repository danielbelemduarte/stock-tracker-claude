import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def fetch_stock_price(ticker):
    """
    Fetch the current price of a stock given its ticker symbol.
    
    Args:
        ticker (str): Stock ticker symbol
    
    Returns:
        dict: A dictionary containing stock price information
    """
    try:
        # Fetch stock information
        stock = yf.Ticker(ticker)
        
        # Get current stock price
        current_price = stock.info.get('regularMarketPrice')
        
        # Get additional relevant information
        return {
            'ticker': ticker,
            'current_price': round(current_price, 2) if current_price else None,
            'company_name': stock.info.get('longName', 'N/A'),
            'previous_close': round(stock.info.get('previousClose', 0), 2),
            'market_cap': stock.info.get('marketCap', 'N/A')
        }
    
    except Exception as e:
        return {
            'error': f'Error fetching stock price for {ticker}: {str(e)}'
        }

def get_stock_moving_average(ticker, days=365):
    """
    Calculate the moving average of a stock over the last year.
    
    Args:
        ticker (str): Stock ticker symbol
        days (int): Number of days to calculate moving average (default: 365)
    
    Returns:
        dict: A dictionary containing moving average details
    """
    # Get current date and date one year ago
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        # Download stock data
        stock_data = yf.download(ticker, start=start_date, end=end_date)
        
        if stock_data.empty:
            return {
                'error': f'No data available for ticker: {ticker}'
            }
        
        # Calculate moving averages
        stock_data['50_day_ma'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['200_day_ma'] = stock_data['Close'].rolling(window=200).mean()
        
        # Get latest moving averages
        latest_50_day_ma = stock_data['50_day_ma'].iloc[-1]
        latest_200_day_ma = stock_data['200_day_ma'].iloc[-1]
        current_price = stock_data['Close'].iloc[-1]
        
        return {
            'ticker': ticker,
            'current_price': round(current_price, 2),
            '50_day_ma': round(latest_50_day_ma, 2),
            '200_day_ma': round(latest_200_day_ma, 2),
            'trend': 'Bullish' if current_price > latest_50_day_ma and latest_50_day_ma > latest_200_day_ma else 'Bearish'
        }
    
    except Exception as e:
        return {
            'error': f'Error fetching stock data: {str(e)}'
        }

def main():
    # Example usage
    tickers = ['AAPL', 'GOOGL', 'MSFT']
    
    print("Stock Price Fetching:")
    for ticker in tickers:
        price_info = fetch_stock_price(ticker)
        print(f"\nStock Price for {ticker}:")
        for key, value in price_info.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
    
    print("\n\nMoving Average Analysis:")
    for ticker in tickers:
        result = get_stock_moving_average(ticker)
        print(f"\nStock Analysis for {ticker}:")
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")

if __name__ == '__main__':
    main()