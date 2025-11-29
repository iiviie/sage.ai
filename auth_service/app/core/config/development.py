"""
Development environment configuration using LocalStack for AWS services.
"""
from typing import Optional, List
from .base import BaseConfig, Environment


class DevelopmentConfig(BaseConfig):
    """
    Development environment configuration.
    Uses LocalStack to mock AWS services locally.
    """

    # DEVELOPMENT-SPECIFIC OVERRIDES

    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True

    # Database - Local PostgreSQL (via Docker)
    DATABASE_URL: str = "postgresql://sage_user:sage_password@postgres:5432/sage_auth_db"

    # Frontend URL - Local development
    FRONTEND_URL: str = "http://localhost:3000"

    # OAuth Redirect URI - Local
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"

    # CORS - Allow local origins
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]

    # LOCALSTACK CONFIGURATION

    # LocalStack endpoint (all AWS services)
    LOCALSTACK_ENDPOINT: str = "http://localstack:4566"

    # AWS credentials (dummy values for LocalStack)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: str = "test"
    AWS_SECRET_ACCESS_KEY: str = "test"

    # S3 Configuration
    S3_BUCKET_NAME: str = "sage-dev-content"
    S3_ENDPOINT_URL: str = "http://localstack:4566"  # LocalStack S3 endpoint

    # Lambda Configuration
    LAMBDA_ENDPOINT_URL: str = "http://localstack:4566"

    # API Gateway URL (LocalStack)
    API_GATEWAY_URL: str = "http://localstack:4566"

    # DynamoDB (if needed in future)
    DYNAMODB_ENDPOINT_URL: str = "http://localstack:4566"

    # SQS/SNS (if needed in future)
    SQS_ENDPOINT_URL: str = "http://localstack:4566"
    SNS_ENDPOINT_URL: str = "http://localstack:4566"

    class Config:
        env_file = ".env.development"
        case_sensitive = True


    def get_s3_endpoint(self) -> Optional[str]:
        """Returns LocalStack S3 endpoint for development"""
        return self.S3_ENDPOINT_URL

    def get_aws_config(self) -> dict:
        """
        Returns AWS client configuration for LocalStack.
        All AWS SDK clients should use this configuration in development.
        """
        return {
            "region_name": self.AWS_REGION,
            "aws_access_key_id": self.AWS_ACCESS_KEY_ID,
            "aws_secret_access_key": self.AWS_SECRET_ACCESS_KEY,
            "endpoint_url": self.LOCALSTACK_ENDPOINT,
        }

    def get_s3_config(self) -> dict:
        """Returns S3-specific boto3 client configuration"""
        return {
            **self.get_aws_config(),
            "endpoint_url": self.S3_ENDPOINT_URL,
        }

    def get_lambda_config(self) -> dict:
        """Returns Lambda-specific boto3 client configuration"""
        return {
            **self.get_aws_config(),
            "endpoint_url": self.LAMBDA_ENDPOINT_URL,
        }

    def is_localstack(self) -> bool:
        """Helper to check if running in LocalStack mode"""
        return True
