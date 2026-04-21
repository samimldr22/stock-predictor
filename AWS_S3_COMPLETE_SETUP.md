# Complete AWS S3 Setup Guide - Step by Step

## Part 1: Create AWS Account & S3 Bucket

### Step 1: Sign Up for AWS
1. Go to https://aws.amazon.com/
2. Click **"Create AWS Account"**
3. Enter your email, password, and account name
4. Add payment method (credit/debit card)
5. Verify phone number
6. Choose **"Basic Support Plan"** (free tier)
7. Complete sign-up

### Step 2: Create S3 Bucket
1. Log in to AWS Console: https://console.aws.amazon.com/
2. Search for **"S3"** in the search bar at top
3. Click on **"S3"** service
4. Click **"Create bucket"** button (orange)
5. Fill in:
   - **Bucket name**: `stock-predictor-models-YOURNAME` (must be globally unique)
     - Example: `stock-predictor-models-john123`
     - Use lowercase, hyphens allowed
     - Note this name down! You'll need it later
   - **Region**: Select **"us-east-1"** (closest/cheapest)
6. Leave all other settings as default
7. Click **"Create bucket"** at bottom
8. ✅ Done! Your bucket is created

---

## Part 2: Create AWS Credentials (Access Key & Secret)

### Step 3: Create IAM User
1. In AWS Console, search for **"IAM"** (Identity and Access Management)
2. Click on **"IAM"** service
3. In left sidebar, click **"Users"**
4. Click **"Create user"** button
5. Enter **User name**: `stock-predictor-app`
6. Click **"Next"**
7. Click **"Attach policies directly"**
8. Search for **"S3"** in the search box
9. Check this policy: **"AmazonS3FullAccess"** (gives S3 permissions)
10. Click **"Next"** → **"Create user"**
11. ✅ User created

### Step 4: Generate Access Key & Secret
1. Click on the user you just created: **"stock-predictor-app"**
2. Go to **"Security credentials"** tab
3. Scroll down to **"Access keys"** section
4. Click **"Create access key"**
5. Select **"Application running outside AWS"**
6. Click **"Create access key"**
7. **IMPORTANT**: You'll see:
   - **Access Key ID** (starts with AKIA...)
   - **Secret Access Key** (long string)
   
   **⚠️ Copy BOTH and save them somewhere safe!** You can only see the secret once.

**Save these 3 values:**
```
S3 Bucket Name: stock-predictor-models-yourname
Access Key ID: AKIA...
Secret Access Key: xxxx...
```

---

## Part 3: Add Secrets to GitHub

### Step 5: Go to Your GitHub Repository
1. Open https://github.com and log in
2. Go to your **stock-predictor** repository
3. Click **"Settings"** tab (top right)
4. In left sidebar, click **"Secrets and variables"** → **"Actions"**

### Step 6: Add First Secret (AWS Access Key)
1. Click **"New repository secret"** button
2. **Name**: `AWS_ACCESS_KEY_ID`
3. **Secret**: Paste your Access Key ID (AKIA...)
4. Click **"Add secret"**

### Step 7: Add Second Secret (AWS Secret Key)
1. Click **"New repository secret"** again
2. **Name**: `AWS_SECRET_ACCESS_KEY`
3. **Secret**: Paste your Secret Access Key (the long string)
4. Click **"Add secret"**

### Step 8: Add Third Secret (S3 Bucket Name)
1. Click **"New repository secret"** again
2. **Name**: `S3_BUCKET_NAME`
3. **Secret**: `stock-predictor-models-yourname` (the exact bucket name you created)
4. Click **"Add secret"**

✅ **All three secrets are now in GitHub!**

---

## Part 4: Test Locally (Optional but Recommended)

### Step 9: Set Environment Variables on Your Computer

**On Windows (PowerShell):**
```powershell
$env:AWS_ACCESS_KEY_ID = "AKIA..."
$env:AWS_SECRET_ACCESS_KEY = "your_secret_key_here"
$env:AWS_DEFAULT_REGION = "us-east-1"
$env:S3_BUCKET_NAME = "stock-predictor-models-yourname"
```

**Or create a `.env` file in project root:**
```
AWS_ACCESS_KEY_ID=AKIA...
AWS_SECRET_ACCESS_KEY=your_secret
AWS_DEFAULT_REGION=us-east-1
S3_BUCKET_NAME=stock-predictor-models-yourname
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

And add to top of model.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Step 10: Test the Code
1. In terminal, navigate to project:
   ```bash
   cd c:\Users\HP\stock-predictor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run a test prediction:
   ```bash
   python model.py
   ```

4. Should see:
   ```
   [yfinance download...]
   Model trained for AAPL and saved to S3!
   Predicted price: $ 185.42
   ```

✅ If you see this, S3 is working!

---

## Part 5: Deploy to EC2

### Step 11: Update EC2 Instance
Your GitHub Actions workflow will now automatically:
1. Detect push to `main` branch
2. SSH into your EC2 instance
3. Pull latest code
4. Install dependencies
5. Set AWS credentials as environment variables
6. Start the app

**The deployment workflow already has this configured** in `.github/workflows/deploy.yml`

---

## Part 6: Test Indian Stocks

### Step 12: Test with Indian Stock Ticker
Once deployed, test:
```
http://your-ec2-public-ip:5000/predict?ticker=INFY.NS
```

Expected response:
```json
{
  "ticker": "INFY.NS",
  "predicted_price": 1245.67,
  "currency": "USD",
  "status": "success"
}
```

**Working Indian stock tickers:**
- `INFY.NS` - Infosys
- `TCS.NS` - Tata Consultancy Services
- `RELIANCE.NS` - Reliance Industries
- `HDFCBANK.NS` - HDFC Bank
- `WIPRO.NS` - Wipro
- `LT.NS` - Larsen & Toubro
- `BAJAJFINSV.NS` - Bajaj Finserv
- `JSWSTEEL.NS` - JSW Steel

---

## Troubleshooting

### Error: "NoCredentialsError"
- ✅ Verify all 3 GitHub secrets are added correctly
- ✅ Check secret names are EXACTLY: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET_NAME`
- ✅ Redeploy after adding secrets (push to main branch)

### Error: "Access Denied" on S3
- ✅ Verify IAM user has "AmazonS3FullAccess" policy attached
- ✅ Check bucket name is spelled correctly in S3_BUCKET_NAME secret

### Error: "The specified bucket does not exist"
- ✅ Verify bucket was created successfully in S3 console
- ✅ Bucket name is case-sensitive in S3_BUCKET_NAME secret
- ✅ Make sure region is us-east-1

### App won't start after deployment
- Check EC2 logs:
  ```bash
  tail -f /home/ubuntu/app.log
  ```
- Verify all secrets are set on EC2 (they're set by GitHub Actions)

---

## Security Best Practices

⚠️ **NEVER:**
- Commit `.env` file to GitHub
- Share your AWS credentials
- Use `AmazonS3FullAccess` in production (use specific bucket policies instead)

✅ **DO:**
- Keep credentials in GitHub Secrets only
- Rotate credentials every 90 days
- Delete old access keys when creating new ones

---

## Cost

- ✅ AWS Free Tier: 5GB free S3 storage for 12 months
- ✅ Our app uses minimal storage (<1MB for models)
- ✅ **Cost: $0/month** for this project under free tier

---

## Summary Checklist

- [ ] Created AWS Account
- [ ] Created S3 Bucket
- [ ] Created IAM User
- [ ] Generated Access Key & Secret
- [ ] Added 3 secrets to GitHub:
  - [ ] `AWS_ACCESS_KEY_ID`
  - [ ] `AWS_SECRET_ACCESS_KEY`
  - [ ] `S3_BUCKET_NAME`
- [ ] Tested locally (optional)
- [ ] Deployed to EC2
- [ ] Tested with `/predict?ticker=INFY.NS`

You're all set! 🚀
