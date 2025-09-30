#!/usr/bin/env python3
"""
Sample Email Templates
Pre-built email templates for common use cases.
"""

from email_automation import EmailAutomation

def create_sample_templates():
    """Create sample email templates in the database."""
    automation = EmailAutomation()
    
    # Welcome Email Template
    welcome_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Welcome to Our Service</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #4CAF50; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f9f9f9; }
            .footer { background-color: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }
            .button { background-color: #4CAF50; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Our Service!</h1>
            </div>
            <div class="content">
                <h2>Hello {{first_name}},</h2>
                <p>Thank you for joining our service! We're excited to have you on board.</p>
                <p>Here's what you can expect:</p>
                <ul>
                    <li>24/7 customer support</li>
                    <li>Regular updates and new features</li>
                    <li>Exclusive member benefits</li>
                </ul>
                <p>If you have any questions, feel free to reach out to our support team.</p>
                <p style="text-align: center;">
                    <a href="#" class="button">Get Started</a>
                </p>
            </div>
            <div class="footer">
                <p>© 2024 Your Company. All rights reserved.</p>
                <p>You received this email because you signed up for our service.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    welcome_text = """
    Welcome to Our Service!
    
    Hello {{first_name}},
    
    Thank you for joining our service! We're excited to have you on board.
    
    Here's what you can expect:
    - 24/7 customer support
    - Regular updates and new features
    - Exclusive member benefits
    
    If you have any questions, feel free to reach out to our support team.
    
    Best regards,
    The Team
    """
    
    automation.create_email_template(
        name="welcome_email",
        subject="Welcome to Our Service, {{first_name}}!",
        body_html=welcome_html,
        body_text=welcome_text
    )
    
    # Newsletter Template
    newsletter_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Monthly Newsletter</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #2196F3; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f9f9f9; }
            .article { margin-bottom: 20px; padding: 15px; background-color: white; border-radius: 5px; }
            .footer { background-color: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Monthly Newsletter</h1>
                <p>Stay updated with our latest news and features</p>
            </div>
            <div class="content">
                <h2>Hello {{first_name}},</h2>
                <p>Here's what's new this month:</p>
                
                <div class="article">
                    <h3>🚀 New Feature Release</h3>
                    <p>We've launched an exciting new feature that will make your experience even better. Check it out in your dashboard!</p>
                </div>
                
                <div class="article">
                    <h3>📊 Monthly Statistics</h3>
                    <p>This month, we've helped over 10,000 customers achieve their goals. Thank you for being part of our community!</p>
                </div>
                
                <div class="article">
                    <h3>💡 Pro Tip</h3>
                    <p>Did you know you can customize your dashboard to show only the information that matters most to you?</p>
                </div>
                
                <p>Thank you for being a valued customer!</p>
            </div>
            <div class="footer">
                <p>© 2024 Your Company. All rights reserved.</p>
                <p><a href="#" style="color: #4CAF50;">Unsubscribe</a> | <a href="#" style="color: #4CAF50;">Update Preferences</a></p>
            </div>
        </div>
    </body>
    </html>
    """
    
    newsletter_text = """
    Monthly Newsletter
    
    Hello {{first_name}},
    
    Here's what's new this month:
    
    🚀 New Feature Release
    We've launched an exciting new feature that will make your experience even better. Check it out in your dashboard!
    
    📊 Monthly Statistics
    This month, we've helped over 10,000 customers achieve their goals. Thank you for being part of our community!
    
    💡 Pro Tip
    Did you know you can customize your dashboard to show only the information that matters most to you?
    
    Thank you for being a valued customer!
    
    Best regards,
    The Team
    """
    
    automation.create_email_template(
        name="newsletter",
        subject="Monthly Newsletter - {{company}}",
        body_html=newsletter_html,
        body_text=newsletter_text
    )
    
    # Promotional Email Template
    promotional_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Special Offer</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; }
            .content { padding: 20px; background-color: #f9f9f9; }
            .offer { background-color: #ff6b6b; color: white; padding: 20px; text-align: center; border-radius: 10px; margin: 20px 0; }
            .button { background-color: #ff6b6b; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; display: inline-block; font-weight: bold; }
            .footer { background-color: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎉 Special Offer Just for You!</h1>
                <p>Don't miss out on this limited-time deal</p>
            </div>
            <div class="content">
                <h2>Hello {{first_name}},</h2>
                <p>We have an exclusive offer that we think you'll love!</p>
                
                <div class="offer">
                    <h2>30% OFF</h2>
                    <p>Guardbox Pro Plan</p>
                    <p>Valid until the end of this month</p>
                </div>
                
                <p>This special discount is only available to our valued customers like you. Upgrade now and enjoy all premium features at half the price!</p>
                
                <p style="text-align: center;">
                    <a href="#" class="button">Claim Your Discount</a>
                </p>
                
                <p><strong>What you get with Guardbox Pro:</strong></p>
                <ul>
                    <li>Unlimited access to all features</li>
                    <li>Priority customer support</li>
                    <li>Advanced analytics and reporting</li>
                    <li>Custom integrations</li>
                </ul>
                
                <p>Hurry! This offer expires soon.</p>
            </div>
            <div class="footer">
                <p>© 2024 Your Company. All rights reserved.</p>
                <p>This offer is valid for {{first_name}} {{last_name}} only.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    promotional_text = """
    🎉 Special Offer Just for You!
    
    Hello {{first_name}},
    
    We have an exclusive offer that we think you'll love!
    
    30% OFF Guardbox Pro Plan
    Valid until the end of this month
    
    This special discount is only available to our valued customers like you. Upgrade now and enjoy all premium features at half the price!
    
    What you get with Guardbox Pro:
    - Unlimited access to all features
    - Priority customer support
    - Advanced analytics and reporting
    - Custom integrations
    
    Hurry! This offer expires soon.
    
    Best regards,
    The Team
    """
    
    automation.create_email_template(
        name="promotional_offer",
        subject="🎉 Special 30% Off Offer for {{first_name}}!",
        body_html=promotional_html,
        body_text=promotional_text
    )
    
    # Follow-up Email Template
    followup_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Follow-up</title>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #9C27B0; color: white; padding: 20px; text-align: center; }
            .content { padding: 20px; background-color: #f9f9f9; }
            .footer { background-color: #333; color: white; padding: 10px; text-align: center; font-size: 12px; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>How are things going?</h1>
            </div>
            <div class="content">
                <h2>Hello {{first_name}},</h2>
                <p>We hope you're enjoying our service! It's been a while since we last heard from you.</p>
                <p>We'd love to know how things are going and if there's anything we can help you with.</p>
                <p>Here are some ways we can assist you:</p>
                <ul>
                    <li>Answer any questions you might have</li>
                    <li>Help you get the most out of our features</li>
                    <li>Provide personalized recommendations</li>
                </ul>
                <p>Don't hesitate to reach out if you need anything!</p>
                <p>Best regards,<br>Your Support Team</p>
            </div>
            <div class="footer">
                <p>© 2024 Your Company. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    followup_text = """
    How are things going?
    
    Hello {{first_name}},
    
    We hope you're enjoying our service! It's been a while since we last heard from you.
    
    We'd love to know how things are going and if there's anything we can help you with.
    
    Here are some ways we can assist you:
    - Answer any questions you might have
    - Help you get the most out of our features
    - Provide personalized recommendations
    
    Don't hesitate to reach out if you need anything!
    
    Best regards,
    Your Support Team
    """
    
    automation.create_email_template(
        name="follow_up",
        subject="How are things going, {{first_name}}?",
        body_html=followup_html,
        body_text=followup_text
    )
    
    print("✅ Sample email templates created successfully!")
    print("Available templates:")
    print("- welcome_email")
    print("- newsletter")
    print("- promotional_offer")
    print("- follow_up")

if __name__ == "__main__":
    create_sample_templates()
