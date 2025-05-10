import boto3
import csv
from io import StringIO

ec2 = boto3.client('ec2')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Configuration (CHANGE THESE)
    AMI_ID = 'ami-0abcdef1234567890'  # Find your AMI in EC2 Console
    INSTANCE_TYPE = 't3.micro'
    SECURITY_GROUP_IDS = ['sg-0123456789abcdef']  # From Step 3
    KEY_NAME = 'scaling-keypair'  # From Step 4
    
    # Get uploaded file
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Read CSV
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    csv_data = file_obj['Body'].read().decode('utf-8')
    reader = csv.DictReader(StringIO(csv_data))
    
    # Get latest VM requirement
    last_row = None
    for row in reader:
        last_row = row
    required_vms = int(last_row['VMs_needed'])
    
    # Get current running instances
    instances = ec2.describe_instances(Filters=[
        {'Name': 'instance-state-name', 'Values': ['running', 'pending']},
        {'Name': 'tag:ScalingGroup', 'Values': ['auto-scaled-vms']}
    ])
    current_vms = len(instances['Reservations'])
    
    # Scale instances
    if required_vms > current_vms:
        print(f"Creating {required_vms - current_vms} instances")
        ec2.run_instances(
            ImageId=AMI_ID,
            InstanceType=INSTANCE_TYPE,
            SecurityGroupIds=SECURITY_GROUP_IDS,
            KeyName=KEY_NAME,
            MinCount=1,
            MaxCount=required_vms - current_vms,
            TagSpecifications=[{
                'ResourceType': 'instance',
                'Tags': [{'Key': 'ScalingGroup', 'Value': 'auto-scaled-vms'}]
            }]
        )
    elif required_vms < current_vms:
        print(f"Terminating {current_vms - required_vms} instances")
        instance_ids = [i['InstanceId'] for r in instances['Reservations'] 
                        for i in r['Instances']][:current_vms - required_vms]
        ec2.terminate_instances(InstanceIds=instance_ids)
    
    return {'statusCode': 200}
