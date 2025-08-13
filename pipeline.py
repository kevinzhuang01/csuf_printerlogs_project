import ast
import json
from collections import defaultdict
from datetime import datetime
import boto3

def read_logs(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield ast.literal_eval(line.strip())  # Convert string dict to Python dict

def aggregate_data(logs):
    usage_summary = defaultdict(lambda: {"pages": 0, "cost": 0})
    for log in logs:
        location = log["location"]
        usage_summary[location]["pages"] += log["pages"]
        usage_summary[location]["cost"] += log["cost"]
    return usage_summary

def save_to_s3(data, bucket_name, s3_key):
    s3 = boto3.client("s3")
    s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=s3_key)
    print(f"Saved to s3://{bucket_name}/{s3_key}")

def main():
    logs = read_logs("csuf_printer_logs.txt")
    summary = aggregate_data(logs)

    print("Summary:", summary)

    # Save to S3 (requires AWS credentials in your env)
    bucket = "your-bucket-name"
    key = f"printer_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    save_to_s3(summary, bucket, key)

if __name__ == "__main__":
    main()


