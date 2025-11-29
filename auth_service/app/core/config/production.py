"""
Production environment configuration using AWS and Supabase.
"""
from typing import Optional, List
from .base import BaseConfig, Environment


class ProductionConfig(BaseConfig):
    """
    Production environment configuration.
    Uses real AWS services (Lambda, S3, API Gateway) and Supabase for database.
    """

    # PRODUCTION-SPECIFIC OVERRIDES



    ENVIRONMENT: Environment = Environment.PRODUCTION
    DEBUG: bool = False

    # Database - Supabase PostgreSQL
    # Format: postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
    DATABASE_URL: str  # Must be set via environment variable

    # Supabase Configuration
    SUPABASE_URL: str  # e.g., https://xxxxx.supabase.co
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str  # For admin operations

    # Frontend URL - Production domain
    FRONTEND_URL: str  # e.g., https://sage.app

    # OAuth Redirect URI - Production
    GOOGLE_REDIRECT_URI: str  # e.g., https://api.sage.app/api/v1/auth/google/callback

    # CORS - Production origins only
    BACKEND_CORS_ORIGINS: List[str]  # Must be set via environment variable

    # AWS PRODUCTION CONFIGURATION

    # AWS Region
    AWS_REGION: str = "us-east-1"

    # AWS Credentials (use IAM roles in Lambda, or environment variables)
    AWS_ACCESS_KEY_ID: Optional[str] = None  # Not needed if using IAM roles
    AWS_SECRET_ACCESS_KEY: Optional[str] = None  # Not needed if using IAM roles

    # S3 Configuration
    S3_BUCKET_NAME: str  # e.g., sage-prod-content
    S3_CLOUDFRONT_DOMAIN: Optional[str] = None  # If using CloudFront CDN

    # API Gateway URL
    API_GATEWAY_URL: str  # e.g., https://api.sage.app or API Gateway URL

    # Lambda Configuration
    LAMBDA_FUNCTION_NAME: str = "sage-auth-service"

    # CloudWatch Logging
    CLOUDWATCH_LOG_GROUP: str = "/aws/lambda/sage-auth-service"



    # SECURITY & MONITORING



    # Sentry (Error Tracking) - Optional
    SENTRY_DSN: Optional[str] = None

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 60

    # SSL/TLS
    FORCE_HTTPS: bool = True

    class Config:
        env_file = ".env.production"
        case_sensitive = True


    def get_s3_endpoint(self) -> Optional[str]:
        """
        Returns None for production (uses default AWS S3 endpoints).
        If using CloudFront, could return CDN domain here.
        """
        return None

    def get_aws_config(self) -> dict:
        """
        Returns AWS client configuration for production.
        In Lambda, credentials are automatically provided by IAM role.
        """
        config = {
            "region_name": self.AWS_REGION,
        }

        # Only add credentials if explicitly provided
        # (Lambda will use IAM role credentials automatically)
        if self.AWS_ACCESS_KEY_ID and self.AWS_SECRET_ACCESS_KEY:
            config["aws_access_key_id"] = self.AWS_ACCESS_KEY_ID
            config["aws_secret_access_key"] = self.AWS_SECRET_ACCESS_KEY

        return config

    def get_s3_config(self) -> dict:
        """Returns S3-specific boto3 client configuration for production"""
        return self.get_aws_config()

    def get_lambda_config(self) -> dict:
        """Returns Lambda-specific boto3 client configuration for production"""
        return self.get_aws_config()

    def is_localstack(self) -> bool:
        """Helper to check if running in LocalStack mode"""
        return False

    def get_supabase_config(self) -> dict:
        """Returns Supabase configuration for client initialization"""
        return {
            "url": self.SUPABASE_URL,
            "anon_key": self.SUPABASE_ANON_KEY,
            "service_role_key": self.SUPABASE_SERVICE_ROLE_KEY,
        }
