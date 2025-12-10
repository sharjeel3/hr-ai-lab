#!/usr/bin/env python3
"""
HR AI Lab - Dashboard Launcher

Quick launcher for all dashboard options.
"""

import sys
import subprocess
from pathlib import Path


def print_header():
    """Print header."""
    print("=" * 80)
    print("HR AI LAB - DASHBOARD LAUNCHER")
    print("=" * 80)
    print()


def print_menu():
    """Print menu options."""
    print("Select dashboard to launch:")
    print()
    print("  1. Generate HTML Dashboard (Static, no dependencies)")
    print("  2. Launch Streamlit Dashboard (Interactive, requires streamlit)")
    print("  3. Open Latest HTML Dashboard")
    print("  4. Generate HTML & Open")
    print("  5. Launch CV Screening Dashboard")
    print("  6. Exit")
    print()


def generate_html():
    """Generate HTML dashboard."""
    print("\n🔄 Generating unified HTML dashboard...")
    script_path = Path(__file__).parent / 'generate_unified_dashboard.py'
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Error generating dashboard: {e}")
        return False


def launch_streamlit():
    """Launch Streamlit dashboard."""
    print("\n🚀 Launching Streamlit dashboard...")
    print("   Dashboard will open in your browser...")
    print("   Press Ctrl+C to stop the server")
    print()
    
    script_path = Path(__file__).parent / 'unified_streamlit_dashboard.py'
    
    try:
        subprocess.run(['streamlit', 'run', str(script_path)])
    except FileNotFoundError:
        print("❌ Streamlit not found!")
        print("   Install with: pip install streamlit plotly pandas")
    except KeyboardInterrupt:
        print("\n✓ Streamlit dashboard stopped")


def open_latest_html():
    """Open most recent HTML dashboard."""
    dashboard_dir = Path(__file__).parent
    html_files = list(dashboard_dir.glob('unified_dashboard_*.html'))
    
    if not html_files:
        print("❌ No HTML dashboards found")
        print("   Generate one first (option 1)")
        return False
    
    latest = max(html_files, key=lambda p: p.stat().st_mtime)
    print(f"\n📊 Opening: {latest.name}")
    
    try:
        subprocess.run(['open', str(latest)])
        return True
    except Exception as e:
        print(f"❌ Error opening dashboard: {e}")
        return False


def launch_cv_screening():
    """Launch CV screening dashboard."""
    print("\n🚀 Launching CV Screening dashboard...")
    script_path = Path(__file__).parent / 'cv_screening_dashboard.py'
    
    if not script_path.exists():
        print("❌ CV screening dashboard not found")
        return False
    
    try:
        subprocess.run(['streamlit', 'run', str(script_path)])
    except FileNotFoundError:
        print("❌ Streamlit not found!")
        print("   Install with: pip install streamlit plotly pandas")
    except KeyboardInterrupt:
        print("\n✓ Dashboard stopped")


def main():
    """Main launcher function."""
    print_header()
    
    while True:
        print_menu()
        
        try:
            choice = input("Enter your choice (1-6): ").strip()
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            sys.exit(0)
        
        print()
        
        if choice == '1':
            generate_html()
            input("\n✓ Press Enter to continue...")
            
        elif choice == '2':
            launch_streamlit()
            
        elif choice == '3':
            open_latest_html()
            input("\n✓ Press Enter to continue...")
            
        elif choice == '4':
            if generate_html():
                open_latest_html()
            input("\n✓ Press Enter to continue...")
            
        elif choice == '5':
            launch_cv_screening()
            
        elif choice == '6':
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please select 1-6.")
            input("Press Enter to continue...")
        
        print()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)
