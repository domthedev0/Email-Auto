#!/usr/bin/env python3
"""
Setup script for Email Automation System
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def create_sample_data():
    """Create sample templates and import sample customers."""
    print("Creating sample data...")
    try:
        # Import and run sample templates
        from sample_templates import create_sample_templates
        create_sample_templates()
        
        # Import sample customers
        from email_automation import EmailAutomation
        automation = EmailAutomation()
        count = automation.import_customers_csv("sample_customers.csv")
        print(f"✅ Imported {count} sample customers!")
        
        return True
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 50)
    print("EMAIL AUTOMATION SYSTEM SETUP")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed. Please install requirements manually.")
        return
    
    # Create sample data
    create_sample_data()
    
    print("\n" + "=" * 50)
    print("SETUP COMPLETE!")
    print("=" * 50)
    print("Next steps:")
    print("1. Edit config.json with your email settings")
    print("2. Run: python customer_manager.py")
    print("3. Or run: python email_automation.py")
    print("\nFor Gmail users:")
    print("- Enable 2-Factor Authentication")
    print("- Generate an App Password")
    print("- Use the App Password in config.json")
    print("=" * 50)

if __name__ == "__main__":
    main()

