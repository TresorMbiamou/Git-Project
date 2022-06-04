import json
import boto3

code_pipeline = boto3.client("codepipeline")
cloud_front = boto3.client("cloudfront")

def lambda_handler(event, context):
    job_id = event["CodePipeline.job"]["id"]
    try:
        event_data = json.loads(
            event["CodePipeline.job"]
                ["data"]
                ["actionConfiguration"]
                ["configuration"]
                ["UserParameters"]
        )
        cloud_front.create_invalidation(
            DistributionId=event_data["distributionId"],
            InvalidationBatch={
                "Paths": {
                    "Quantity": len(event_data["objectPaths"]),
                    "Items": event_data["objectPaths"],
                },
                "CallerReference": event["CodePipeline.job"]["id"],
            },
        )
    except Exception as e:
        code_pipeline.put_job_failure_result(
            jobId=job_id,
            failureDetails={
                "type": "JobFailed",
                "message": str(e),
            },
                 )
    else:
        code_pipeline.put_job_success_result(
            jobId=job_id,
        )