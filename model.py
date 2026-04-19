import yfinance as yf
import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

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
    with open("model.pkl", "wb") as f:
        pickle.dump(model, f)
    last_prices = prices[-window:]
    with open("last_prices.pkl", "wb") as f:
        pickle.dump(last_prices, f)
    print(f"Model trained for {ticker}!")

def predict_next():
    with open("model.pkl", "rb") as f:
        model = pickle.load(f)
    with open("last_prices.pkl", "rb") as f:
        last_prices = pickle.load(f)
    prediction = model.predict([last_prices])[0]
    return round(float(prediction), 2)

if __name__ == "__main__":
    train_model("AAPL")
    print("Predicted price: $", predict_next())