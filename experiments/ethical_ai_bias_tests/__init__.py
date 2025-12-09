"""
Ethical AI Bias Testing Suite (Experiment F)

This package provides an agent-based framework for detecting and measuring
bias in HR AI systems. It can be applied to all other experiments as a
foundational quality assurance tool.

Main Components:
- BiasTestingAgent: Core agent for bias detection
- BiasType: Enumeration of bias types to test
- BiasTestCase: Data structure for test cases
- BiasTestResult: Data structure for test results

Quick Start:
    from experiments.ethical_ai_bias_tests import (
        BiasTestingAgent, BiasType, run_bias_analysis_on_experiment
    )
    
    # Initialize agent
    agent = BiasTestingAgent(config)
    
    # Generate test cases
    test_cases = agent.generate_test_cases(
        original_data=sample_cv,
        bias_types=[BiasType.GENDER, BiasType.ETHNICITY],
        data_type="cv"
    )
    
    # Run tests
    results = agent.run_batch_tests(test_cases, experiment_fn, score_extractor)
    
    # Generate report
    report = agent.generate_bias_report(results)

For detailed documentation, see README.md
"""

from .bias_testing_agent import (
    BiasTestingAgent,
    BiasType,
    BiasTestCase,
    BiasTestResult,
    run_bias_analysis_on_experiment
)

__all__ = [
    'BiasTestingAgent',
    'BiasType',
    'BiasTestCase',
    'BiasTestResult',
    'run_bias_analysis_on_experiment'
]

__version__ = '1.0.0'
