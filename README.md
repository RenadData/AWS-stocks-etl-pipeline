# AWS-stocks-etl-pipeline
# Stocks ETL Pipeline — AWS S3 + Lambda + QuickSight

An end-to-end serverless ETL pipeline that ingests raw stock price data, transforms it using AWS Lambda, and delivers clean data ready for visualization in Amazon QuickSight.

---

##  Project Overview

Stock price data often comes in a wide format — one column per ticker, one row per date — which is difficult to query and visualize. This pipeline automatically reshapes that data into a clean long format and stores it in a processed S3 bucket, ready for analysis.

**Tracked tickers:** AAPL · AMZN · GOOGL · JNJ · JPM · META · MSFT · NVDA · PG · XOM

**Date range:** 2015 – present

---

##  Architecture

```
Raw S3 Bucket (renad-raw-data)
        │
        │  Prices.csv (wide format)
        ▼
  AWS Lambda Function
        │
        │  - Reads CSV from S3
        │  - Reshapes wide → long format
        │  - Cleans missing values
        │  - Rounds prices to 2 decimal places
        ▼
Processed S3 Bucket (renad-processes-data)
        │
        │  stocks_clean.csv (long format)
        ▼
  Amazon QuickSight
        │
        │  Connected via S3 manifest
        ▼
   Dashboard & Insights
```

---

## Data Transformation

### Before (Wide Format)
| Date | AAPL | AMZN | GOOGL | ... |
|------|------|------|-------|-----|
| 2015-01-02 | 24.24 | 15.43 | 26.28 | ... |
| 2015-01-05 | 23.55 | 15.11 | 25.78 | ... |

### After (Long Format)
| date | ticker | price |
|------|--------|-------|
| 2015-01-02 | AAPL | 24.24 |
| 2015-01-02 | AMZN | 15.43 |
| 2015-01-02 | GOOGL | 26.28 |

---

##  Tech Stack

| Layer | Tool |
|-------|------|
| Storage | AWS S3 |
| Compute | AWS Lambda (Python) |
| Visualization | Amazon QuickSight |
| Language | Python 3 (boto3, csv, io) |

---

##  Project Structure

```
stocks-analysis/
├── lambda/
│   └── lambda_function.py     # ETL logic — reads, transforms, writes
├── raw-data/
│   └── Prices.csv             # Raw stock prices (wide format)
├── processed-data/
│   └── stocks_clean.csv       # Cleaned output (long format)
└── manifest.json              # QuickSight S3 data source config
```

---

## How It Works

1. **Ingest** — Raw `Prices.csv` is uploaded to the raw S3 bucket
2. **Trigger** — Lambda function is invoked (manually or via S3 event trigger)
3. **Transform** — Lambda reads the file, iterates through each row and ticker, skips missing values, and reshapes data into long format
4. **Load** — Cleaned CSV is written to the processed S3 bucket at `processed/stocks_clean.csv`
5. **Visualize** — QuickSight connects to the processed bucket via `manifest.json` and renders dashboards

---

## Setup & Deployment

### Prerequisites
- AWS account with S3 and Lambda access
- Two S3 buckets created:
  - `renad-raw-data`
  - `renad-processes-data`

### Steps

**1. Upload raw data**
```bash
aws s3 cp raw-data/Prices.csv s3://renad-raw-data/Prices.csv
```

**2. Deploy Lambda function**
- Go to AWS Lambda → Create Function → Author from scratch
- Runtime: Python 3.x
- Paste the contents of `lambda/lambda_function.py`
- Add IAM permissions for S3 read/write

**3. Run the pipeline**
- Invoke the Lambda function manually from the AWS Console, or
- Set up an S3 event trigger on the raw bucket for automatic runs

**4. Connect QuickSight**
- In Amazon QuickSight, create a new dataset
- Choose S3 as the source
- Upload `manifest.json` to point QuickSight to your processed data

---

## Sample Output

The processed dataset contains price history for 10 major stocks from 2015 onwards, normalized into a query-friendly format — enabling analysis like:

- Price trends per ticker over time
- Comparative performance across stocks
- Year-over-year growth

---

## Author

**Renad Alamri**  
[LinkedIn](https://www.linkedin.com/in/renad-alamri-) · [GitHub](https://github.com/RenadData)
