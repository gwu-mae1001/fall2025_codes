#!/usr/bin/env python3
"""
Email Sender Code For MAE1001
Sends the snake_scores.csv file to student's email
"""
import smtplib
from email.message import EmailMessage
import ssl
import os
import csv

# Email configuration (sender)
email_sender = "cs3907.edgelab@gmail.com"
email_password = "cwgr fxzm luhm dhbz"

# CSV file to send
score_file = 'snake_scores.csv'

def read_top_scorers():
    """Read and format top 5 scorers"""
    try:
        scores = []
        with open(score_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if row.get('Name') and row.get('Score') and row.get('Length'):
                        scores.append({
                            'name': row['Name'].strip(),
                            'score': int(row['Score']),
                            'length': int(row['Length'])
                        })
                except (ValueError, KeyError):
                    continue
        
        if not scores:
            return "No scores recorded yet."
        
        # Sort by score (descending)
        scores.sort(key=lambda x: x['score'], reverse=True)
        
        # Format top 5
        result = "\nTop 5 Scorers:\n"
        result += "="*40 + "\n"
        for i, entry in enumerate(scores[:5], 1):
            result += f"{i}. {entry['name']} - {entry['score']} pts (Length: {entry['length']})\n"
        result += "="*40 + "\n"
        
        return result
    
    except FileNotFoundError:
        return "No scores file found."
    except Exception as e:
        return f"Error reading scores: {e}"

def send_email():
    """Send the CSV file via email"""
    
    # Get student's email address
    print("\n" + "="*50)
    print("SEND SNAKE GAME SCORES")
    print("="*50 + "\n")
    
    email_receiver = input("Enter your email address: ").strip()
    
    while not email_receiver or '@' not in email_receiver:
        print("Invalid email address!")
        email_receiver = input("Enter your email address: ").strip()
    
    # Check if file exists
    if not os.path.exists(score_file):
        print(f"\n✗ Error: {score_file} not found!")
        print("  Please play the game first to generate scores.\n")
        return
    
    # Get top scorers
    top_scorers = read_top_scorers()
    
    # Create email message
    msg = EmailMessage()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "Snake Game Scores from Raspberry Pi"
    
    # Email body
    body = "This message is sent from Raspberry Pi, and here are the top scorers of the game:\n\n"
    body += top_scorers
    
    msg.set_content(body)
    
    # Attach the CSV file
    with open(score_file, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, 
                          maintype='text', 
                          subtype='csv', 
                          filename='snake_scores.csv')
    
    # Send email
    print("\nSending email...")
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context, timeout=30) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(msg)
        
        print("\n✓ EMAIL SENT SUCCESSFULLY!")
        print(f"  Sent to: {email_receiver}")
        print(f"  Attachment: {score_file}")
        print("\nCheck your inbox (and spam folder)!\n")
    
    except Exception as e:
        print(f"\n✗ Error sending email: {e}\n")

if __name__ == "__main__":
    send_email()