# Pinterest Data Pipeline Project

## Table of Contents 

## Project Overview

## Batch Processing: configuring the EC2 Kafka client
This section provides a step-by-step guide to configuring the EC2 Kafka client for your data pipeline project.

Before connecting to your EC2 instance, you'll need to create a key pair file locally. Follow these steps:

Navigate to the AWS Parameter Store in your AWS account.
Locate the specific key pair associated with your EC2 instance using your KeyPairId (found in the email containing your AWS login credentials).
Select this key pair and under the Value field, click on "Show" to reveal the content of your key pair. Copy the entire value, including the BEGIN and END headers.
Paste the copied content into a new file in your code editor (e.g., VSCode) with a .pem extension.

To connect to your EC2 instance, follow these steps:

Navigate to the EC2 console.
Identify the EC2 instance with your unique UserId.
Under the "Details" section, find the "Key pair name" and make a note of it.
Save the previously created .pem file in your code editor using the following format: Key pair name.pem.
Follow the connection instructions (SSH client) provided on the EC2 console to connect to your EC2 instance.

Now that you're connected to your EC2 instance, you need to install Kafka and the IAM MSK authentication package.

Installing Kafka:
Install Kafka on your client EC2 machine. Make sure to install the same version of Kafka as the one the MSK cluster is running on (in this case, 2.12-2.8.1).
Installing the IAM MSK Authentication Package:
Install the IAM MSK authentication package on your client EC2 machine. This package is necessary to connect to MSK clusters that require IAM authentication, like the one you have access to.

Before configuring your Kafka client to use AWS IAM for cluster authentication, follow these steps:

In the AWS IAM console, access the "Roles" section from the left-hand sidebar. Locate your access role, and ensure to copy its associated Role ARN for reference. Proceed to the "Trust relationships" tab, and select "Edit trust policy." Here, add a principal by clicking "Add a principal" and choose "IAM roles" as the Principal type. Replace the existing ARN with the access role ARN that you previously copied. This action grants your EC2 instance the necessary permissions to authenticate with the AWS MSK cluster.

Configure the client.properties file in the kafka_folder/bin directory in order to use AWS IAM authentication.

To create Kafka topics, you need specific information about the MSK cluster. Follow these steps:

Retrieve Cluster Information
Retrieve the Bootstrap servers string and the Plaintext Apache Zookeeper connection string from the MSK Management Console. Make a note of these strings.

You will need to create the following three topics with the specified format:

.pin topic for Pinterest posts data
.geo topic  for post geolocation data
.user topic for post user data
Before running any Kafka commands, ensure that your CLASSPATH environment variable is set properly.

In the Kafka create topic command, replace the BootstrapServerString with the value you obtained in the previous step. Please note that you have been granted permission to create topics with the exact names specified above on the MSK cluster. Ensure you follow the correct format to avoid permission errors.

## Batch Processing: connecting MSK cluster to S3 Bucket

## Batch Processing: configuring an API in API Gateway

## Batch Processing: Databricks

## Batch Processing: Spark on Databricks

## Batch Processing: Databricks workloads on AWS MWAA

## Stream Processing: Kinesis stream data and read using Databricks


