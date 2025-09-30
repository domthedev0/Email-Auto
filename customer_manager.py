#!/usr/bin/env python3
"""
Customer Management CLI Tool
Interactive tool for managing customers and email templates.
"""

import json
import csv
import sys
from email_automation import EmailAutomation
from datetime import datetime

class CustomerManager:
    def __init__(self):
        self.automation = EmailAutomation()
    
    def show_menu(self):
        """Display the main menu."""
        print("\n" + "="*50)
        print("EMAIL AUTOMATION - CUSTOMER MANAGER")
        print("="*50)
        print("1. Add Customer")
        print("2. Import Customers")
        print("3. View All Customers")
        print("4. Search Customers")
        print("5. Update Customer")
        print("6. Delete Customer")
        print("7. Create Email Template")
        print("8. View Email Templates")
        print("9. Send Test Email")
        print("10. Send Bulk Emails")
        print("11. Schedule Email Campaign")
        print("12. View Statistics")
        print("13. Export Customers to CSV")
        print("14. Database Management")
        print("15. Customer Management (Bulk)")
        print("0. Exit")
        print("="*50)
    
    def add_customer(self):
        """Add a new customer interactively."""
        print("\n--- ADD NEW CUSTOMER ---")
        
        email = input("Email address: ").strip()
        if not email:
            print("Email is required!")
            return
        
        first_name = input("First name (optional): ").strip()
        last_name = input("Last name (optional): ").strip()
        company = input("Company (optional): ").strip()
        phone = input("Phone (optional): ").strip()
        status = input("Status (active/inactive, default: active): ").strip() or "active"
        
        if self.automation.add_customer(email, first_name, last_name, company, phone, status):
            print(f"✅ Customer {email} added successfully!")
        else:
            print(f"❌ Failed to add customer {email}")
    
    def import_customers_csv(self):
        """Import customers from CSV file."""
        print("\n--- IMPORT CUSTOMERS FROM CSV ---")
        
        csv_file = input("CSV file path: ").strip()
        if not csv_file:
            print("CSV file path is required!")
            return
        
        try:
            count = self.automation.import_customers_csv(csv_file)
            print(f"✅ Successfully imported {count} customers from {csv_file}")
        except Exception as e:
            print(f"❌ Error importing CSV: {str(e)}")
    
    def view_customers(self):
        """View all customers."""
        print("\n--- ALL CUSTOMERS ---")
        
        customers = self.automation.get_customers()
        if not customers:
            print("No customers found.")
            return
        
        print(f"{'ID':<5} {'Email':<30} {'Name':<25} {'Company':<20} {'Status':<10}")
        print("-" * 90)
        
        for customer in customers:
            name = f"{customer['first_name']} {customer['last_name']}".strip()
            print(f"{customer['id']:<5} {customer['email']:<30} {name:<25} {customer['company']:<20} {customer['status']:<10}")
    
    def search_customers(self):
        """Search customers by email or name."""
        print("\n--- SEARCH CUSTOMERS ---")
        
        search_term = input("Search term (email or name): ").strip().lower()
        if not search_term:
            print("Search term is required!")
            return
        
        customers = self.automation.get_customers()
        results = []
        
        for customer in customers:
            if (search_term in customer['email'].lower() or 
                search_term in customer['first_name'].lower() or 
                search_term in customer['last_name'].lower() or
                search_term in customer['company'].lower()):
                results.append(customer)
        
        if not results:
            print("No customers found matching your search.")
            return
        
        print(f"\nFound {len(results)} customer(s):")
        print(f"{'ID':<5} {'Email':<30} {'Name':<25} {'Company':<20} {'Status':<10}")
        print("-" * 90)
        
        for customer in results:
            name = f"{customer['first_name']} {customer['last_name']}".strip()
            print(f"{customer['id']:<5} {customer['email']:<30} {name:<25} {customer['company']:<20} {customer['status']:<10}")
    
    def create_email_template(self):
        """Create a new email template."""
        print("\n--- CREATE EMAIL TEMPLATE ---")
        
        name = input("Template name: ").strip()
        if not name:
            print("Template name is required!")
            return
        
        subject = input("Email subject: ").strip()
        if not subject:
            print("Email subject is required!")
            return
        
        print("\nEmail body (HTML) - Press Enter twice when done:")
        html_lines = []
        while True:
            line = input()
            if line == "" and len(html_lines) > 0 and html_lines[-1] == "":
                break
            html_lines.append(line)
        
        body_html = "\n".join(html_lines[:-1])  # Remove the last empty line
        
        print("\nEmail body (Text) - Press Enter twice when done:")
        text_lines = []
        while True:
            line = input()
            if line == "" and len(text_lines) > 0 and text_lines[-1] == "":
                break
            text_lines.append(line)
        
        body_text = "\n".join(text_lines[:-1])  # Remove the last empty line
        
        if self.automation.create_email_template(name, subject, body_html, body_text):
            print(f"✅ Email template '{name}' created successfully!")
        else:
            print(f"❌ Failed to create email template '{name}'")
    
    def view_templates(self):
        """View all email templates."""
        print("\n--- EMAIL TEMPLATES ---")
        
        import sqlite3
        conn = sqlite3.connect(self.automation.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM email_templates")
        templates = cursor.fetchall()
        conn.close()
        
        if not templates:
            print("No email templates found.")
            return
        
        for template in templates:
            template_id, name, subject, body_html, body_text, created_at = template
            print(f"\nID: {template_id}")
            print(f"Name: {name}")
            print(f"Subject: {subject}")
            print(f"Created: {created_at}")
            print("-" * 40)
    
    def send_test_email(self):
        """Send a test email."""
        print("\n--- SEND TEST EMAIL ---")
        
        to_email = input("Recipient email: ").strip()
        if not to_email:
            print("Recipient email is required!")
            return
        
        subject = input("Subject: ").strip()
        if not subject:
            print("Subject is required!")
            return
        
        print("Email body (HTML) - Press Enter twice when done:")
        html_lines = []
        while True:
            line = input()
            if line == "" and len(html_lines) > 0 and html_lines[-1] == "":
                break
            html_lines.append(line)
        
        body_html = "\n".join(html_lines[:-1])
        
        if self.automation.send_email(to_email, subject, body_html=body_html):
            print(f"✅ Test email sent successfully to {to_email}!")
        else:
            print(f"❌ Failed to send test email to {to_email}")
    
    def send_bulk_emails(self):
        """Send bulk emails using a template."""
        print("\n--- SEND BULK EMAILS ---")
        
        # Get available templates
        import sqlite3
        conn = sqlite3.connect(self.automation.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM email_templates")
        templates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not templates:
            print("No email templates found. Please create a template first.")
            return
        
        print("Available templates:")
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template}")
        
        try:
            choice = int(input("Select template (number): ")) - 1
            if 0 <= choice < len(templates):
                template_name = templates[choice]
            else:
                print("Invalid selection!")
                return
        except ValueError:
            print("Invalid input!")
            return
        
        customer_filter = input("Customer filter (active/inactive, default: active): ").strip() or "active"
        
        try:
            limit = input("Limit number of emails (optional): ").strip()
            limit = int(limit) if limit else None
        except ValueError:
            print("Invalid limit, sending to all customers")
            limit = None
        
        print(f"\nSending bulk emails using template '{template_name}'...")
        result = self.automation.send_bulk_emails(template_name, customer_filter, limit)
        print(f"✅ Bulk email completed: {result['sent']} sent, {result['failed']} failed")
    
    def schedule_campaign(self):
        """Schedule an email campaign."""
        print("\n--- SCHEDULE EMAIL CAMPAIGN ---")
        
        campaign_name = input("Campaign name: ").strip()
        if not campaign_name:
            print("Campaign name is required!")
            return
        
        # Get available templates
        import sqlite3
        conn = sqlite3.connect(self.automation.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM email_templates")
        templates = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        if not templates:
            print("No email templates found. Please create a template first.")
            return
        
        print("Available templates:")
        for i, template in enumerate(templates, 1):
            print(f"{i}. {template}")
        
        try:
            choice = int(input("Select template (number): ")) - 1
            if 0 <= choice < len(templates):
                template_name = templates[choice]
            else:
                print("Invalid selection!")
                return
        except ValueError:
            print("Invalid input!")
            return
        
        print("\nScheduling options:")
        print("1. Send now")
        print("2. Schedule for later")
        
        schedule_choice = input("Choose option (1-2): ").strip()
        
        if schedule_choice == "1":
            scheduled_time = datetime.now().isoformat()
        elif schedule_choice == "2":
            scheduled_time = input("Enter scheduled time (YYYY-MM-DD HH:MM): ").strip()
            try:
                # Validate datetime format
                datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M")
                scheduled_time = datetime.strptime(scheduled_time, "%Y-%m-%d %H:%M").isoformat()
            except ValueError:
                print("Invalid datetime format!")
                return
        else:
            print("Invalid choice!")
            return
        
        customer_filter = input("Customer filter (active/inactive, default: active): ").strip() or "active"
        
        if self.automation.schedule_email_campaign(campaign_name, template_name, scheduled_time, customer_filter):
            print(f"✅ Campaign '{campaign_name}' scheduled successfully!")
        else:
            print(f"❌ Failed to schedule campaign '{campaign_name}'")
    
    def view_statistics(self):
        """View email automation statistics."""
        print("\n--- EMAIL AUTOMATION STATISTICS ---")
        
        stats = self.automation.get_statistics()
        
        print(f"Total Customers: {stats['total_customers']}")
        print(f"Active Customers: {stats['active_customers']}")
        print(f"Total Emails Sent: {stats['total_emails_sent']}")
        print(f"Email Templates: {stats['total_templates']}")
        print(f"Email Campaigns: {stats['total_campaigns']}")
    
    def export_customers_csv(self):
        """Export customers to CSV file."""
        print("\n--- EXPORT CUSTOMERS TO CSV ---")
        
        filename = input("CSV filename (default: customers_export.csv): ").strip() or "customers_export.csv"
        
        customers = self.automation.get_customers()
        
        if not customers:
            print("No customers to export.")
            return
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                fieldnames = ['id', 'email', 'first_name', 'last_name', 'company', 'phone', 'status', 'created_at', 'last_email_sent', 'email_count']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(customers)
            
            print(f"✅ Exported {len(customers)} customers to {filename}")
        except Exception as e:
            print(f"❌ Error exporting customers: {str(e)}")

    def database_management_menu(self):
        """Submenu for database management tasks."""
        while True:
            print("\n--- DATABASE MANAGEMENT ---")
            print("1. Backup database")
            print("2. Restore database")
            print("3. Vacuum database")
            print("4. Integrity check")
            print("5. List tables")
            print("6. Export table to CSV")
            print("0. Back")
            sub = input("Choose (0-6): ").strip()
            if sub == "0":
                break
            elif sub == "1":
                path = input("Backup file path (e.g., customers.backup.db): ").strip()
                if not path:
                    print("Path required.")
                else:
                    ok = self.automation.backup_database(path)
                    print("✅ Backup created." if ok else "❌ Backup failed.")
            elif sub == "2":
                path = input("Restore from file path: ").strip()
                if not path:
                    print("Path required.")
                else:
                    confirm = input("Type 'RESTORE' to confirm restore (overwrites current DB): ").strip()
                    if confirm == "RESTORE":
                        ok = self.automation.restore_database(path)
                        print("✅ Database restored." if ok else "❌ Restore failed.")
                    else:
                        print("Restore cancelled.")
            elif sub == "3":
                ok = self.automation.vacuum_database()
                print("✅ Vacuum completed." if ok else "❌ Vacuum failed.")
            elif sub == "4":
                ok = self.automation.check_database_integrity()
                print("✅ Integrity OK." if ok else "❌ Integrity check failed. See logs.")
            elif sub == "5":
                tables = self.automation.list_tables()
                if not tables:
                    print("No tables found.")
                else:
                    print("Tables:")
                    for t in tables:
                        print(f"- {t}")
            elif sub == "6":
                
                table = input("Table name to export: ").strip()
                if not table:
                    print("Table name required.")
                    continue
                out = input("Output CSV file (e.g., export.csv): ").strip()
                if not out:
                    print("Output path required.")
                    continue
                ok = self.automation.export_table_csv(table, out)
                print("✅ Exported." if ok else "❌ Export failed.")
            else:
                print("Invalid choice.")

    def customer_bulk_menu(self):
        """Submenu for bulk customer operations (delete/add)."""
        while True:
            print("\n--- CUSTOMER MANAGEMENT (BULK) ---")
            print("1. Bulk delete by status (active/inactive)")
            print("2. Bulk delete by email domain (e.g., example.com)")
            print("3. Bulk delete by IDs (comma-separated)")
            print("4. Bulk delete by emails (comma-separated)")
            print("5. Bulk delete from CSV (column: email or id)")
            print("6. Bulk add customers from CSV")
            print("0. Back")
            sub = input("Choose (0-6): ").strip()
            if sub == "0":
                break
            elif sub == "1":
                status = input("Status to delete (active/inactive): ").strip() or "active"
                confirm = input(f"Type 'DELETE' to delete all with status '{status}': ").strip()
                if confirm == "DELETE":
                    n = self.automation.delete_customers_by_status(status)
                    print(f"✅ Deleted {n} customers with status '{status}'.")
                else:
                    print("Cancelled.")
            elif sub == "2":
                domain = input("Domain (e.g., example.com): ").strip()
                if not domain:
                    print("Domain required.")
                    continue
                confirm = input(f"Type 'DELETE' to delete all with domain '{domain}': ").strip()
                if confirm == "DELETE":
                    n = self.automation.delete_customers_by_domain(domain)
                    print(f"✅ Deleted {n} customers with domain '{domain}'.")
                else:
                    print("Cancelled.")
            elif sub == "3":
                ids_raw = input("IDs comma-separated: ").strip()
                if not ids_raw:
                    print("IDs required.")
                    continue
                try:
                    ids = [int(x) for x in ids_raw.split(',') if x.strip().isdigit()]
                except Exception:
                    print("Invalid IDs.")
                    continue
                confirm = input(f"Type 'DELETE' to delete {len(ids)} customers: ").strip()
                if confirm == "DELETE":
                    n = self.automation.delete_customers_by_ids(ids)
                    print(f"✅ Deleted {n} customers.")
                else:
                    print("Cancelled.")
            elif sub == "4":
                emails_raw = input("Emails comma-separated: ").strip()
                emails = [e.strip() for e in emails_raw.split(',') if e.strip()]
                if not emails:
                    print("Emails required.")
                    continue
                confirm = input(f"Type 'DELETE' to delete {len(emails)} customers: ").strip()
                if confirm == "DELETE":
                    n = self.automation.delete_customers_by_emails(emails)
                    print(f"✅ Deleted {n} customers.")
                else:
                    print("Cancelled.")
            elif sub == "5":
                path = input("CSV file path: ").strip()
                if not path:
                    print("File required.")
                    continue
                column = input("Column to use (email/id) [email]: ").strip() or "email"
                if column not in ("email", "id"):
                    print("Unsupported column.")
                    continue
                confirm = input("Type 'DELETE' to proceed: ").strip()
                if confirm == "DELETE":
                    n = self.automation.delete_customers_from_csv(path, column=column)
                    print(f"✅ Deleted {n} customers from CSV.")
                else:
                    print("Cancelled.")
            elif sub == "6":
                path = input("CSV file path: ").strip()
                if not path:
                    print("File required.")
                    continue
                n = self.automation.import_customers_csv(path)
                print(f"✅ Imported {n} customers from CSV.")
            else:
                print("Invalid choice.")
    
    def run(self):
        """Run the customer manager CLI."""
        while True:
            self.show_menu()
            choice = input("\nEnter your choice (0-15): ").strip()
            
            if choice == "0":
                print("Goodbye!")
                break
            elif choice == "1":
                self.add_customer()
            elif choice == "2":
                self.import_customers_csv()
            elif choice == "3":
                self.view_customers()
            elif choice == "4":
                self.search_customers()
            elif choice == "5":
                print("Update customer functionality not implemented yet.")
            elif choice == "6":
                ident = input("Enter Customer ID or Email to delete: ").strip()
                if not ident:
                    print("No identifier provided.")
                else:
                    confirm = input(f"Type '0' to confirm deleting '{ident}': ").strip()
                    if confirm == "0":
                        if self.automation.delete_customer(ident):
                            print("✅ Customer deleted.")
                        else:
                            print("❌ Customer not found or deletion failed.")
                    else:
                        print("Deletion cancelled.")
            elif choice == "7":
                self.create_email_template()
            elif choice == "8":
                self.view_templates()
            elif choice == "9":
                self.send_test_email()
            elif choice == "10":
                self.send_bulk_emails()
            elif choice == "11":
                self.schedule_campaign()
            elif choice == "12":
                self.view_statistics()
            elif choice == "13":
                self.export_customers_csv()
            elif choice == "14":
                self.database_management_menu()
            elif choice == "15":
                self.customer_bulk_menu()
            else:
                print("Invalid choice! Please try again.")
            
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    manager = CustomerManager()
    manager.run()
