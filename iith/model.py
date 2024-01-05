import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

from io import BytesIO
import base64

sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")

import yfinance as yf
from datetime import datetime, timedelta



def download_stock_data(tech_list, start_date, end_date):
    yf.pdr_override()
    company_list = []
    for stock in tech_list:
        company = yf.download(stock, start_date, end_date)
        company_list.append(company)
    return company_list


def plot_moving_averages(company_list, tech_list):
    ma_day = [10, 20, 50]
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figheight(10)
    fig.set_figwidth(15)

    for i, (company, company_name) in enumerate(zip(company_list, ["A", "B", "C", "D"])):
        for ma in ma_day:
            column_name = f"MA for {ma} days"
            company[column_name] = company['Adj Close'].rolling(ma).mean()

        company[['Adj Close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[i // 2, i % 2])
        axes[i // 2, i % 2].set_title(company_name)

    fig.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image

def plot_daily_returns(company_list, tech_list):
    fig, axes = plt.subplots(nrows=2, ncols=2)
    fig.set_figheight(10)
    fig.set_figwidth(15)

    for i, (company, company_name) in enumerate(zip(company_list, ["A", "B", "C", "D"])):
        company['Daily Return'] = company['Adj Close'].pct_change()
        company['Daily Return'].plot(ax=axes[i // 2, i % 2], legend=True, linestyle='--', marker='o')
        axes[i // 2, i % 2].set_title(company_name)

    fig.tight_layout()
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image


def get_arima_predictions(stock_symbol):
    stock = yf.Ticker(stock_symbol)
    
    start_date = "2023-01-01"
    end_date = datetime.today().strftime('%Y-%m-%d')
    
    data = stock.history(start=start_date, end=end_date)
    data['Date'] = data.index
    features = ['Close', 'Date']
    data = data[features]

    data.set_index('Date', inplace=True)
    data['Previous_Close'] = data['Close'].shift(1)
    data = data.dropna()

    X = data[['Previous_Close']]
    y = data['Close']

    print("fitting model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model_fit = model.fit(X, y)

    last_date = data.index[-1]
    predictions = []

    for i in range(10):
        prediction_data = pd.DataFrame({'Previous_Close': [data['Close'].iloc[-1]]})
        next_day_close = model_fit.predict(prediction_data)[0]
        predictions.append(next_day_close)
        last_date = last_date + timedelta(days=1)
        data.loc[last_date] = [next_day_close, next_day_close]

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Actual Close Prices')
    plt.plot(data['Previous_Close'], label='Previous Day Close Prices', linestyle='--')
    plt.plot(pd.date_range(start=last_date, periods=10), predictions, label='Predicted Close Prices', marker='o')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title('ARIMA Predictions')
    plt.legend()
    
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    image_stream.seek(0)
    encoded_image = base64.b64encode(image_stream.read()).decode('utf-8')
    return encoded_image