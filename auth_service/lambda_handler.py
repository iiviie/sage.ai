"""
Lambda handler entry point for AWS Lambda deployment.
This file serves as the entry point specified in Lambda configuration.
"""
from app.main import handler

# AWS Lambda will call this function
# Format: lambda_handler.handler (filename.function_name)
def lambda_handler(event, context):
    """
    AWS Lambda handler function.

    Args:
        event: API Gateway event or direct Lambda invocation event
        context: Lambda context object

    Returns:
        Response formatted for API Gateway or direct invocation
    """
    return handler(event, context)
