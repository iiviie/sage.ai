"""
Base configuration settings shared across all environments.
"""
from pydantic_settings import BaseSettings
from typing import Optional, List
from enum import Enum


class Environment(str, Enum):
    """Supported environment types"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class BaseConfig(BaseSettings):
    """
    Base configuration class with settings common to all environments.
    Environment-specific configs will inherit from this.
    """

    # Application Metadata
    APP_NAME: str = "Sage Auth Service"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True

    # Security - JWT Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Google OAuth2 (Common across environments, but URLs will differ)
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_AUTHORIZATION_URL: str = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL: str = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL: str = "https://www.googleapis.com/oauth2/v3/userinfo"

    # CORS - Override in environment-specific configs
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]



    # ENVIRONMENT-SPECIFIC SETTINGS (Override in subclasses)


    # Database
    DATABASE_URL: str

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:3000"

    # OAuth Redirect URI
    GOOGLE_REDIRECT_URI: str

    # AWS Configuration (will differ between LocalStack and real AWS)
    AWS_REGION: str = "us-east-1"
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None

    # S3 Configuration
    S3_BUCKET_NAME: str = "sage-content-bucket"

    # API Gateway
    API_GATEWAY_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields for flexibility


    def get_database_url(self) -> str:
        """
        Returns the database URL for the current environment.
        Override in subclasses for environment-specific logic.
        """
        return self.DATABASE_URL

    def get_s3_endpoint(self) -> Optional[str]:
        """
        Returns S3 endpoint URL.
        Override in subclasses (e.g., LocalStack uses custom endpoint).
        """
        return None

    def get_aws_config(self) -> dict:
        """
        Returns AWS client configuration.
        Override in subclasses for environment-specific settings.
        """
        config = {
            "region_name": self.AWS_REGION,
        }

        if self.AWS_ACCESS_KEY_ID and self.AWS_SECRET_ACCESS_KEY:
            config["aws_access_key_id"] = self.AWS_ACCESS_KEY_ID
            config["aws_secret_access_key"] = self.AWS_SECRET_ACCESS_KEY

        return config
