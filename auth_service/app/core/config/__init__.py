"""
Configuration module for Sage Auth Service.
Automatically loads the correct configuration based on ENVIRONMENT variable.
"""
import os
from typing import Union
from .base import BaseConfig, Environment
from .development import DevelopmentConfig
from .production import ProductionConfig


def get_settings() -> Union[DevelopmentConfig, ProductionConfig]:
    """
    Factory function to load the appropriate configuration based on ENVIRONMENT.

    The ENVIRONMENT variable can be set via:
    1. Environment variable: export ENVIRONMENT=production
    2. .env file: ENVIRONMENT=development
    3. Docker: environment variable in docker-compose.yml

    Returns:
        Configuration instance (DevelopmentConfig or ProductionConfig)

    Raises:
        ValueError: If ENVIRONMENT is not recognized
    """
    # Get environment from ENV var, default to development
    env = os.getenv("ENVIRONMENT", "development").lower()

    config_map = {
        Environment.DEVELOPMENT.value: DevelopmentConfig,
        Environment.PRODUCTION.value: ProductionConfig,
        "dev": DevelopmentConfig,  # Alias
        "prod": ProductionConfig,  # Alias
    }

    config_class = config_map.get(env)

    if config_class is None:
        raise ValueError(
            f"Invalid ENVIRONMENT value: '{env}'. "
            f"Must be one of: {', '.join(config_map.keys())}"
        )

    return config_class()


# Global settings instance - automatically loads correct environment
settings = get_settings()


# Export commonly used classes and functions
__all__ = [
    "settings",
    "get_settings",
    "BaseConfig",
    "DevelopmentConfig",
    "ProductionConfig",
    "Environment",
]
