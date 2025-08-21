import ast
import json
import logging
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, Generator, Any
import os
from datetime import datetime
import boto3
logging.basicConfig(level = logging.INFO)
@dataclass
class LogEntry:
    location: str
    pages: int
    cost: float


def read_logs(filepath:str) -> Generator[LogEntry,None,None]:
    with open(filepath, 'r') as f:
        for line in f:
            try:
                log = ast.literal_eval(line.strip())
                yield ast.literal_eval(line.strip())
            except Exception as e:
                logging.warning(f"Skipping invalid log line: {line}, error: {e}")
def aggregate_data(logs: Generator[LogEntry,None,None]) -> Dict[str,Dict[str,Any]]:
    usage_summary = defaultdict(lambda: {"pages": 0, "cost": 0})
    for log in logs:
        usage_summary[log.location]["pages"] += log["pages"]
        usage_summary[log.location]["cost"] += log["cost"]
    return dict(usage_summary)

def save_to_s3(data:dict, bucket_name:str, s3_key:str)-> None:
    s3 = boto3.client("s3")
    try:
        s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=s3_key)
        logging.info(f"Saved to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        logging.error("Failed to save to S3: {e}")


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


