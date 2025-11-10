# AWS_Elastic_Disaster_Recovery
### On-prem server → AWS → auto failover
Server recovery from on-premises to the cloud in ~30 minutes.

## Architecture

### On-prem:
- Windows Server
- Installed: AWS Replication Agent (DRS) & Amazon CloudWatch Agent
- VPN/IPsec tunnel in AWS VPC

### AWS (e.g., us-east-1):
- VPC + private subnets
- AWS Elastic Disaster Recovery: Source server (replicating from On-premises → us-east-1a) & Recovery instances (EC2) in case of failover
- CloudWatch: Namespace **CWAgent** with metrics from on-prem agent & Alarm with **treatMissingData = breaching**
- SNS
- Lambda: Function drs-start-recovery, Trigger — SNS (or directly from Alarm) & Calls **drs:StartRecovery** for **SOURCE_SERVER_ID**
