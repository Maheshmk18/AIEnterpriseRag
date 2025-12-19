"""
Generate sample department PDFs for testing RAG system
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

# Create test_documents directory
os.makedirs("test_documents", exist_ok=True)

# Department documents content
documents = {
    "HR_Leave_Policy.pdf": {
        "title": "Human Resources - Leave Policy",
        "content": """
        <b>COMPANY LEAVE POLICY</b><br/><br/>
        
        <b>1. Annual Leave</b><br/>
        All full-time employees are entitled to 20 days of paid annual leave per year.
        Leave must be requested at least 2 weeks in advance through the HR portal.
        Unused leave can be carried forward up to 5 days to the next year.<br/><br/>
        
        <b>2. Sick Leave</b><br/>
        Employees receive 10 days of paid sick leave annually.
        Medical certificate required for absences exceeding 3 consecutive days.
        Sick leave cannot be carried forward to the next year.<br/><br/>
        
        <b>3. Maternity/Paternity Leave</b><br/>
        Maternity leave: 16 weeks paid leave
        Paternity leave: 2 weeks paid leave
        Must notify HR at least 1 month before expected date.<br/><br/>
        
        <b>4. Emergency Leave</b><br/>
        Up to 3 days per year for family emergencies.
        Requires manager approval and HR notification within 24 hours.<br/><br/>
        
        <b>Contact HR:</b> hr@company.com for any leave-related queries.
        """
    },
    
    "HR_Onboarding_Guide.pdf": {
        "title": "Employee Onboarding Guide",
        "content": """
        <b>WELCOME TO THE COMPANY!</b><br/><br/>
        
        <b>Week 1: Getting Started</b><br/>
        - Day 1: Orientation session at 9 AM in Conference Room A
        - Complete all paperwork with HR (tax forms, bank details, emergency contacts)
        - Receive company laptop, ID card, and access credentials
        - IT setup and system access configuration<br/><br/>
        
        <b>Week 2-4: Training</b><br/>
        - Attend department-specific training sessions
        - Shadow team members to understand workflows
        - Complete mandatory compliance training modules
        - One-on-one meetings with team lead and manager<br/><br/>
        
        <b>Required Documents:</b><br/>
        - Government-issued ID
        - Educational certificates
        - Previous employment records
        - Bank account details for salary deposit<br/><br/>
        
        <b>Benefits Enrollment:</b><br/>
        Enroll in health insurance, retirement plans within first 30 days.
        """
    },
    
    "Finance_Expense_Policy.pdf": {
        "title": "Finance Department - Expense Reimbursement Policy",
        "content": """
        <b>EXPENSE REIMBURSEMENT POLICY</b><br/><br/>
        
        <b>1. Eligible Expenses</b><br/>
        - Travel expenses (flights, hotels, transportation)
        - Client entertainment and meals
        - Office supplies and equipment
        - Professional development and training
        - Internet and mobile phone bills (partial)<br/><br/>
        
        <b>2. Submission Process</b><br/>
        - Submit expense reports within 30 days of incurring expense
        - Attach original receipts for all claims
        - Use company expense management system
        - Manager approval required for amounts over $500<br/><br/>
        
        <b>3. Reimbursement Timeline</b><br/>
        - Approved expenses processed within 10 business days
        - Payment via direct deposit to registered bank account
        - Monthly expense limit: $2,000 per employee<br/><br/>
        
        <b>4. Travel Expenses</b><br/>
        - Book flights at least 2 weeks in advance for best rates
        - Economy class for domestic, business class for international (8+ hours)
        - Hotel: Maximum $200 per night
        - Meals: $75 per day allowance<br/><br/>
        
        <b>Contact:</b> finance@company.com
        """
    },
    
    "IT_Security_Policy.pdf": {
        "title": "IT Department - Security and Access Policy",
        "content": """
        <b>IT SECURITY POLICY</b><br/><br/>
        
        <b>1. Password Requirements</b><br/>
        - Minimum 12 characters with uppercase, lowercase, numbers, symbols
        - Change password every 90 days
        - No password reuse for last 5 passwords
        - Enable two-factor authentication (2FA) for all systems<br/><br/>
        
        <b>2. Device Security</b><br/>
        - Company laptops must have full disk encryption
        - Install company-approved antivirus software
        - Enable automatic security updates
        - Lock screen when away from desk (auto-lock after 5 minutes)<br/><br/>
        
        <b>3. Data Protection</b><br/>
        - Store sensitive data only on company servers
        - No personal cloud storage (Dropbox, Google Drive) for work files
        - Encrypt all emails containing confidential information
        - Report data breaches immediately to security@company.com<br/><br/>
        
        <b>4. Remote Work</b><br/>
        - Use company VPN for all remote connections
        - Secure home WiFi with WPA3 encryption
        - No public WiFi for accessing company systems
        - Report lost/stolen devices within 2 hours<br/><br/>
        
        <b>IT Support:</b> helpdesk@company.com | Extension: 1234
        """
    },
    
    "Sales_Commission_Structure.pdf": {
        "title": "Sales Department - Commission Structure",
        "content": """
        <b>SALES COMMISSION STRUCTURE 2024</b><br/><br/>
        
        <b>1. Base Commission Rates</b><br/>
        - New customer acquisition: 10% of contract value
        - Existing customer upsell: 7% of additional revenue
        - Renewal deals: 5% of renewal value
        - Referral bonus: $500 per qualified lead that converts<br/><br/>
        
        <b>2. Performance Tiers</b><br/>
        - Bronze (0-80% of quota): Standard commission rates
        - Silver (80-100% of quota): 1.2x commission multiplier
        - Gold (100-120% of quota): 1.5x commission multiplier
        - Platinum (120%+ of quota): 2x commission multiplier + $5,000 bonus<br/><br/>
        
        <b>3. Payment Schedule</b><br/>
        - Commissions calculated monthly
        - Paid on the 15th of following month
        - Annual bonus paid in January for previous year performance<br/><br/>
        
        <b>4. Quarterly Targets</b><br/>
        - Q1: $250,000 revenue target
        - Q2: $300,000 revenue target
        - Q3: $275,000 revenue target
        - Q4: $350,000 revenue target<br/><br/>
        
        <b>Sales Manager:</b> sales.manager@company.com
        """
    },
    
    "Marketing_Brand_Guidelines.pdf": {
        "title": "Marketing - Brand Guidelines",
        "content": """
        <b>BRAND GUIDELINES</b><br/><br/>
        
        <b>1. Logo Usage</b><br/>
        - Primary logo: Full color on white background
        - Secondary logo: White on dark backgrounds
        - Minimum size: 1 inch width for print, 150px for digital
        - Clear space: Maintain 0.5 inch margin around logo
        - Never stretch, rotate, or modify logo colors<br/><br/>
        
        <b>2. Color Palette</b><br/>
        - Primary: Purple #6C63FF
        - Secondary: Blue #7A5AF8
        - Accent: Light Purple #ECEBFF
        - Background: Off-white #F8F7FF
        - Text: Dark Gray #1F2937<br/><br/>
        
        <b>3. Typography</b><br/>
        - Headings: Inter Bold, 24-48pt
        - Body text: Inter Regular, 14-16pt
        - Captions: Inter Light, 12pt<br/><br/>
        
        <b>4. Social Media</b><br/>
        - Post frequency: 3-5 times per week
        - Hashtag strategy: Max 5 relevant hashtags
        - Image dimensions: 1080x1080 for Instagram, 1200x628 for Facebook
        - Tone: Professional yet approachable, helpful, innovative<br/><br/>
        
        <b>Marketing Team:</b> marketing@company.com
        """
    },
    
    "Operations_Remote_Work_Policy.pdf": {
        "title": "Operations - Remote Work Policy",
        "content": """
        <b>REMOTE WORK POLICY</b><br/><br/>
        
        <b>1. Eligibility</b><br/>
        - Employees with 6+ months tenure
        - Role must be suitable for remote work
        - Consistent performance record required
        - Manager approval mandatory<br/><br/>
        
        <b>2. Work Schedule</b><br/>
        - Hybrid: 3 days office, 2 days remote per week
        - Full remote: Available for specific roles only
        - Core hours: 10 AM - 3 PM must be available online
        - Flexible start/end times within 7 AM - 7 PM window<br/><br/>
        
        <b>3. Equipment and Setup</b><br/>
        - Company provides laptop, monitor, keyboard, mouse
        - $500 home office setup allowance
        - Ergonomic chair reimbursement up to $300
        - High-speed internet required (minimum 50 Mbps)<br/><br/>
        
        <b>4. Communication</b><br/>
        - Daily standup via video call at 9:30 AM
        - Respond to messages within 2 hours during work hours
        - Use company Slack/Teams for all work communication
        - Weekly team sync meetings mandatory<br/><br/>
        
        <b>5. Performance Monitoring</b><br/>
        - Regular check-ins with manager (weekly)
        - Deliverable-based performance tracking
        - Quarterly remote work policy review<br/><br/>
        
        <b>Operations:</b> operations@company.com
        """
    },
    
    "Legal_NDA_Policy.pdf": {
        "title": "Legal - Non-Disclosure Agreement Policy",
        "content": """
        <b>CONFIDENTIALITY AND NDA POLICY</b><br/><br/>
        
        <b>1. Confidential Information</b><br/>
        - Trade secrets and proprietary technology
        - Customer lists and business strategies
        - Financial data and pricing information
        - Unpublished product roadmaps
        - Employee personal information<br/><br/>
        
        <b>2. Employee Obligations</b><br/>
        - Sign NDA within first week of employment
        - Protect confidential information during and after employment
        - No disclosure to third parties without written authorization
        - Return all confidential materials upon termination<br/><br/>
        
        <b>3. Third-Party NDAs</b><br/>
        - Required before sharing any company information with vendors
        - Legal department must review all NDAs before signing
        - Standard NDA template available on legal portal
        - Mutual NDAs preferred for partnerships<br/><br/>
        
        <b>4. Data Handling</b><br/>
        - Encrypt all confidential documents
        - Use secure file sharing platforms only
        - No printing of highly sensitive documents
        - Shred physical confidential documents when disposing<br/><br/>
        
        <b>5. Violations</b><br/>
        - Immediate termination for intentional breaches
        - Legal action may be pursued
        - Report suspected breaches to legal@company.com immediately<br/><br/>
        
        <b>Legal Team:</b> legal@company.com
        """
    },
    
    "Engineering_Code_Review_Guidelines.pdf": {
        "title": "Engineering - Code Review Guidelines",
        "content": """
        <b>CODE REVIEW GUIDELINES</b><br/><br/>
        
        <b>1. Review Process</b><br/>
        - All code must be reviewed before merging to main branch
        - Minimum 2 approvals required for production code
        - Reviews should be completed within 24 hours
        - Use pull request templates for consistency<br/><br/>
        
        <b>2. Review Checklist</b><br/>
        - Code follows style guide and best practices
        - Adequate test coverage (minimum 80%)
        - No security vulnerabilities or code smells
        - Documentation updated for new features
        - Performance impact considered<br/><br/>
        
        <b>3. Best Practices</b><br/>
        - Keep pull requests small (max 400 lines)
        - Write descriptive commit messages
        - Include screenshots for UI changes
        - Link to relevant tickets/issues
        - Respond to review comments within 4 hours<br/><br/>
        
        <b>4. Code Standards</b><br/>
        - Python: Follow PEP 8 style guide
        - JavaScript: Use ESLint with company config
        - Use meaningful variable and function names
        - Comment complex logic and algorithms
        - No hardcoded credentials or secrets<br/><br/>
        
        <b>5. Testing Requirements</b><br/>
        - Unit tests for all new functions
        - Integration tests for API endpoints
        - E2E tests for critical user flows
        - All tests must pass before merge<br/><br/>
        
        <b>Engineering Lead:</b> tech.lead@company.com
        """
    },
    
    "Admin_Office_Facilities_Guide.pdf": {
        "title": "Administration - Office Facilities Guide",
        "content": """
        <b>OFFICE FACILITIES GUIDE</b><br/><br/>
        
        <b>1. Office Hours</b><br/>
        - Building access: 6 AM - 10 PM on weekdays
        - Weekend access: 8 AM - 6 PM (requires prior approval)
        - Reception desk: 8 AM - 6 PM Monday-Friday
        - Security: 24/7 on-site security personnel<br/><br/>
        
        <b>2. Meeting Rooms</b><br/>
        - Book via company calendar system
        - Maximum booking: 4 hours per session
        - Cancel if not needed (24 hours notice)
        - Available rooms: Conference A (20 people), Conference B (10 people),
          Small meeting rooms 1-5 (4-6 people each)<br/><br/>
        
        <b>3. Parking</b><br/>
        - Underground parking: 200 spaces available
        - First-come, first-served basis
        - Electric vehicle charging stations: 10 spots
        - Visitor parking: 20 spaces (register at reception)<br/><br/>
        
        <b>4. Cafeteria</b><br/>
        - Breakfast: 7:30 AM - 9:30 AM
        - Lunch: 12 PM - 2 PM
        - Snacks and beverages: All day
        - Free coffee, tea, and water
        - Subsidized meals for employees<br/><br/>
        
        <b>5. Gym and Wellness</b><br/>
        - On-site gym: 6 AM - 9 PM
        - Yoga classes: Tuesday and Thursday 6 PM
        - Meditation room available
        - Health checkup: Annual free health screening<br/><br/>
        
        <b>Facilities Manager:</b> facilities@company.com | Ext: 5678
        """
    }
}

# Generate PDFs
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=18,
    textColor='#6C63FF',
    spaceAfter=30,
)

for filename, doc_data in documents.items():
    filepath = os.path.join("test_documents", filename)
    pdf = SimpleDocTemplate(filepath, pagesize=letter)
    story = []
    
    # Add title
    title = Paragraph(doc_data["title"], title_style)
    story.append(title)
    story.append(Spacer(1, 0.2 * inch))
    
    # Add content
    content = Paragraph(doc_data["content"], styles['BodyText'])
    story.append(content)
    
    # Build PDF
    pdf.build(story)
    print(f"✅ Created: {filename}")

print(f"\n🎉 Successfully created {len(documents)} test PDFs in 'test_documents' folder!")
print("\nYou can now upload these PDFs to test the RAG system.")
