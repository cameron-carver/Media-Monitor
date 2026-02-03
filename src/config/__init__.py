"""Configuration module for Media Monitor."""

from .companies import (
    Company,
    SensitivityProfile,
    NameUniqueness,
    MatchingStrategy,
    COMMON_WORD_PROFILE,
    AMBIGUOUS_NAME_PROFILE,
    MODERATE_PROFILE,
    UNIQUE_NAME_PROFILE,
)
from .company_registry import COMPANY_REGISTRY, get_company, get_all_companies

__all__ = [
    "Company",
    "SensitivityProfile",
    "NameUniqueness",
    "MatchingStrategy",
    "COMMON_WORD_PROFILE",
    "AMBIGUOUS_NAME_PROFILE",
    "MODERATE_PROFILE",
    "UNIQUE_NAME_PROFILE",
    "COMPANY_REGISTRY",
    "get_company",
    "get_all_companies",
]
