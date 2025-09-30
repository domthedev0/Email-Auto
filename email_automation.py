#!/usr/bin/env python3
"""
Email Automation System
A comprehensive tool for sending automated emails to customers.
"""

import smtplib
import sqlite3
import json
import schedule
import time
import logging
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Dict, Optional
import os
import csv
import shutil

class EmailAutomation:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the email automation system."""
        self.config = self.load_config(config_file)
        self.setup_logging()
        self.setup_database()
        
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default config if file doesn't exist
            default_config = {
                "smtp": {
                    "server": "smtp.gmail.com",
                    "port": 587,
                    "username": "your_email@gmail.com",
                    "password": "your_app_password",
                    "use_tls": True
                },
                "email_settings": {
                    "from_name": "Your Company",
                    "reply_to": "noreply@yourcompany.com",
                    "max_emails_per_batch": 50,
                    "delay_between_emails": 1
                },
                "database": {
                    "file": "customers.db"
                }
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
    
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('email_automation.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_database(self):
        """Setup SQLite database for customer management."""
        self.db_path = self.config["database"]["file"]
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                first_name TEXT,
                last_name TEXT,
                company TEXT,
                phone TEXT,
                status TEXT DEFAULT 'active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_email_sent TIMESTAMP,
                email_count INTEGER DEFAULT 0
            )
        ''')
        
        # Create email_templates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                subject TEXT NOT NULL,
                body_html TEXT,
                body_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create email_campaigns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS email_campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                template_id INTEGER,
                status TEXT DEFAULT 'draft',
                scheduled_time TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (template_id) REFERENCES email_templates (id)
            )
        ''')
        
        conn.commit()
        conn.close()
        self.logger.info("Database setup completed")
    
    def add_customer(self, email: str, first_name: str = "", last_name: str = "", 
                    company: str = "", phone: str = "", status: str = "active") -> bool:
        """Add a new customer to the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO customers 
                (email, first_name, last_name, company, phone, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (email, first_name, last_name, company, phone, status))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Customer added: {email}")
            return True
        except Exception as e:
            self.logger.error(f"Error adding customer {email}: {str(e)}")
            return False
    
    def import_customers_csv(self, csv_file: str) -> int:
        """Import customers from CSV file."""
        imported_count = 0
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if self.add_customer(
                        email=row.get('email', ''),
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        company=row.get('company', ''),
                        phone=row.get('phone', ''),
                        status=row.get('status', 'active')
                    ):
                        imported_count += 1
        except Exception as e:
            self.logger.error(f"Error importing CSV: {str(e)}")
        
        self.logger.info(f"Imported {imported_count} customers from CSV")
        return imported_count
    
    def create_email_template(self, name: str, subject: str, body_html: str = "", 
                            body_text: str = "") -> bool:
        """Create a new email template."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO email_templates 
                (name, subject, body_html, body_text)
                VALUES (?, ?, ?, ?)
            ''', (name, subject, body_html, body_text))
            
            conn.commit()
            conn.close()
            self.logger.info(f"Email template created: {name}")
            return True
        except Exception as e:
            self.logger.error(f"Error creating template {name}: {str(e)}")
            return False
    
    def get_customers(self, status: str = "active", limit: int = None) -> List[Dict]:
        """Get customers from database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT * FROM customers WHERE status = ?"
        params = [status]
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        columns = [description[0] for description in cursor.description]
        customers = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        conn.close()
        return customers
    
    def delete_customer(self, identifier: str) -> bool:
        """Delete a customer by id or email. Returns True if a row was deleted."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # Determine if identifier is an integer id or an email
            deleted = 0
            if identifier.isdigit():
                cursor.execute("DELETE FROM customers WHERE id = ?", (int(identifier),))
                deleted = cursor.rowcount
            else:
                cursor.execute("DELETE FROM customers WHERE email = ?", (identifier,))
                deleted = cursor.rowcount
            conn.commit()
            conn.close()
            if deleted:
                self.logger.info(f"Customer deleted: {identifier}")
                return True
            else:
                self.logger.warning(f"No customer found for: {identifier}")
                return False
        except Exception as e:
            self.logger.error(f"Error deleting customer {identifier}: {str(e)}")
            return False

    def delete_customers_by_status(self, status: str) -> int:
        """Bulk delete customers by status. Returns number of rows deleted."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE status = ?", (status,))
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            self.logger.info(f"Deleted {deleted} customers with status='{status}'")
            return deleted or 0
        except Exception as e:
            self.logger.error(f"Error bulk deleting by status: {str(e)}")
            return 0

    def delete_customers_by_domain(self, domain: str) -> int:
        """Bulk delete customers whose email ends with the given domain."""
        try:
            if not domain.startswith('@'):
                domain = '@' + domain
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM customers WHERE email LIKE ?", ('%' + domain,))
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            self.logger.info(f"Deleted {deleted} customers with domain '{domain}'")
            return deleted or 0
        except Exception as e:
            self.logger.error(f"Error bulk deleting by domain: {str(e)}")
            return 0

    def delete_customers_by_ids(self, ids: List[int]) -> int:
        """Bulk delete customers by a list of IDs."""
        if not ids:
            return 0
        try:
            placeholders = ','.join(['?'] * len(ids))
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM customers WHERE id IN ({placeholders})", ids)
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            self.logger.info(f"Deleted {deleted} customers by IDs")
            return deleted or 0
        except Exception as e:
            self.logger.error(f"Error bulk deleting by IDs: {str(e)}")
            return 0

    def delete_customers_by_emails(self, emails: List[str]) -> int:
        """Bulk delete customers by a list of emails."""
        if not emails:
            return 0
        try:
            placeholders = ','.join(['?'] * len(emails))
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM customers WHERE email IN ({placeholders})", emails)
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            self.logger.info(f"Deleted {deleted} customers by emails list")
            return deleted or 0
        except Exception as e:
            self.logger.error(f"Error bulk deleting by emails: {str(e)}")
            return 0

    def delete_customers_from_csv(self, csv_file: str, column: str = 'email') -> int:
        """Bulk delete customers using a CSV file column (default 'email')."""
        try:
            values: List[str] = []
            with open(csv_file, 'r', newline='', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                if column not in reader.fieldnames:
                    self.logger.error(f"CSV missing required column: {column}")
                    return 0
                for row in reader:
                    val = row.get(column)
                    if val:
                        values.append(val.strip())
            if not values:
                return 0
            if column == 'email':
                return self.delete_customers_by_emails(values)
            elif column == 'id':
                # Convert to ints when possible
                ids = []
                for v in values:
                    try:
                        ids.append(int(v))
                    except Exception:
                        continue
                return self.delete_customers_by_ids(ids)
            else:
                self.logger.error(f"Unsupported CSV delete column: {column}")
                return 0
        except Exception as e:
            self.logger.error(f"Error bulk deleting from CSV: {str(e)}")
            return 0

    def backup_database(self, backup_file: str) -> bool:
        """Create a file-level backup of the SQLite database."""
        try:
            shutil.copy2(self.db_path, backup_file)
            self.logger.info(f"Database backed up to {backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error backing up database: {str(e)}")
            return False

    def restore_database(self, backup_file: str) -> bool:
        """Restore the SQLite database from a backup file."""
        try:
            if not os.path.isfile(backup_file):
                self.logger.error(f"Backup file not found: {backup_file}")
                return False
            shutil.copy2(backup_file, self.db_path)
            self.logger.info(f"Database restored from {backup_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error restoring database: {str(e)}")
            return False

    def vacuum_database(self) -> bool:
        """Run VACUUM to rebuild and defragment the database file."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("VACUUM")
            conn.commit()
            conn.close()
            self.logger.info("Database vacuum completed")
            return True
        except Exception as e:
            self.logger.error(f"Error vacuuming database: {str(e)}")
            return False

    def check_database_integrity(self) -> bool:
        """Run PRAGMA integrity_check; return True if OK."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check")
            result = cursor.fetchone()
            conn.close()
            ok = bool(result and result[0] == 'ok')
            if ok:
                self.logger.info("Database integrity check: OK")
            else:
                self.logger.warning(f"Database integrity check failed: {result}")
            return ok
        except Exception as e:
            self.logger.error(f"Error running integrity check: {str(e)}")
            return False

    def list_tables(self) -> List[str]:
        """List user tables in the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return tables

    def export_table_csv(self, table_name: str, output_file: str) -> bool:
        """Export an entire table to CSV."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            conn.close()

            with open(output_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columns)
                writer.writerows(rows)
            self.logger.info(f"Exported table '{table_name}' to {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Error exporting table '{table_name}': {str(e)}")
            return False

    def send_email(self, to_email: str, subject: str, body_html: str = "", 
                  body_text: str = "", attachments: List[str] = None) -> bool:
        """Send a single email."""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.config['email_settings']['from_name']} <{self.config['smtp']['username']}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Reply-To'] = self.config['email_settings']['reply_to']
            
            # Add text and HTML parts
            if body_text:
                text_part = MIMEText(body_text, 'plain')
                msg.attach(text_part)
            
            if body_html:
                html_part = MIMEText(body_html, 'html')
                msg.attach(html_part)
            
            # Add attachments if any
            if attachments:
                for file_path in attachments:
                    if os.path.isfile(file_path):
                        with open(file_path, "rb") as attachment:
                            part = MIMEBase('application', 'octet-stream')
                            part.set_payload(attachment.read())
                            encoders.encode_base64(part)
                            part.add_header(
                                'Content-Disposition',
                                f'attachment; filename= {os.path.basename(file_path)}'
                            )
                            msg.attach(part)
            
            # Connect to SMTP server and send email
            server = smtplib.SMTP(self.config['smtp']['server'], self.config['smtp']['port'])
            if self.config['smtp']['use_tls']:
                server.starttls()
            
            server.login(self.config['smtp']['username'], self.config['smtp']['password'])
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error sending email to {to_email}: {str(e)}")
            return False
    
    def send_bulk_emails(self, template_name: str, customer_filter: str = "active", 
                        limit: int = None) -> Dict[str, int]:
        """Send bulk emails using a template."""
        # Get template
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM email_templates WHERE name = ?", (template_name,))
        template = cursor.fetchone()
        conn.close()
        
        if not template:
            self.logger.error(f"Template '{template_name}' not found")
            return {"sent": 0, "failed": 0}
        
        template_id, name, subject, body_html, body_text, created_at = template
        
        # Get customers
        customers = self.get_customers(status=customer_filter, limit=limit)
        
        sent_count = 0
        failed_count = 0
        
        for customer in customers:
            # Personalize email content
            personalized_subject = self.personalize_content(subject, customer)
            personalized_html = self.personalize_content(body_html, customer)
            personalized_text = self.personalize_content(body_text, customer)
            
            # Send email
            if self.send_email(
                to_email=customer['email'],
                subject=personalized_subject,
                body_html=personalized_html,
                body_text=personalized_text
            ):
                sent_count += 1
                # Update customer record
                self.update_customer_email_stats(customer['id'])
            else:
                failed_count += 1
            
            # Delay between emails to avoid spam filters
            time.sleep(self.config['email_settings']['delay_between_emails'])
        
        self.logger.info(f"Bulk email completed: {sent_count} sent, {failed_count} failed")
        return {"sent": sent_count, "failed": failed_count}
    
    def personalize_content(self, content: str, customer: Dict) -> str:
        """Personalize email content with customer data."""
        if not content:
            return content
        
        replacements = {
            '{{first_name}}': customer.get('first_name', ''),
            '{{last_name}}': customer.get('last_name', ''),
            '{{email}}': customer.get('email', ''),
            '{{company}}': customer.get('company', ''),
            '{{phone}}': customer.get('phone', ''),
            '{{full_name}}': f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
        }
        
        personalized_content = content
        for placeholder, value in replacements.items():
            personalized_content = personalized_content.replace(placeholder, value)
        
        return personalized_content
    
    def update_customer_email_stats(self, customer_id: int):
        """Update customer email statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE customers 
            SET last_email_sent = CURRENT_TIMESTAMP, 
                email_count = email_count + 1 
            WHERE id = ?
        ''', (customer_id,))
        conn.commit()
        conn.close()
    
    def schedule_email_campaign(self, campaign_name: str, template_name: str, 
                              scheduled_time: str, customer_filter: str = "active") -> bool:
        """Schedule an email campaign."""
        try:
            # Get template ID
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM email_templates WHERE name = ?", (template_name,))
            template_result = cursor.fetchone()
            
            if not template_result:
                self.logger.error(f"Template '{template_name}' not found")
                return False
            
            template_id = template_result[0]
            
            # Create campaign
            cursor.execute('''
                INSERT INTO email_campaigns 
                (name, template_id, scheduled_time, status)
                VALUES (?, ?, ?, ?)
            ''', (campaign_name, template_id, scheduled_time, 'scheduled'))
            
            conn.commit()
            conn.close()
            
            self.logger.info(f"Campaign '{campaign_name}' scheduled for {scheduled_time}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error scheduling campaign: {str(e)}")
            return False
    
    def run_scheduled_campaigns(self):
        """Run all scheduled campaigns that are due."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get campaigns that are due
        cursor.execute('''
            SELECT c.*, t.name as template_name, t.subject, t.body_html, t.body_text
            FROM email_campaigns c
            JOIN email_templates t ON c.template_id = t.id
            WHERE c.status = 'scheduled' AND c.scheduled_time <= ?
        ''', (datetime.now().isoformat(),))
        
        campaigns = cursor.fetchall()
        
        for campaign in campaigns:
            campaign_id, name, template_id, status, scheduled_time, created_at, template_name, subject, body_html, body_text = campaign
            
            self.logger.info(f"Running scheduled campaign: {name}")
            
            # Send bulk emails
            result = self.send_bulk_emails(template_name)
            
            # Update campaign status
            cursor.execute('''
                UPDATE email_campaigns 
                SET status = 'completed' 
                WHERE id = ?
            ''', (campaign_id,))
            
            conn.commit()
        
        conn.close()
    
    def get_statistics(self) -> Dict:
        """Get email automation statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        # Active customers
        cursor.execute("SELECT COUNT(*) FROM customers WHERE status = 'active'")
        active_customers = cursor.fetchone()[0]
        
        # Total emails sent
        cursor.execute("SELECT SUM(email_count) FROM customers")
        total_emails = cursor.fetchone()[0] or 0
        
        # Templates count
        cursor.execute("SELECT COUNT(*) FROM email_templates")
        total_templates = cursor.fetchone()[0]
        
        # Campaigns count
        cursor.execute("SELECT COUNT(*) FROM email_campaigns")
        total_campaigns = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_customers": total_customers,
            "active_customers": active_customers,
            "total_emails_sent": total_emails,
            "total_templates": total_templates,
            "total_campaigns": total_campaigns
        }

def main():
    """Main function to run the email automation system."""
    automation = EmailAutomation()
    
    # Schedule the campaign runner to run every minute
    schedule.every(1).minutes.do(automation.run_scheduled_campaigns)
    
    print("Email Automation System Started")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nEmail Automation System Stopped")

if __name__ == "__main__":
    main()
