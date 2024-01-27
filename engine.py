import aws_mgmt
from smb import SMB
from utils import extract_sharenames

# Current working instance's ID
instance_id = None

# Main function
def start():
    global instance_id
    instance_id = aws_mgmt.get_working_instance()
    print(f'Will start working on {instance_id}')

if __name__ == '__main__':
    start()
    instance_details = aws_mgmt.get_instance_details_by_id(instance_id)
    instance_ip = aws_mgmt.get_instance_address_ip(instance_details)

    print(f'Instance\'s IP {instance_ip}')

    instance_username = aws_mgmt.get_instance_username(instance_id=instance_id)
    instance_password = aws_mgmt.get_instance_password(instance_id=instance_id)

    smb = SMB(username=instance_username, password=instance_password, ip=instance_ip)

    connection = smb.connect()

    sharenames = extract_sharenames(connection)[1::]

    print(f'Shares on {instance_ip}')
    print(sharenames)