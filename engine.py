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

# Global Variables
current_instance = None
running_instance_count = 0

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

# To get ANY user input. Keep getting input till we get a valid input
def get_user_input(input_message, validate_function):
    user_input =  input(input_message)

    try:
        validate_function(user_input)
    except Exception as e:
        print(e)
        get_user_input(input_message, validate_function)

# To validate the instance choice
def validate_instance_choice(user_choice):
    if(str(user_choice).lower() == 'n'):
        print('Will Create a new instance')
    else:
        user_choice = int(user_choice)
        if(user_choice > running_instance_count or user_choice < 1):
            raise Exception('Invalid number - no such instance')

# To get ready and choose an instance
def user_choose_instance():
    print(f'You have {running_instance_count} instance(s) running')
    user_choice = get_user_input(f'Choose one (1 - {running_instance_count}) or create a new instance(N): ', validate_instance_choice)

# Main starting function
def start():
    global running_instance_count

    running_instances_ids, not_running_instances_ids = get_existing_instances()
    running_instance_count = len(running_instances_ids)

    if(running_instance_count > 0):
        user_choose_instance()
    else:
        print('You do not have any instances, will create a new one')






if __name__ == '__main__':
    start()