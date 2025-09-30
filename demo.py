#!/usr/bin/env python3
"""
Email Automation System Demo
Demonstrates the key features of the email automation system.
"""

from email_automation import EmailAutomation
import time

def demo():
    """Run a demonstration of the email automation system."""
    print("🚀 Email Automation System Demo")
    print("=" * 50)
    
    # Initialize the system
    print("Initializing email automation system...")
    automation = EmailAutomation()
    
    # Create sample templates
    print("\n📝 Creating sample email templates...")
    from sample_templates import create_sample_templates
    create_sample_templates()
    
    # Import sample customers
    print("\n👥 Importing sample customers...")
    count = automation.import_customers_csv("sample_customers.csv")
    print(f"Imported {count} customers")
    
    # Show statistics
    print("\n📊 System Statistics:")
    stats = automation.get_statistics()
    print(f"Total Customers: {stats['total_customers']}")
    print(f"Active Customers: {stats['active_customers']}")
    print(f"Email Templates: {stats['total_templates']}")
    
    # Show available templates
    print("\n📧 Available Email Templates:")
    import sqlite3
    conn = sqlite3.connect(automation.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name, subject FROM email_templates")
    templates = cursor.fetchall()
    conn.close()
    
    for i, (name, subject) in enumerate(templates, 1):
        print(f"{i}. {name}: {subject}")
    
    # Show customers
    print("\n👥 Sample Customers:")
    customers = automation.get_customers(limit=5)
    for customer in customers:
        print(f"- {customer['first_name']} {customer['last_name']} ({customer['email']})")
    
    print("\n" + "=" * 50)
    print("Demo completed! The system is ready to use.")
    print("\nTo get started:")
    print("1. Edit config.json with your email settings")
    print("2. Run: python customer_manager.py")
    print("3. Or run: python email_automation.py")
    print("\nFor Gmail users:")
    print("- Enable 2-Factor Authentication")
    print("- Generate an App Password")
    print("- Use the App Password in config.json")
    print("=" * 50)

if __name__ == "__main__":
    demo()

