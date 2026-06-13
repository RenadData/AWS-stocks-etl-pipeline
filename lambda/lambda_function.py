import boto3
import csv
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    RAW_BUCKET = "renad-raw-data"          
    PROCESSED_BUCKET = "renad-processes-data"  
    FILE_KEY = "Prices.csv"

    try:
        # Read raw CSV from S3
        response = s3.get_object(Bucket=RAW_BUCKET, Key=FILE_KEY)
        csv_content = response['Body'].read().decode('utf-8')

        reader = csv.reader(io.StringIO(csv_content))
        header = next(reader)  # ['Date', 'AAPL', 'AMZN', ...]
        tickers = header[1:]   

        # Reshape 
        long_rows = []
        for row in reader:
            date = row[0]
            for i, ticker in enumerate(tickers):
                price = row[i + 1]
                # Skip missing values
                if not price or price.strip() == '':
                    continue
                long_rows.append({
                    "date": date,
                    "ticker": ticker,
                    "price": round(float(price), 2)
                })

        # Write to CSV
        output_csv = io.StringIO()
        writer = csv.DictWriter(output_csv, fieldnames=["date", "ticker", "price"])
        writer.writeheader()
        writer.writerows(long_rows)

        # Upload to processed bucket
        s3.put_object(
            Bucket=PROCESSED_BUCKET,
            Key="processed/stocks_clean.csv",
            Body=output_csv.getvalue()
        )
        print(f"Done! {len(long_rows)} rows written.")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise