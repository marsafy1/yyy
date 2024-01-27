import boto3
import os

from dotenv import load_dotenv
from utils import decrypt_password, get_user_input

# Loading the .env file
load_dotenv()

# Getting the keys from .env
access_key = os.getenv('AWS_ACCESS_KEY')
secret_key = os.getenv('AWS_SECRET_KEY')

# Configurations
region_name = 'me-central-1'
ubuntu_ami_id = 'ami-0b98fa71853d8d270' # Ubuntu
windows_ami_id = 'ami-0bdb551a74e682731' # Winshare
ami_id = windows_ami_id # Assigning the AMI Id
instance_type = 't3.micro'
key_pair_name = 'development'
security_group_id = 'sg-0ceff133271f50a36'

# Global Variables
current_instance = None
running_instances_ids = []
not_running_instances_ids = []
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
        KeyName=key_pair_name
    )

    # Fetching the instance ID
    instance_id = instances['Instances'][0]['InstanceId']

    # Initialize waiter
    waiter = client.get_waiter('instance_running')

    # Wait for the instance to be in the running state
    waiter.wait(InstanceIds=[instance_id])

    print(f"EC2 Instance with ID {instance_id} has been created.")

    return instance_id


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
    print(f'User chose {user_choice}')
    return user_choice

# To get the working instance that will be used later
def get_working_instance():
    global running_instances_ids, not_running_instances_ids, running_instance_count

    running_instances_ids, not_running_instances_ids = get_existing_instances()
    running_instance_count = len(running_instances_ids)

    if(running_instance_count > 0):
        user_choice = int(user_choose_instance()) - 1
        return running_instances_ids[user_choice]
    else:
        print('You do not have any instances, will create a new one')
        return create_new_instance()
    
# To get the info about the instance
def get_instance_details_by_id(instance_id):
    response = client.describe_instances(InstanceIds=[instance_id])
    return response

# To extract address Ip
def get_instance_address_ip(instance_details):
    return instance_details['Reservations'][0]['Instances'][0]['NetworkInterfaces'][0]['Association']['PublicIp']

# To get the instance's username
def get_instance_username(instance_id):
    return 'Administrator'

# To get the instance's password
def get_instance_password(instance_id):
    encrypted_password = client.get_password_data(InstanceId=instance_id)['PasswordData']
    return decrypt_password(encrypted_password)