# yyy - AWS Instance Management and Shares Information Gathering

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
To get started with this project, ensure you have Python installed along with the required libraries and configure the .env file with your data:

```bash
pip install -r requirements.txt
```

## Examples
### Running engine without having any existing instances
```
You do not have any instances, will create a new one
EC2 Instance with ID i-yyy has been created.
Created i-yyy
Please wait for 4 minutes before accessing the instance
```
### Running engine and having existing instances
You will be asked to either choose one of the existing instances or create a new one
```
You have 1 instance(s) running
Choose one (1 - 1) or create a new instance(N): 1
User chose 1
Will start working on i-yyy
Instance's IP 3.29.18.22
Shares on 3.29.18.22
[yyy, yyy, yyy]
```
## Todo
1. Add names to functions' parameters
2. Proper Doc
