# Pinterest Data Pipeline Project

## Table of Contents 
- [Project Overview](#project-overview)
- [Batch Processing: Configuring the EC2 Kafka Client](#batch-processing-configuring-the-ec2-kafka-client)
- [Batch Processing: Connecting MSK Cluster to S3 Bucket](#batch-processing-connecting-msk-cluster-to-s3-bucket)
- [Batch Processing: Configuring an API in API Gateway](#batch-processing-configuring-an-api-in-api-gateway)
- [Batch Processing: Databricks](#batch-processing-databricks)
- [Batch Processing: Spark on Databricks](#batch-processing-spark-on-databricks)
- [Batch Processing: Databricks Workloads on AWS MWAA](#batch-processing-databricks-workloads-on-aws-mwaa)
- [Stream Processing: Kinesis Stream Data and Read Using Databricks](#stream-processing-kinesis-stream-data-and-read-using-databricks)


## Project Overview
The Pinterest Data Pipeline project is a comprehensive data engineering initiative designed to streamline the collection, processing, and analysis of data from the Pinterest platform. Leveraging various AWS services and data processing tools, this project aims to create an end-to-end data pipeline that seamlessly handles both batch and stream processing of Pinterest data. Key components include Amazon MSK for stream processing, Amazon S3 for data storage, Databricks for data transformation, AWS MWAA for workflow orchestration, and AWS API Gateway for data ingestion. By setting up Kinesis Data Streams and configuring REST APIs, this project ensures real-time data ingestion and processing. The pipeline also includes data cleaning and storage in Delta Tables, enabling efficient querying and analytics. This project simplifies the complex task of managing Pinterest data, making it accessible and actionable for data-driven insights.

## Batch Processing: Configuring the EC2 Kafka client
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

## Batch Processing: Connecting MSK cluster to S3 Bucket
To set up the connection between your MSK cluster and the designated S3 bucket, follow these steps.

Go to the AWS S3 console and find the S3 bucket you want to connect to the MSK cluster. Take note of this bucket name for subsequent steps.

On your EC2 client, download the Confluent.io Amazon S3 Connector. Copy the downloaded connector to the S3 bucket identified in the previous step.

Access the MSK Connect console.

Create a custom plugin with the name <your_chosen_name>-plugin. Ensure you use this specific name when creating the plugin.

Create a connector with the name <your_chosen_name>-connector. Utilize this name for the connector configuration as well.

Configure the connector with the appropriate settings, specifically, set the bucket name to your S3 bucket.

Pay attention to the topics.regex field in the connector configuration. Ensure it follows the structure: <your_chosen_name>.*. This configuration ensures that data from all three previously created Kafka topics will be saved to the designated S3 bucket.

In the "Access permissions" tab, select the IAM role used for authentication to the MSK cluster. This role contains the necessary permissions to connect to both MSK and MSK Connect.

By following these configurations, data flowing through the IAM-authenticated MSK cluster will be automatically stored in the designated S3 bucket.

## Batch Processing: Configuring an API in API Gateway
This section outlines the steps required to configure your provided API in API Gateway and integrate it with the Kafka REST Proxy, enabling the flow of data from your EC2 client to the MSK Cluster and storage in the S3 bucket. 

Start by creating a resource in API Gateway that allows you to build a PROXY integration for your API.

For the previously created resource, set up an HTTP ANY method. When defining the Endpoint URL, ensure that you copy the correct PublicDNS from the EC2 machine you've been working on in the previous milestones. This EC2 instance should be named after your_chosen_name.

Deploy the API and take note of the Invoke URL, as it will be required for a later task. With the Kafka REST Proxy integration now in place for your API, configure the Kafka REST Proxy on your EC2 client machine.

Start by installing the Confluent package for the Kafka REST Proxy on your EC2 client machine.

Allow the REST proxy to perform IAM authentication to the MSK cluster by modifying the kafka-rest.properties file.

Launch the REST proxy on the EC2 client machine. Now you're prepared to send data to your API, which, in turn, will forward the data to the MSK Cluster using the previously created plugin-connector pair.

Ensure that data from the three tables extracted using the user_posting_emulation.py script is sent to their corresponding Kafka topics.

Verify that data is being sent to the cluster by running a Kafka consumer (one per topic). If everything has been set up correctly, you should observe messages being consumed.

Confirm whether data is being stored in the designated S3 bucket. Take note of the folder organization within the bucket created by your connector.

## Batch Processing: Databricks
In order to process the data from the topics I used Databricks in order to do this you will need to create a Databricks account.

Mount a S3 bucket to Databricks:
In order to do this you will need to create a authentication_credentials.csv that contains a secret access key and access key.

When reading the JSON data from S3 into Databricks, be sure to specify the complete path to the JSON objects, as they appear in your S3 bucket (e.g., topics/<your_chosen_name>.pin/partition=0/).

To organize your data efficiently within Databricks, create three distinct DataFrames:

df_pin for Pinterest post data.
df_geo for geolocation data.
df_user for user data.
This setup will allow you to perform data cleaning and querying effectively within your Databricks environment.

## Batch Processing: Spark on Databricks
Transform the data as shown in my clean_and_analyse_pinterest_data.ipynb file located in this file. Query the data as you see fit, the queries I conducted are shown in this file. 

## Batch Processing: Databricks workloads on AWS MWAA (Managed Workflows for Apache Airflow)
Ensure your AWS account has access to MWAA, along with an associated S3 bucket called mwaa-dags-bucket. create an API token in Databricks to establish a connection with your AWS account and set up the MWAA-Databricks connection. To obtain the Databricks connection type we will need to install the corresponding Python dependency in our MWAA environment, by uploading a requirements.txt file in the MWAA-designated S3 bucket.

All that's required is the creation of an Airflow DAG (Directed Acyclic Graph) that will trigger the execution of a Databricks Notebook on a predefined schedule. Upload this DAG to the dags folder in the mwaa-dags-bucket. Your AWS account has the necessary permissions to upload and update a file named <your_chosen_name_dag.py> to the mwaa-dags-bucket. Ensure that your DAG is named correctly to avoid permission errors.

Lastly, you can manually trigger the DAG you've uploaded in the previous step and verify that it runs successfully. This streamlined setup simplifies the management of your Databricks workloads on AWS MWAA. 

## Stream Processing: Kinesis stream data and read using Databricks
In order to analyse streaming data extracted from Pinterest ensure your AWS account has access to AWS Kinesis. Create 3 distinct Kinesis Data streams, one for each table. 

Configure your previously created REST API to enable Kinesis actions invocation. 

The provided access role takes the form of <your_chosen_name-kinesis-access-role>. You can conveniently obtain its ARN from the IAM console under Roles. Ensure that you use this ARN when setting up the Execution role for the integration points of all the methods you'll create in your API. Your API should be capable of invoking actions like listing streams in Kinesis, creating, describing, and deleting streams, and adding records to streams in Kinesis.

The user_posting_emulation_streaming.py script I created builds upon the upon the user_posting_emulation.py script but sends the Pinterest data to the newly modified API. This API then sends the data to shards in AWS Kinesis. 

The read_and_write_stream_data_to_delta_tables.ipynb file showcases how I read the data into Databricks, cleaned the data in the same way I cleaned the batch processing data previously and wrote the data to delta tables in Databricks. 





