import aws_mgmt
import uuid
from smbprotocol.connection import Connection, Dialects
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect

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
    
    # Create the SMB connection
    connection = Connection(uuid.uuid4(), instance_ip, 445)
    connection.connect(Dialects.SMB_2_0_2)

    # Create the SMB session
    session = Session(connection, '', '')
    session.connect()

    # Retrieve the list of shares
    tree = TreeConnect(session, f"\\\\{instance_ip}\\")
    shares = tree.list_shares()

    for share in shares:
        print(share['share_name'])

    # Clean up the connection
    tree.disconnect()
    session.disconnect()
    connection.disconnect()