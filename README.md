# **AWS_Elastic_Disaster_Recovery**
### **On-prem server → AWS → auto failover**
Server recovery from on-premises to the cloud in ~30 minutes.

## **Short Architecture**

### **On-prem:**
- Windows Server
- Installed: AWS Replication Agent (DRS) **&** Amazon CloudWatch Agent
- VPN/IPsec tunnel in AWS VPC

### **AWS (e.g., us-east-1):**
- VPC + private subnets
- AWS Elastic Disaster Recovery: Source server (replicating from On-premises → us-east-1a) **&** Recovery instances (EC2) in case of failover
- CloudWatch: Namespace **CWAgent** with metrics from on-prem agent **&** Alarm with **treatMissingData = breaching**
- SNS
- Lambda: Function drs-start-recovery, Trigger — SNS (or directly from Alarm) **&** Calls **drs:StartRecovery** for **SOURCE_SERVER_ID**

##




## **Documentation**

- [What is AWS Elastic Disaster Recovery?](https://docs.aws.amazon.com/drs/latest/userguide/what-is-drs.html)   
- [Elastic Disaster Recovery – Getting started](https://docs.aws.amazon.com/drs/latest/userguide/getting-started.html)   
- [Elastic Disaster Recovery – Quick start guide](https://docs.aws.amazon.com/drs/latest/userguide/quick-start-guide-gs.html)   
- [Installing the AWS Replication Agent on Windows](https://docs.aws.amazon.com/drs/latest/userguide/windows-agent.html)   
- [Elastic Disaster Recovery – First time setup / Adding source servers](https://docs.aws.amazon.com/drs/latest/userguide/quick-start-guide-gs.html#drs-quick-start-adding-source-servers)
- [Install the CloudWatch agent on on-premises servers](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/install-CloudWatch-Agent-on-premise.html)
- [Elastic Disaster Recovery initialization and permissions](https://docs.aws.amazon.com/drs/latest/userguide/getting-started-initializing.html)
- [Using Amazon CloudWatch alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [Configuring how CloudWatch alarms treat missing data](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarms-and-missing-data)
- [Create an Amazon SNS topic and publish messages](https://docs.aws.amazon.com/sns/latest/dg/sns-getting-started.html)
- [Notifying users on alarm changes](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Notify_Users_Alarm_Changes.html)
- [Actions, resources, and condition keys for AWS Elastic Disaster Recovery](https://docs.aws.amazon.com/service-authorization/latest/reference/list_awselasticdisasterrecovery.html)
- [StartRecovery](https://docs.aws.amazon.com/drs/latest/APIReference/API_StartRecovery.html)
- [Invoke a Lambda function from an alarm](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/alarms-and-actions-Lambda.html)
- [Why doesn't Amazon SNS invoke my Lambda function when triggered by a CloudWatch alarm?](https://repost.aws/knowledge-center/sns-lambda-function-cloudwatch-alarm)
