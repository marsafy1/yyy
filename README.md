# yyy - AWS Instance Management and Information Gathering

## Overview
This Python project automates the creation and configuration of AWS instances, specifically focusing on Windows servers. It facilitates the setup of security group IDs, retrieves decrypted instance passwords, and gathers information using SMB commands.

## Key Features
- **Instance Creation and Configuration**: Automate the deployment of AWS instances with custom configurations.
- **Security Group Management**: Dynamically set up and modify AWS security group IDs.
- **Password Retrieval**: Automatically retrieve and decrypt Windows server instance passwords.
- **SMB Integration**: Use SMB commands in Python to collect information from the configured Windows server.

## Main Libraries Used
- `boto3`: Used for interacting with the Amazon Web Services (AWS) API.
- `subprocess`: Utilized for executing SMB commands within Python.
- `pycrypto`: Employed for decryption of AWS instance passwords.

## Getting Started
To get started with this project, ensure you have Python installed along with the required libraries:

```bash
pip install boto3 pycrypto


## Todo
1. Add names to functions' parameters
2. Proper Doc