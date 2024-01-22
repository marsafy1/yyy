import boto3
import os
from dotenv import load_dotenv

# Loading the .env file
load_dotenv()

# Getting the keys from .env
access_key = os.getenv('AWS_ACCESS_KEY')
secret_key = os.getenv('AWS_SECRET_KEY')

# Configurations
region_name = 'me-central-1'
ami_id = 'ami-0e35ae85b404efe33'
instance_type = 't3.micro'
security_group_id = 'sg-0f99030b4a237d514'

# Creating a boto3 client
client = boto3.client('ec2',
                    region_name=region_name,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=secret_key
                    )
# Getting info about our EC2s resources
conn = boto3.resource('ec2', aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region_name)

# To check if an instance is running
def instance_is_running(instance):
    instance_state = instance.state['Name']
    return instance_state == 'running'

# To get our running and non-running instances separately
def get_existing_instances():
    instances = conn.instances.filter()
    running_instances_ids = [instance.id for instance in instances if instance_is_running(instance)]
    not_running_instances_ids = [instance.id for instance in instances if not instance_is_running(instance)]
    return running_instances_ids, not_running_instances_ids

# To create a new instance
def create_new_instance():

    instances = client.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=[
            security_group_id
        ],
    )

    # Fetching the instance ID
    instance_id = instances['Instances'][0]['InstanceId']
    print(f"EC2 Instance with ID {instance_id} has been created.")

    return instance_id
