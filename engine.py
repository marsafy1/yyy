import aws_mgmt

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
    print(instance_ip)