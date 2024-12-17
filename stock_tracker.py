import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

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
    
    for ticker in tickers:
        result = get_stock_moving_average(ticker)
        print(f"Stock Analysis for {ticker}:")
        for key, value in result.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        print('\n')

if __name__ == '__main__':
    main()