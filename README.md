# Email Automation System

A comprehensive Python-based email automation system for sending personalized emails to customers. This system includes customer management, email templates, scheduling, and bulk email capabilities.

## Features

- 📧 **Email Management**: Send individual or bulk emails with HTML and text support
- 👥 **Customer Database**: SQLite-based customer management with import/export capabilities
- 📝 **Email Templates**: Create and manage reusable email templates with personalization
- ⏰ **Scheduling**: Schedule email campaigns for future delivery
- 📊 **Statistics**: Track email performance and customer engagement
- 🎨 **HTML Templates**: Beautiful, responsive email templates
- 🔧 **CLI Interface**: Easy-to-use command-line interface for management
- 📈 **Bulk Operations**: Import customers from CSV, send bulk emails
- 🔒 **SMTP Support**: Works with Gmail, Outlook, and other SMTP providers

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd email-auto

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Edit `config.json` with your email settings:

```json
{
    "smtp": {
        "server": "smtp.gmail.com",
        "port": 587,
        "username": "your_email@gmail.com",
        "password": "your_app_password",
        "use_tls": true
    },
    "email_settings": {
        "from_name": "Your Company",
        "reply_to": "noreply@yourcompany.com",
        "max_emails_per_batch": 50,
        "delay_between_emails": 1
    }
}
```

### 3. Gmail Setup (Recommended)

For Gmail, you'll need to:
1. Enable 2-Factor Authentication
2. Generate an App Password
3. Use the App Password in the config file

### 4. Run the System

```bash
# Start the customer management interface
python customer_manager.py

# Or run the automation system directly
python email_automation.py
```

## Usage

### Customer Management

Run the customer manager to interact with the system:

```bash
python customer_manager.py
```

**Main Menu Options:**
1. **Add Customer** - Add individual customers
2. **Import Customers from CSV** - Bulk import from CSV file
3. **View All Customers** - List all customers in database
4. **Search Customers** - Find customers by name or email
5. **Create Email Template** - Design email templates
6. **View Email Templates** - List available templates
7. **Send Test Email** - Send a test email
8. **Send Bulk Emails** - Send emails to multiple customers
9. **Schedule Email Campaign** - Schedule future email campaigns
10. **View Statistics** - See email performance metrics
11. **Export Customers to CSV** - Export customer data

### Email Templates

The system supports both HTML and text email templates with personalization:

**Available Placeholders:**
- `{{first_name}}` - Customer's first name
- `{{last_name}}` - Customer's last name
- `{{email}}` - Customer's email address
- `{{company}}` - Customer's company
- `{{phone}}` - Customer's phone number
- `{{full_name}}` - Customer's full name

**Sample Template:**
```html
<h1>Hello {{first_name}}!</h1>
<p>Welcome to {{company}}. We're excited to have you on board.</p>
<p>Your email: {{email}}</p>
```

### Sample Data

The system includes sample templates and customer data:

```bash
# Create sample email templates
python sample_templates.py

# Sample customer data is in sample_customers.csv
```

## File Structure

```
email-auto/
├── email_automation.py      # Main automation system
├── customer_manager.py      # CLI management interface
├── sample_templates.py      # Sample email templates
├── config.json             # Configuration file
├── requirements.txt        # Python dependencies
├── sample_customers.csv    # Sample customer data
├── customers.db            # SQLite database (created automatically)
├── email_automation.log    # System logs
└── README.md              # This file
```

## Database Schema

### Customers Table
- `id` - Primary key
- `email` - Customer email (unique)
- `first_name` - Customer first name
- `last_name` - Customer last name
- `company` - Company name
- `phone` - Phone number
- `status` - active/inactive
- `created_at` - Creation timestamp
- `last_email_sent` - Last email timestamp
- `email_count` - Number of emails sent

### Email Templates Table
- `id` - Primary key
- `name` - Template name (unique)
- `subject` - Email subject line
- `body_html` - HTML email body
- `body_text` - Text email body
- `created_at` - Creation timestamp

### Email Campaigns Table
- `id` - Primary key
- `name` - Campaign name
- `template_id` - Reference to email template
- `status` - draft/scheduled/completed
- `scheduled_time` - When to send
- `created_at` - Creation timestamp

## Advanced Usage

### Custom SMTP Providers

The system works with any SMTP provider. Update `config.json`:

```json
{
    "smtp": {
        "server": "smtp.yourprovider.com",
        "port": 587,
        "username": "your_email@domain.com",
        "password": "your_password",
        "use_tls": true
    }
}
```

### Bulk Email Limits

Configure email sending limits in `config.json`:

```json
{
    "email_settings": {
        "max_emails_per_batch": 100,
        "delay_between_emails": 2
    }
}
```

### Scheduling Campaigns

Schedule campaigns for specific times:

```python
from email_automation import EmailAutomation
from datetime import datetime, timedelta

automation = EmailAutomation()

# Schedule for tomorrow at 9 AM
scheduled_time = (datetime.now() + timedelta(days=1)).replace(hour=9, minute=0)
automation.schedule_email_campaign(
    campaign_name="Weekly Newsletter",
    template_name="newsletter",
    scheduled_time=scheduled_time.isoformat()
)
```

## Troubleshooting

### Common Issues

1. **SMTP Authentication Failed**
   - Check username/password
   - For Gmail, use App Password instead of regular password
   - Ensure 2FA is enabled

2. **Database Errors**
   - Check file permissions
   - Ensure SQLite4 is installed

3. **Email Not Sending**
   - Check SMTP settings
   - Verify recipient email addresses
   - Check spam folder

4. **Template Not Found**
   - Ensure template name is correct
   - Check template exists in database

### Logs

Check `email_automation.log` for detailed error messages and system activity.

## Security Considerations

- Store sensitive configuration in environment variables
- Use App Passwords for email accounts
- Regularly backup the customer database
- Implement rate limiting for bulk emails
- Follow email marketing best practices and regulations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For support and questions:
- Check the troubleshooting section
- Review the logs
- Create an issue in the repository

---

**Happy Email Marketing! 📧✨**

