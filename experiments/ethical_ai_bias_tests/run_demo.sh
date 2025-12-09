#!/bin/bash

# Quick launcher for bias testing demos
# Usage: ./run_demo.sh [quick|live|test]

cd "$(dirname "$0")/../../.."

echo "🔬 Bias Testing Agent - Demo Launcher"
echo "======================================"
echo ""

case "${1:-quick}" in
    quick)
        echo "Running QUICK DEMO (instant results)..."
        echo ""
        python3 experiments/ethical_ai_bias_tests/quick_demo.py
        ;;
    live)
        echo "Running LIVE DEMO (interactive)..."
        echo ""
        python3 experiments/ethical_ai_bias_tests/live_demo.py
        ;;
    test)
        echo "Running UNIT TESTS..."
        echo ""
        python3 experiments/ethical_ai_bias_tests/test_bias_agent.py
        ;;
    examples)
        echo "Running EXAMPLES..."
        echo ""
        python3 experiments/ethical_ai_bias_tests/example_bias_test.py
        ;;
    *)
        echo "Usage: $0 [quick|live|test|examples]"
        echo ""
        echo "Options:"
        echo "  quick     - Quick demo with instant results (default)"
        echo "  live      - Live demo with mock CV screener"
        echo "  test      - Run unit tests"
        echo "  examples  - Run all examples"
        echo ""
        exit 1
        ;;
esac
