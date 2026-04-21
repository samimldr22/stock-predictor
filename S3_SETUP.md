# S3 Integration Setup

## Prerequisites
- AWS Account with S3 access
- AWS CLI configured or IAM user credentials

## Environment Variables Required

Add these to your GitHub Secrets for CI/CD:
- `AWS_ACCESS_KEY_ID` - AWS access key
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `S3_BUCKET_NAME` - Name of your S3 bucket (e.g., "stock-predictor-models")

For local development, set:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
export S3_BUCKET_NAME=your-bucket-name
```

## How It Works

1. **Training**: When `/predict` is called, the model trains and saves directly to S3:
   - `{ticker}_model.pkl` - The trained Linear Regression model
   - `{ticker}_last_prices.pkl` - Last 5 prices for prediction

2. **Prediction**: Loads the latest model and prices from S3, then predicts the next price

3. **Benefits**:
   - No local file storage needed
   - Models persist across app restarts
   - Easily scalable to multiple instances
   - Ticker-specific models for accuracy

## Indian Stock Support

✅ Indian stocks work perfectly with yfinance using NSE suffix:
- **INFY.NS** - Infosys
- **TCS.NS** - Tata Consultancy Services
- **RELIANCE.NS** - Reliance Industries
- **HDFCBANK.NS** - HDFC Bank
- **WIPRO.NS** - Wipro
- **LT.NS** - Larsen & Toubro

Example: `/predict?ticker=INFY.NS`

## S3 Bucket Policy

Ensure your S3 bucket has a policy allowing the EC2 instance (or IAM user) permissions:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```
