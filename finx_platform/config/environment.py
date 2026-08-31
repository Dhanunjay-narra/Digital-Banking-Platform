"""Environment Management and Profile helpers."""

from enum import Enum
from finx_platform.config.settings import settings


class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


def is_production() -> bool:
    return settings.ENVIRONMENT == EnvironmentType.PRODUCTION


def is_testing() -> bool:
    return settings.ENVIRONMENT == EnvironmentType.TESTING
