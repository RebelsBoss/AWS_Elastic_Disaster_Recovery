import json
import os
import boto3
from botocore.exceptions import ClientError

drs = boto3.client("drs")  # Elastic Disaster Recovery

SOURCE_SERVER_ID = os.getenv("SOURCE_SERVER_ID")
if not SOURCE_SERVER_ID:
    raise RuntimeError(
        "Environment variable SOURCE_SERVER_ID is not set. "
        "Set it in the Lambda configuration (Configuration → Environment variables)."
    )

IS_DRILL = os.getenv("IS_DRILL", "false").lower() == "true"


def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    # 1. If the call via SNS is from CloudWatch Alarm
    try:
        record = event["Records"][0]
        sns_msg = record["Sns"]["Message"]
        print("SNS message:", sns_msg)

        try:
            msg = json.loads(sns_msg)
        except json.JSONDecodeError:
            msg = {}

        state = msg.get("NewStateValue")
        alarm_name = msg.get("AlarmName")

        if state and state != "ALARM":
            print(f"Alarm {alarm_name} is in state {state}, nothing to do.")
            return {
                "status": "ignored",
                "reason": f"Alarm state is {state}, not ALARM",
            }

        print(f"Alarm {alarm_name} is in ALARM state, starting recovery...")

    except (KeyError, IndexError, TypeError):
        # If the call is not from SNS (manual test/direct invoke), we simply proceed.
        print("Non-SNS or direct invocation, proceeding to start recovery")

    # 2. Let's get started DRS recovery job
    try:
        response = drs.start_recovery(
            isDrill=IS_DRILL,
            sourceServers=[{"sourceServerID": SOURCE_SERVER_ID}],
            tags={"startedBy": "cloudwatch-alarm-lambda"},
        )

        job = response.get("job", {})
        job_id = job.get("jobID")

        print("Started DRS recovery job:", json.dumps(job))

        return {
            "status": "started",
            "jobID": job_id,
            "sourceServerID": SOURCE_SERVER_ID,
            "isDrill": IS_DRILL,
        }

    except ClientError as e:
        print("Error starting DRS recovery:", e)
        raise
