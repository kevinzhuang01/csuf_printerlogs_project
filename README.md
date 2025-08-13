# CSUF Printer Logs Data Pipeline

## Overview

This project simulates and processes printer usage logs for Cal State University, Fullerton buildings: Computer Science, Liberal Arts, and Electrical Engineering.

It includes:

- Printer logs data collected from three Campus buildings .
- A data processing pipeline that aggregates usage metrics (pages printed, cost) per building.
- Integration with AWS S3 to store aggregated results for scalable access.
- A Dockerfile for containerizing the pipeline for easy deployment.
- AWS Lambda handler for serverless execution.
