"""
HRIS Data Quality Agent (Experiment G)

AI-powered data quality assessment and improvement for HRIS systems.

This module provides tools for:
- Detecting data quality issues (missing, inconsistent, invalid data)
- Validating business rules and referential integrity
- Generating comprehensive quality reports
- Creating automated data cleansing scripts
- Tracking quality metrics over time
"""

from .hris_data_quality_agent import (
    HRISDataQualityAgent,
    QualityIssueType,
    Severity,
    QualityIssue,
    QualityReport,
)

__version__ = "1.0.0"
__author__ = "HR AI Lab"
__all__ = [
    "HRISDataQualityAgent",
    "QualityIssueType",
    "Severity",
    "QualityIssue",
    "QualityReport",
]
