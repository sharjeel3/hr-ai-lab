#!/usr/bin/env python3
"""
Quick script to view interview dashboard in browser
"""

import webbrowser
from pathlib import Path
import sys

def find_latest_dashboard():
    """Find the most recent dashboard file."""
    dashboard_dir = Path("results/dashboards")
    dashboard_files = list(dashboard_dir.glob("interview_dashboard_*.html"))
    
    if not dashboard_files:
        print("❌ No dashboard files found")
        print("Run: python3 experiments/interview_summarisation/generate_dashboard.sh")
        return None
    
    # Sort by modification time, most recent first
    latest = max(dashboard_files, key=lambda p: p.stat().st_mtime)
    return latest

def main():
    """Open the latest dashboard in browser."""
    dashboard_path = find_latest_dashboard()
    
    if not dashboard_path:
        sys.exit(1)
    
    print(f"📊 Opening dashboard: {dashboard_path.name}")
    print(f"📂 Location: {dashboard_path.absolute()}")
    
    # Open in browser
    webbrowser.open(f"file://{dashboard_path.absolute()}")
    
    print("\n✅ Dashboard opened in browser!")
    print("\nTip: To generate a new dashboard, run:")
    print("  ./experiments/interview_summarisation/generate_dashboard.sh")

if __name__ == "__main__":
    main()
