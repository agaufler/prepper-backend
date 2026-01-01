"""
Backend Server for Ultimate Prepper Guide
Handles payment processing with Stripe and PDF delivery via email
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend

# Stripe Configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

# Email Configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

# Price in cents ($5.99 = 599 cents)
PRODUCT_PRICE = 599

@app.route('/api/config', methods=['GET'])
def get_config():
    """Return Stripe publishable key to frontend"""
    return jsonify({
        'publishableKey': STRIPE_PUBLISHABLE_KEY,
        'price': PRODUCT_PRICE
    })

@app.route('/api/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """Create a Stripe Checkout Session"""
    try:
        data = request.json
        
        # Import survival_pdf_lib for PDF generation
        from survival_pdf_lib import generate_survival_pdf
        
        # Generate PDF first
        pdf_filename = f"ultimate_prepper_{data.get('scenario', 'guide').replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join('/tmp', pdf_filename)
        generate_survival_pdf(data, pdf_path)
        
        # Send email immediately with PDF (for test mode simplicity)
        # In production, this would be done via webhook after payment confirmation
        try:
            send_email_with_pdf(
                to_email=data.get('email'),
                user_data=data,
                pdf_path=pdf_path
            )
            print(f"✓ Email sent to {data.get('email')}")
        except Exception as e:
            print(f"✗ Email error: {e}")
            # Continue anyway - don't block checkout
        
        # Create Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f'Ultimate Prepper Guide - {data.get("scenario", "Survival")} Checklist',
                        'description': f'Personalized for {data.get("location", "your location")}',
                    },
                    'unit_amount': PRODUCT_PRICE,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='success_url='success_url = f"https://ultimateprepperguide.org/?success=true&email={data.get('email', '')}",
            cancel_url='https://ultimateprepperguide.org/?canceled=true, 
            customer_email=data.get('email'),
            metadata={
                'scenario': data.get('scenario'),
                'email': data.get('email'),
                'location': data.get('location'),
                'household_size': data.get('householdSize'),
                'pdf_path': pdf_path
            }
        )
        
        return jsonify({
            'sessionId': session.id
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@app.route('/api/webhook', methods=['POST'])
def stripe_webhook():
    """Handle Stripe webhook for successful payments"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET', '')
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400
    
    # Handle successful payment
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Get metadata
        pdf_path = session['metadata'].get('pdf_path')
        email = session['metadata'].get('email')
        scenario = session['metadata'].get('scenario')
        
        # Send email with PDF
        if pdf_path and email and os.path.exists(pdf_path):
            send_email_with_pdf(
                to_email=email,
                user_data=session['metadata'],
                pdf_path=pdf_path
            )
            
            # Clean up PDF after sending
            try:
                os.remove(pdf_path)
            except:
                pass
    
    return jsonify({'status': 'success'})

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    """Create a Stripe Payment Intent"""
    try:
        data = request.json
        
        # Create PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=PRODUCT_PRICE,
            currency='usd',
            metadata={
                'scenario': data.get('scenario'),
                'email': data.get('email'),
                'location': data.get('location'),
                'household_size': data.get('householdSize')
            }
        )
        
        return jsonify({
            'clientSecret': intent.client_secret
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 403

@app.route('/api/payment-success', methods=['POST'])
def payment_success():
    """
    Called after successful payment
    Generates PDF and sends via email
    """
    try:
        data = request.json
        user_data = data.get('userData', {})
        payment_intent_id = data.get('paymentIntentId')
        
        # Verify payment with Stripe
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        
        if intent.status != 'succeeded':
            return jsonify({'error': 'Payment not completed'}), 400
        
        # Generate PDF
        pdf_path = generate_pdf_for_user(user_data)
        
        # Send email with PDF
        send_email_with_pdf(
            to_email=user_data.get('email'),
            user_data=user_data,
            pdf_path=pdf_path
        )
        
        return jsonify({
            'success': True,
            'message': 'PDF sent to your email!'
        })
        
    except Exception as e:
        print(f"Error in payment_success: {str(e)}")
        return jsonify({'error': str(e)}), 500

def generate_pdf_for_user(user_data):
    """Generate personalized PDF based on user data"""
    scenario = user_data.get('scenario', 'EMP Attack')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{scenario.replace(' ', '_')}_{timestamp}.pdf"
    output_path = f"/tmp/{filename}"
    
    # Create placeholder PDF (replace with your actual PDF generator)
    from reportlab.pdfgen import canvas
    c = canvas.Canvas(output_path)
    c.drawString(100, 750, f"Your {scenario} Survival Guide")
    c.drawString(100, 730, f"Location: {user_data.get('location')}")
    c.drawString(100, 710, f"Household: {user_data.get('householdSize')} people")
    c.drawString(100, 690, f"Climate: {user_data.get('climate')}")
    c.drawString(100, 650, "This is a placeholder PDF.")
    c.drawString(100, 630, "Your actual personalized checklist will be generated here.")
    c.save()
    
    return output_path

def send_email_with_pdf(to_email, user_data, pdf_path):
    """Send email with PDF attachment"""
    
    scenario = user_data.get('scenario', 'Survival')
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = f'Your {scenario} Survival Guide - Ready to Download!'
    
    # Email body
    body = f"""Hi there!

Thank you for your purchase! Your personalized {scenario} Survival Guide is attached to this email.

Your Profile:
• Scenario: {scenario}
• Location: {user_data.get('location')}
• Household Size: {user_data.get('householdSize')} people
• Climate: {user_data.get('climate')}
• Experience Level: {user_data.get('experience')}

What's Inside Your Guide:
✓ Complete supply checklist with specific brands
✓ Quantities customized for your household size
✓ Priority levels (Critical → High → Medium → Low)
✓ Detailed explanations for why each item matters
✓ 72-hour action plan
✓ Storage and organization tips

Tips for Using Your Guide:
1. Print a copy and keep it with your emergency supplies
2. Check off items as you acquire them
3. Review and update your supplies every 6 months
4. Share relevant sections with family members

Questions or issues? Simply reply to this email.

Stay safe and prepared!

Best regards,
The Ultimate Prepper Team
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach PDF
    with open(pdf_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
        msg.attach(part)
    
    # Send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    server.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
    server.quit()
    print(f"Email sent successfully to {to_email}")

if __name__ == '__main__':
    print("Starting Prepper Guide Backend Server...")
    print(f"Email configured: {EMAIL_ADDRESS}")
    app.run(debug=True, host='0.0.0.0', port=5001)
