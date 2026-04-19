from flask import Flask, jsonify, request, render_template
from model import predict_next, train_model

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict")
def predict():
    ticker = request.args.get("ticker", "AAPL").upper()
    try:
        train_model(ticker)
        price = predict_next()
        return jsonify({
            "ticker": ticker,
            "predicted_price": price,
            "currency": "USD",
            "status": "success"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)