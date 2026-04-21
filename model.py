import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle
import boto3
import os
from io import BytesIO


from dotenv import load_dotenv
load_dotenv()
# S3 Configuration
S3_BUCKET = os.getenv("S3_BUCKET_NAME", "stock-predictor-models")
s3_client = boto3.client("s3")

def train_model(ticker="AAPL", period="6mo"):
    stock = yf.download(ticker, period=period, auto_adjust=True)
    prices = stock["Close"].values.flatten()  # fix: flatten the array
    X, y = [], []
    window = 5
    for i in range(window, len(prices)):
        X.append(prices[i-window:i])
        y.append(prices[i])
    X = np.array(X)
    y = np.array(y)
    model = LinearRegression()
    model.fit(X, y)
    
    # Save model to S3
    model_buffer = BytesIO()
    pickle.dump(model, model_buffer)
    model_buffer.seek(0)
    s3_client.upload_fileobj(model_buffer, S3_BUCKET, f"{ticker}_model.pkl")
    
    # Save last prices to S3
    prices_buffer = BytesIO()
    pickle.dump(prices[-window:], prices_buffer)
    prices_buffer.seek(0)
    s3_client.upload_fileobj(prices_buffer, S3_BUCKET, f"{ticker}_last_prices.pkl")
    
    print(f"Model trained for {ticker} and saved to S3!")

def predict_next(ticker="AAPL"):
    # Load model from S3
    model_buffer = BytesIO()
    s3_client.download_fileobj(S3_BUCKET, f"{ticker}_model.pkl", model_buffer)
    model_buffer.seek(0)
    model = pickle.load(model_buffer)
    
    # Load last prices from S3
    prices_buffer = BytesIO()
    s3_client.download_fileobj(S3_BUCKET, f"{ticker}_last_prices.pkl", prices_buffer)
    prices_buffer.seek(0)
    last_prices = pickle.load(prices_buffer)
    
    prediction = model.predict([last_prices])[0]
    return round(float(prediction), 2)

if __name__ == "__main__":
    train_model("AAPL")
    print("Predicted price: $", predict_next("AAPL"))