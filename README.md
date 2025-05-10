# VM-Auto-Scaling-Project
This project implements an automated VM scaling solution using AWS services. It processes CSV files uploaded to an S3 bucket, reads VM requirements, and dynamically scales EC2 instances up or down using a Lambda function. The system ensures efficient resource allocation based on workload demands.
Objectives
Store VM requirement CSV files in an S3 bucket.

Process CSV files using a Lambda function to scale EC2 instances.

Grant necessary permissions via IAM roles.

Secure EC2 instances with a security group and key pair.

Automate Lambda execution on S3 uploads.

Prerequisites
AWS account with access to S3, Lambda, EC2, IAM, and CloudWatch.

Basic knowledge of AWS Console and Python.

AWS CLI (optional for automation).

Architecture
S3 Bucket: Stores CSV files with VM requirements.

Lambda Function: Processes CSV files and manages EC2 instances.

IAM Role: Grants Lambda permissions to access S3, EC2, and CloudWatch.

Security Group: Allows SSH/HTTP access to EC2 instances.

Key Pair: Enables secure SSH access to instances.

CloudWatch: Logs Lambda execution details.

